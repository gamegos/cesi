$(document).ready(function(){
  $(".btn").click(function(){
        var $tr = $(this).parent(); 
        $.ajax({
                url: 'demo_test.html',
                dataType: 'json',
                success: function(data){
                    $.html(data['status']);
               }});
  });
});

