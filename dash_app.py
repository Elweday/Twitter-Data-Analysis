from dash import Dash, html, dcc,  Input, Output
import plotly.express as px
import pandas as pd
import plotly.io as pio
from datetime import date

pio.templates.default = "plotly_white"
df = pd.read_csv("test.csv")
#df['data_text']= df['data_text'].str.replace('(\\n)|( : )',' ', regex=True).str.replace('(@[A-z0-9_]+)|(https.+\S)|(RT)|(#.+\S)','', regex=True)
entities = list(filter(lambda x:"entity_name" in x, df.columns))
domains = list(filter(lambda x:"domain_name" in x, df.columns))
df[entities+domains].melt(id_vars=domains).dropna()
df['data_created_at'] = pd.to_datetime( df['data_created_at'] )
df['data_created_at']

app = Dash(__name__)

xy = pd.DataFrame(df.data_created_at.dt.to_period('d').value_counts().sort_index())
xy['year'] = xy.index.to_timestamp().year
timef , timei = xy.index.max().strftime("%m/%Y"), xy.index.min().strftime("%m/%Y")
fig = px.area(
                 x=xy.index.to_timestamp().strftime("%d/%m"), y=xy['data_created_at'],color = xy['year'],
                 title=f"<b>Tweet Activity</b> From {timei} to {timef}", labels = {'x':"Date", "y":"Tweet Count", "color":"Year"}, color_discrete_sequence=["#2191fb","#ba274a","#841c26","#b2ece1","#8cdedc"],
)
               


#df = pd.DataFrame({
#    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#    "Amount": [4, 1, 2, 2, 4, 0],
#    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
#})

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children=
    f'''Your average tweet length is {30}'''),


    dcc.Graph(
        id='tweet-activity',
        figure=fig
    )

])
#DateRangePickerCallBack
""" @app.callback(
    Output('tweet-activity', 'figure'),
    Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date')
    )
def filter_tweet_activity(start_date, end_date):
    xy = pd.DataFrame(df.data_created_at.dt.to_period('d').value_counts().sort_index())
    xy = xy.loc[start_date:end_date]
    timef , timei = xy.index.max().strftime("%m/%Y"), xy.index.min().strftime("%m/%Y")
    fig = px.area(
                 x=xy.index.to_timestamp().strftime("%d/%m"), y=xy['data_created_at'],color = xy['year'],
    )
    fig.update_layout(transition_duration=500)
    return fig  """
#DateRangePicker
"""     dcc.DatePickerRange(
        id='date-filter',
        min_date_allowed=date(2023, 1, 1),
        max_date_allowed=date.today(),
        initial_visible_month=date(2023, 1, 1),
        end_date=date.today()
    ), """

if __name__ == '__main__':
    app.run_server(debug=True)
