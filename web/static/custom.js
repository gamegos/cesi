var $actc = function(){
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
                        $name = "/node/"+data['nodename'] + "/process/" + data['data']['group'] + ":" + data['data']['name'] + "/restart";
                        $restart.attr('name',$name );
                        $restart.attr('value',"Restart");
                        $restart.html("Restart");
                        
                        $td = $td.next();
                        $stop = $td.children('button').first();
                        $stop.attr('class',"btn btn-primary btn-block");
                        $name2 = "/node/"+data['nodename'] + "/process/" + data['data']['group'] + ":" + data['data']['name'] + "/stop";
                        $stop.attr('name',$name2 );
                        $stop.attr('value',"Stop");
                        $stop.html("Stop");
                    }else if(data['data']['state']==0){
                        $start = $td.children('button');
                        $start.attr('class',"btn btn-primary btn-block");
                        $name = "/node/"+data['nodename'] + "/process/" + data['data']['group'] + ":" + data['data']['name'] + "/start";
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
  };



var $select = function(){
        var $maindiv = $("#maindiv");
        $maindiv.empty();
        $( ".ui-selected").each(function() { 
            var $node_name = $(this).find('a').attr('value');
            var $url = "/node/"+$node_name
            $.ajax({
                url: $url,
                dataType: 'json',
                success: function(result){
                                $maindiv.append('<div class="panel panel-primary panel-custom" id="panel'+$node_name+'"></div>');
                                $panel = $("#panel"+$node_name);
                                $panel.append('<div class="panel-heading"><span class="glyphicon glyphicon-th-list"></span> '+ $node_name +'</div>');
                                $panel.append('<table class="table table-bordered" id="table'+$node_name+'" ></table>');
                                $table = $("#table"+$node_name);
                                $table = $table.append('<tr class="active"> <th>Pid</th> <th>Name</th> <th>Group</th> <th>Uptime</th> <th>State name</th> <th></th> <th></th> </tr>');
                                for (var $counter = 0; $counter < result['process_info'].length; $counter++){
                                    $table = $table.append('<tr class="process_info" id="'+$node_name+$counter+'"></tr>');
                                    $tr_p = $('#'+$node_name+$counter);
                                    //pid
                                    if( result['process_info'][$counter]['pid'] == 0 ){
                                        $tr_p.append('<td> - </td>');
                                    }else{
                                        $tr_p.append('<td>'+ result['process_info'][$counter]['pid'] + '</td>');
                                    }

                                    //name
                                    $tr_p.append('<td>'+ result['process_info'][$counter]['name'] + '</td>')

                                    //group
                                    $tr_p.append('<td>'+ result['process_info'][$counter]['group'] + '</td>');

                                    //uptime
                                    var $uptime = result['process_info'][$counter]['description'].substring(17,24)
                                    $tr_p.append('<td>'+ $uptime + '</td>');

                                    //statename
                                    $state = result['process_info'][$counter]['state'];
                                    if( $state==0 || $state==40 || $state==100 || $state==200 ){
                                        $tr_p.append('<td class="alert alert-danger">'+ result['process_info'][$counter]['statename'] + '</td>');
                                    }else if($state==10 || $state==20){
                                        $tr_p.append('<td class="alert alert-success">'+ result['process_info'][$counter]['statename'] + '</td>');
                                    }else{
                                        $tr_p.append('<td class="alert alert-warning">'+ result['process_info'][$counter]['statename'] + '</td>');
                                    }

                                    //buttons
                                     if( $state==20 ){
                                        $tr_p.append('<td><button class="btn btn-primary btn-block act" name="/node/'+$node_name+'/process/'+result['process_info'][$counter]['group']+':'+result['process_info'][$counter]['name']+'/restart" value="Restart">Restart</button></td><td><button class="btn btn-primary btn-block act" name="/node/'+$node_name+'/process/'+result['process_info'][$counter]['group']+':'+result['process_info'][$counter]['name']+'/stop" value="Stop">Stop</button> </td>');
                                    }else if($state==0){
                                        $tr_p.append('<td><button class="btn btn-primary btn-block act" name="/node/'+$node_name+'/process/'+result['process_info'][$counter]['group']+':'+result['process_info'][$counter]['name']+'/start" value="Start">Start</button></td><td><button class="btn btn-primary btn-block disabled act" value="Stop">Stop</button> </td>');
                                    }
$(".act").click($actc)
                                }
                        }  
                });
         });
}

var $showallprocess = function(){
}

$( document ).ready(function() {
    $(".ajax2").click($select);
    $("#selectable").selectable();
    $(".act").click($actc);
});
