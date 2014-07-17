$(document).ready(function(){
  $(".btn").click(function(){
        var $tr = $(this).parent();
        var $link = $(this).children('a').attr('href')
        $.ajax({
                url: $link,
                dataType: 'json',
                success: function(data){
                    $tr.html(data['status']);
               }});
  });
});

