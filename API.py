import tweepy
from tqdm import tqdm
import pandas as pd
from collections import Counter
import json
import plotly
import plotly.express as px
import plotly.io as pio 
import os 
from dotenv import load_dotenv


load_dotenv()
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def __validate__(user_name):
  try :
    api.user_timeline(screen_name = user_name)
    return True
  except tweepy.errors.NotFound:
    return False

def get_all(func,user_name,limit = 20,parse = lambda x:x, filter_ = lambda x:x,**kwargs):
    """
    get a list of all followers of a twitter account

    """
    returns = []
    for item in tqdm(tweepy.Cursor(func, screen_name=user_name,**kwargs).items(limit), position=0, leave=True,**kwargs):
        try:
            returns.append(item)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
    return list(map(parse,filter(filter_,returns)))

def get_tweets(user, limit = 100):
    user_tweets = pd.DataFrame()
    keys = ['id_str','created_at','text','in_reply_to_screen_name', 'retweeted', 'is_quote_status', 'favorite_count','retweet_count', 'lang' ]
    for status in get_all(api.user_timeline, user, limit):
        json = status._json
        user_tweets = user_tweets.append({key:json.get(key) for key in keys}, ignore_index=True)
    user_tweets['created_at'] = pd.to_datetime(user_tweets['created_at'])
    return user_tweets

def get_pp(user):
  try:
    return api.lookup_users(screen_name = user)[0].profile_image_url_https.replace('_normal','')
  except:
    return 'https://icon-library.com/images/default-user-icon/default-user-icon-8.jpg'
def path_image(path):
    return '<img style="border-radius: 20px; width: 80px; height: 80px;" class="pp" src="'+ path + '"  >'

def _analysis(tweets):
    #classes = 'table table-bordered table-hover table-sm table-responsive'
    classes = ''
    top_replies = list(tweets['in_reply_to_screen_name'].value_counts(sort = True, ascending = False).index)
    top_replies_html = (pd.DataFrame(list(zip(range(1,21),top_replies, map(get_pp,top_replies)))).rename({0:"Rank",1:"User",2:"Image"}, axis = 1).to_html(render_links=True,header=True,escape=False, index=False ,formatters={"Image":path_image},classes = classes,border= 0))
    ####
    cnt = pd.DataFrame(Counter(" ".join(tweets.query("retweeted == 0")['text'].str.replace('(\\n)|( : )',' ', regex=True).str.replace('(@[A-z0-9_]+)|(https.+\S)|(RT)|(#.+\S)','', regex=True)).split(" ")).items()).rename({0:"Word", 1:"Frequency"}, axis =1).sort_values("Frequency", ascending = False)
    filtered_words = cnt[(cnt['Word'].str.len()>=4) & (cnt['Word'].str.len()<=8)].sort_values("Frequency", ascending = False).reset_index(drop=1)[:51]
    filtered_words.index =  range(1,len(filtered_words)+1)
    filtered_words = filtered_words.reset_index().rename({"index":"Rank"})
    words_html = (filtered_words.to_html(header= True,index = False, escape=False, render_links=True, classes = classes))

    ####
    pio.templates.default = "plotly_white"
    xy = pd.DataFrame(tweets.created_at.dt.to_period('d').value_counts().sort_index())
    timef , timei = xy.index.max().strftime("%m/%Y"), xy.index.min().strftime("%m/%Y")
    fig = px.line(
         x=xy.index.to_timestamp(), y=xy['created_at'],
         labels = {'x':"Time", "y":"Tweet Count"}, color_discrete_sequence=["#1DA1F2"],
         width=950, height=280).update_layout(font_color="#f9f9f9", plot_bgcolor= "rgba(0,0,0,0)",paper_bgcolor= 'rgba(0,0,0,0)' )
    all_pub_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return [top_replies_html, words_html, {'fig':all_pub_json, 'from':timei,'to':timef }]
