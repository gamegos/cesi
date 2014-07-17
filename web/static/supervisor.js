$(document).ready(function(){
  $(".btn").click(function(){
        var $tr = $(this).parent();
        var $link ="../show_info.py" 
        $.ajax({
                url: $link,
                dataType: 'json',
                success: function(data){
                    console.log(data['status'])
                    $tr.html(data['status']);
               }});
  });
});

