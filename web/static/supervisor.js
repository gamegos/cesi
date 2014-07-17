$(document).ready(function(){
  $("button").click(function(){
        var $tr = $(this).parent().parent();
        var $td = $tr.children('td').first();
        var $link = $(this).attr('name');
        $.ajax({
                url: $link,
                dataType: 'json',
                success: function(data){
                    if (data['data']['pid'] == 0 ){
                        $td.html("-");
                    }else{
                        $td.html(data['data']['pid']);
                    }
               }});
  });
});

