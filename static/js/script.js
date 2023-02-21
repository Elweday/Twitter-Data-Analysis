$(document).ready(function() {
    const reg = /^[A-Za-z0-9_]{4,15}$/;
    function tweak(){
      $("#user").blur();
      $("#user").addClass("disabled")
      $("#search").addClass("disabled")
      $("#search").html('<div class="spinner-grow spinner-grow-sm" role="status"></div>');
      $("#user").removeClass("is-valid")

    }
    $("#f").on('submit',function(event) {
      event.preventDefault();
      tweak();
      $("#f").unbind("submit");
      document.getElementById("f").submit(); $("#f").submit()

    });
    


      $("#user").on("input", function() {
       if (reg.test($("#user").val()))
       {
        $("#user").attr('class', 'form-control is-valid');
        $("#search").prop('disabled', false);
       }
       else
       {
        $("#user").attr('class', 'form-control is-invalid');
        $("#search").prop('disabled', true);
       }
      });
  });