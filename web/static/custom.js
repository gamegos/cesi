
$(document).ready(function(){
    $(".act").click(function(){
        var $tr = $(this).parent().parent();
        var $td = $tr.children('td').first();
        var $link = $(this).attr('name');
        $.ajax({
                url: $link,
                dataType: 'json',
                success: function(data){
                    if (data['data']['pid'] == 0 ){ $td.html("-"); }else{ $td.html(data['data']['pid']); }
                    
                    $td = $td.next();
                    $td.html(data['data']['name']);

                    $td = $td.next();
                    $td.html(data['data']['group']);

                    $td = $td.next();
                    $td.html(data['data']['description'].substring(17,24));

                    $td = $td.next();
                    if( data['data']['state']==0 || data['data']['state']==40 || data['data']['state']==100 || data['data']['state']==200 ){
                        $td.attr('class', "alert alert-danger");
                    }else if( data['data']['state']==10 || data['data']['state']==20 ){
                        $td.attr('class', "alert alert-success");
                    }else{
                        $td.attr('class', "alert alert-warning");
                    }
                    $td.html(data['data']['statename']);

                    $td = $td.next();
                    if( data['data']['state']==20){
                        $restart = $td.children('button').first();
                        $restart.attr('class',"btn btn-primary btn-block");
                        $name0 = "\/node\/";
                        $name = $name0.concat(data['nodename'], "\/process\/", data['data']['group'], ":", data['data']['name'], "\/restart");
                        $restart.attr('name',$name );
                        $restart.attr('value',"Restart");
                        $restart.html("Restart");
                        
                        $td = $td.next();
                        $stop = $td.children('button').first();
                        $stop.attr('class',"btn btn-primary btn-block");
                        $name2 = $name0.concat(data['nodename'], "\/process\/", data['data']['group'], ":", data['data']['name'], "\/stop");
                        $stop.attr('name',$name2 );
                        $stop.attr('value',"Stop");
                        $stop.html("Stop");
                    }else if(data['data']['state']==0){
                        $start = $td.children('button');
                        $start.attr('class',"btn btn-primary btn-block");
                        $name0 = "\/node\/";
                        $name = $name0.concat(data['nodename'], "\/process\/", data['data']['group'], ":", data['data']['name'], "\/start");
                        $start.attr('name',$name );
                        $start.attr('value',"Start");
                        $start.html("Start");

                        $td = $td.next();
                        $stop = $td.children('button').first();
                        $stop.attr('class',"btn btn-primary btn-block");
                        $stop.attr('class',"btn btn-primary btn-block disabled");
                        $stop.attr('name'," ");
                        $stop.attr('value',"Stop");
                    }
               }});
  });



$(".ajax").click(function(){
        var $li = $(this).parent();
        console.log($li)
        var $ul = $li.children('ul');
        console.log($ul)
        var $nodeli = $ul.children('li').first();
        console.log($nodeli)
        var $a = $nodeli.children('a').first();
        console.log($a)
        var $url = "/node/name/list";
        console.log($url)
        $.ajax({
                url: $url,
                dataType: 'json',
                success: function(result){
                    for($counter = 0; $counter < result['node_name_list'].length; $counter++){
                        console.log($counter);
                        $a.html(result['node_name_list'][$counter]);
                        console.log($a);
                        $nodeli = $nodeli.next();
                        console.log($nodeli);
                        $a = $nodeli.children('a').first();
                        console.log($a);
                    }
                }});
        });

});
