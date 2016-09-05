var $login = function(){
    var $url = "/login/control";
    $.ajax({
        url: $url,
        dataType: 'json',
        type: 'post',
        data: $(this).parent().parent().serialize(),
        success: function(data){
            if(data['status']=='warning'){
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: data['message'],
                    type: 'warning',
                    closeWith: ['click']
                });
            }else{
               window.location='/'; 
            }
        },
        complete: function(){
            $(".loginform").find('input').each(function(){
                $(this).val("");
            });
        }
    });

}

var $adduser= function(){
    $(".activity-log").remove();
    var $link = "/add/user";
    $.ajax({
        url: $link,
        dataType: 'json',
        success: function(data){
            if(data['status'] == 'success'){
                $( "a > input:checked" ).each(function() {
                    $(this).prop( "checked",false );
                });
                
                var $maindiv = $('#maindiv');
                $maindiv.empty();
                $maindiv.append('<div class="col-lg-4"></div>');
                $maindiv.append('<div class="col-lg-4 use"></div>');
                $maindiv.append('<div class="col-lg-4"></div>');
                $middlegrid = $(".use");
                $middlegrid.prepend(' <div class="login-panel panel panel-default addauser"></div>');
                var $login_panel = $middlegrid.children('div').first();
                $login_panel.append('<div class="panel-heading"> <h3 class="panel-title">Please Enter User Information </h3>  </div>');
                $login_panel.append('<div class="add_user panel-body"></div>');

                var $panel_body =$('.add_user');
                $panel_body.append('<form class="adduserform" method="post" action="/add/user/handler">');

                var $form = $panel_body.children('form').first();
                $form.append('<fieldset></fieldset>');

                var $fieldset= $form.children('fieldset').first();
                $fieldset.append('<div class="form-group"> <input class="form-control" placeholder="Username" name="username"  autofocus> </div>');
                $fieldset.append('<div class="form-group"> <input class="form-control" placeholder="Password" name="password" type="password" value=""> </div>');
                $fieldset.append('<div class="form-group"> <input class="form-control" placeholder="Confirm Password" name="confirmpassword" type="password" value=""> </div>');
                $fieldset.append('<div class="form-group"> <select class="form-control" name="usertype"> <option selected>Standart User</option> <option>Admin</option> <option>Only Log</option> <option>Read Only</option> </select> </div>');
                $fieldset.append('<a class="btn btn-lg btn-success btn-block save" >Save</a>');

                $(".save").click($adduserhandler);
            }else{
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: 'Only can admin add a user.',
                    type: 'error',
                    closeWith: ['click']
                });
            }
        }
    });
}

var $adduserhandler = function(){
    var $url = "/add/user/handler";
    $.ajax({
        url: $url,
        dataType: 'json',
        type: 'post',
        data: $(this).parent().parent().serialize(),
        success: function(data){
            if(data['status']=="success"){
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: data['message'],
                    type: 'success',
                    closeWith: ['click']
                });
            }else if(data['status']=="null" || data['status']=="warning"){
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: data['message'],
                    type: 'warning',
                    closeWith: ['click']
                });

            }else{
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: data['message'],
                    type: 'error',
                    closeWith: ['click']
                });
            }
        }
    });
    
    $(".adduserform").find('input').each(function(){
        $(this).val("");
    });
}

var $showdeluserpage = function(){
    $(".activity-log").remove();
    var $link = "/delete/user";
    $.ajax({
        url: $link,
        dataType: 'json',
        success: function(data){
            if(data['status'] == "success"){
                $( "a > input:checked" ).each(function() {
                    $(this).prop( "checked",false );
                });

                var $maindiv = $('#maindiv');
                $maindiv.empty();
                $maindiv.prepend('<div class="login-panel panel panel-default deleteuser"></div>');
                
                var $panel = $maindiv.children('div').first();
                $panel.append('<div class="panel-heading"> <h3 class="panel-title">Delete User </h3>  </div>');
                $panel.append('<div class="panel-body"></div>');

                $addtable = $panel.children('div').last();

                $addtable.append('<div class="table-responsive"></div>');

                var $tablediv = $addtable.children('div').first();
                $tablediv.append('<table class="table table-striped table-bordered table-hover" id="dataTables-example">');

                var $table = $tablediv.children('table').first();
                $table.append('<tr><th>Username</th><th>Usertype</th><th></th></tr>');

                for(var i=1; i<data['names'].length; i++){
                    username = data['names'][i];
                    if(data['types'][i] == 0){
                        usertype = "Admin";
                    }else if(data['types'][i] == 1){
                        usertype = "Standart User";
                    }else if(data['types'][i] == 2){
                        usertype = "Only Log";
                    }else if(data['types'][i] == 3){
                        usertype = "Read Only";
                    }

                    $table.append('<tr class="'+username+'"></tr>');

                    var $maintr = $table.find('tr').last();
                    $maintr.append('<td>'+username+'</td> <td>'+usertype+'</td><td><button name="'+data['names'][i]+'" class="glyphicon glyphicon-trash btn btn-sm btn-success btn-block delete"></button></td>');

                    var $delbtn =$maintr.find('button').last();
                    $delbtn.click($delete_user);
                }
            }else{
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: 'Only admin can delete user',
                    type: 'error',
                    closeWith: ['click']
                });
            }
        } 
    });
}

var $delete_user = function(){
    var $username = $(this).attr('name')
    var $url = "/delete/user/"+$username
    if($url=="/delete/user/admin"){
        noty({
            timeout: 5000,
            layout: 'bottom',
            text: 'Admin can not be delete',
            type: 'error',
            closeWith: ['click']
        });

    }else if( confirm("Are you sure delete this user?") ){
        $.ajax({
            url: $url,
            dataType: 'json',
            success: function(data){
                if(data['status'] == 'success'){
                    $("."+$username).remove();
                }else{
                    noty({
                        timeout: 5000,
                        layout: 'bottom',
                        text: data['message'],
                        type: 'error',
                        closeWith: ['click']
                    });
                }
            }
        });
    }
}

var $changepassword = function(){
    $(".activity-log").remove();
    $username = $(this).attr('name');
    $link = "/change/password/"+$username;
    $.ajax({
        url: $link,
        dataType: 'json',
        success: function(data){
            if(data['status'] == "success"){
                $( "a > input:checked" ).each(function() {
                    $(this).prop( "checked",false );
                });

                var $maindiv = $('#maindiv');
                $maindiv.empty();

                $maindiv.append('<div class="col-md-4"></div>');
                $maindiv.append('<div class="col-md-4 use"></div>');
                $maindiv.append('<div class="col-md-4"></div>');
                $middlegrid = $(".use");

                $middlegrid.prepend('<div class="login-panel panel panel-default changepassworddiv"></div>'); 

                var $panel= $middlegrid.children('div').first();
                $panel.append('<div class="panel-heading"><h3 class="panel-title">Change Password</h3></div>');
                $panel.append('<div class="panel-body"><form class="changepasswordform" method="post" action="/change/password/'+$username+'/handler"><fieldset></fieldset></form></div>');

                var $fieldset =$middlegrid.find('fieldset');
                $fieldset.append('<div class="form-group"><input class="form-control" placeholder="Old password" name="old" type="password" autofocus></div>');
                $fieldset.append('<div class="form-group"><input class="form-control" placeholder="New Password" name="new" type="password"></div>');
                $fieldset.append('<div class="form-group"><input class="form-control" placeholder="Confirm Password" name="confirm" type="password"></div>');
                $fieldset.append('<a name="'+$username+'" class="btn btn-lg btn-success btn-block"> Save </a>');

                var $btn = $panel.find('a').last();
                $btn.click($passwordhandler);
            }else{
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: 'Unsuccesfull',
                    type: 'error',
                    closeWith: ['click']
                });

            }
        }
    }); 
}

var $passwordhandler = function(){
    var $username=$(this).attr('name');
    var $url = "/change/password/"+$username+"/handler";
    $.ajax({
        url: $url,
        dataType: 'json',
        type: 'post',
        data: $(this).parent().parent().serialize(),
        success: function(data){
            if(data['status']=="success"){
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: 'Password changed',
                    type: 'success',
                    closeWith: ['click']
                });

            }else if(data['status']=="null") {
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: data['message'],
                    type: 'warning',
                    closeWith: ['click']
                });
            }else{
                noty({
                    timeout: 5000,
                    layout: 'bottom',
                    text: data['message'],
                    type: 'error',
                    closeWith: ['click']
                });
            }
        }
   });

    $(".changepasswordform").find('input').each(function(){
        $(this).val("");
    });
}


var $buttonactions = function(){
    var button = $(this);
    var $tr = $(this).parent().parent();
    var $td = $tr.children('td').first().next();
    var $url = $(this).attr('name');
    var $place = $(this).attr('place');
    var $environment = $(this).attr('env');
    $.ajax({
        beforeSend: function(){
            button.prepend('<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> ');
            button.parent().parent().find('button').each(function(){
                $(this).addClass('disabled');
            });
        },
        url: $url,
        dataType: 'json',
        success: function(data){
            if(data['status'] == "Success"){
                if (data['data']['pid'] == 0 ){ $td.html("-"); }else{ $td.html(data['data']['pid']); }
                    
                    if( $place == "node" ){
                        $td = $td.next();
                        $td.html(data['data']['name']);
                    
                        $td = $td.next();
                        $td.html(data['data']['group']);
                    }else{
                        $td = $td.next();
                        $td.html($environment);
                        
                        $td = $td.next();
                        $td.html(data['nodename']);
                        
                        $td = $td.next();
                        $td.html(data['data']['name']);
                    }

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
                        $stop.attr('class',"btn btn-primary btn-block disabled");
                        $stop.attr('name'," ");
                        $stop.attr('value',"Stop");
                        $stop.html("Stop");
                    }
                }else if(data['status'] == "error2"){
                    noty({
                        timeout: 5000,
                        layout: 'bottom',
                        text: data['message'],
                        type: 'error',
                        closeWith: ['click']
                    });

                }else{
                    noty({
                        timeout: 5000,
                        layout: 'bottom',
                        text: "Error:"+data['message']+"  Code:"+data['code']+"  Payload:"+data['code'],
                        type: 'error',
                        closeWith: ['click']
                     });
                }
        }
    });
};

var $selectgroupenv = function(){
    $(".activity-log").remove();
    var $usertype = $(this).attr('usertype');
    console.log($usertype);
    var $maindiv = $("#maindiv");

    $('div[id^="panel"]').each(function(){
        $(this).remove();
    });

    var $dashboardiv = $(".dash");
    $dashboardiv.empty();

    var $logdiv = $("#dialog");
    $logdiv.empty();

    var $adduserdiv = $(".addauser");
    $adduserdiv.empty();

    var $deluserdiv = $(".deleteuser");
    $deluserdiv.empty();

    var $changepassworddiv = $(".changepassworddiv");
    $changepassworddiv.empty();

    var $checkbox = $(this).children('a').first().children('input').first();
    var ischecked = $checkbox.is(":checked");


    $( ".ajax2 > a > input:checked" ).each(function() {
       $(this).prop("checked", false);
    });
    var $group_name = $(this).find('input').attr('group');
    var $environment_name = $(this).find('input').attr('env');
    var $url = "/group/"+$group_name+"/environment/"+$environment_name

    var $emptycontrol = 0;
    var $checkcount = 0;

    if(ischecked){
        $checkbox.prop("checked", false);
        
        $(this).parent().parent().find('input').each(function(){
            if($(this).prop('checked') == true){
                $checkcount = $checkcount + 1;
            }
        });

        if($checkcount == 0){   
            $( "#group"+$group_name ).remove();
        }else{
            var $tr_u = $( "#group"+$group_name ).find("tr[class*='"+$environment_name+"']");
            if($tr_u.length > 0){
                $tr_u.each(function(){
                    if($usertype == 0 || $usertype == 1){
                        var $oldenv = $(this).children('td').first().next().next().text();
                    }else{
                        var $oldenv = $(this).children('td').first().next().text();
                    }
                    $oldenv = $oldenv.split(',');
                    if($oldenv.length > 1){
                        var $index = $oldenv.indexOf($environment_name);
                        $oldenv.splice($index,1);
                        var $newenv = $oldenv.join();
                        if($usertype == 0 || $usertype == 1){
                            $(this).children('td').first().next().next().text($newenv);
                        }else{
                            $(this).children('td').first().next().text($newenv);
                        }
                        $(this).children('td').first().next().next().next().next().next().next().next().find('button').first().attr('env', $newenv);
                        $(this).children('td').first().next().next().next().next().next().next().next().next().find('button').first().attr('env', $newenv);
                    }else{
                        $(this).remove();
                    }
                });
            }
        }

    }else{
        $checkbox.prop("checked", true);

        $(this).parent().parent().find('input').each(function(){
            if($(this).prop('checked') == true){
                $checkcount = $checkcount + 1;
            }
        });

        if($checkcount == 1){
 
            $maindiv.prepend('<div class="panel panel-primary panel-custom" id="group'+$group_name+'"></div>'); 
            $panel = $maindiv.children('div').first();
            $panel.append('<div class="panel-heading"><span class="glyphicon glyphicon-th-list"></span> '+ $group_name +'</div>');

            if($usertype == 0 || $usertype == 1){
                $panel.children('div').first().append('<div style="float:right;"><button class="btn btn-warning btn-sm multibtn" name="restart" >Restart</button><button class="btn btn-warning btn-sm multibtn" name="start" >Start</button><button class="btn btn-warning btn-sm multibtn" name="stop" >Stop</button></div>');
                $panel.find("button[class~='multibtn']").each(function(){
                    $(this).click($multievent);
                });
            }

            $panel.append('<table class="table table-bordered"></table>');
            $table = $panel.find('table');
            $table.append('<tr class="active"><th>Pid</th> <th>Environment</th> <th>Node name</th> <th>Name</th> <th>Uptime</th> <th>State</th> </tr>');
            
            if($usertype == 0 || $usertype == 1){
                $table.find('tr').first().prepend('<th><input type="checkbox" class="multiple"></th>');
            }

            $table.find("input[class='multiple']").change($multiplecheckbox);

            $.ajax({
                url: $url,
                dataType: 'json',
                success: function(result){
                    for(var $counter = 0; $counter < result['process_list'].length; $counter++){
            
                        var $pid = result['process_list'][$counter][0];
                        var $name = result['process_list'][$counter][1];
                        var $nodename = result['process_list'][$counter][2];
                        var $state = result['process_list'][$counter][4];
                        var $statename = result['process_list'][$counter][5];
                        var $uptime = result['process_list'][$counter][3];
                
                        $table.append('<tr class="'+$nodename+'x'+$group_name+'x'+$name+'x'+$environment_name+'"></tr>');
                        $tr = $('tr[class="'+$nodename+'x'+$group_name+'x'+$name+'x'+$environment_name+'"]');
            
                        if($usertype == 0 || $usertype == 1){ 
                            //check
                            $tr.append('<td> <input type="checkbox" class="single" node="'+$nodename+'" procname="'+$group_name+':'+$name+'"> </td>');                        
                        }
                        //pid
                        if($pid == 0){
                            $tr.append('<td> - </td>');
                        }else{
                            $tr.append('<td>'+$pid+'</td>');
                        }

                        //environment
                        $tr.append('<td>'+$environment_name+'</td>');
        
                        // nodename
                        $tr.append('<td>'+$nodename+'</td>');

                        //name
                        $tr.append('<td>'+$name+'</td>');
        
                        //Uptime
                        $tr.append('<td>'+$uptime+'</td>');
        
                        //Statename
                        if( $state==0 || $state==40 || $state==100 || $state==200 ){
                            $tr.append('<td class="alert alert-danger">'+$statename+ '</td>');
                        }else if($state==10 || $state==20){
                            $tr.append('<td class="alert alert-success">'+$statename+ '</td>');
                        }else{
                            $tr.append('<td class="alert alert-warning">'+$statename+ '</td>');
                        }
                       
                        if($usertype == 0 || $usertype == 1 ){ 
                            //buttons
                            if( $state==20 ){
                                $tr.append('<td></td>');
                                $td = $tr.children('td').last();
                                $td.append('<button place="group" class="btn btn-primary btn-block act" env="'+$environment_name+'" name="/node/'+$nodename+'/process/'+$group_name+':'+$name+'/restart" value="Restart">Restart</button>');
                                var $btn_restart = $td.children('button').first();
                                $btn_restart.click($buttonactions);
        
                                $tr.append('<td></td>');
                                var $td = $tr.children('td').last();
                                $td.append('<button place="group" class="btn btn-primary btn-block act" env="'+$environment_name+'" name="/node/'+$nodename+'/process/'+$group_name+':'+$name+'/stop" value="Stop">Stop</button>');
                                var $btn_stop = $td.children('button').first();
                                $btn_stop.click($buttonactions);
                            }else if($state==0){
                                $tr.append('<td></td>');
                                var $td= $tr.children('td').last();;
                                $td.append('<button place="group" class="btn btn-primary btn-block act" env="'+$environment_name+'" name="/node/'+$nodename+'/process/'+$group_name+':'+$name+'/start" value="Start">Start</button>');
                                var $btn_restart = $td.children('button').first();
                                $btn_restart.click($buttonactions);
        
                                $tr.append('<td></td>');
                                var $td = $tr.children('td').last();
                                $td.append('<button place="group" class="btn btn-primary btn-block disabled act" value="Stop">Stop</button>');
                                var $btn_stop = $td.children('button').first();
                                $btn_stop.click($buttonactions);
                            }
                        }
    
                        if($usertype == 0 || $usertype == 1 || $usertype == 2 ){
                            //Readlog
                             $tr.append('<td><a class="btn btn-primary btn-block act" nodename="'+$nodename+'" processgroup="'+$group_name+'" processname="'+$name+'" url="/node/'+$nodename+'/process/'+$group_name+':'+$name+'/readlog"> Readlog </a></td>');
                             var $readlog = $tr.children('td').last().children('a').first();
    
                             $readlog.click(function(){
                                 var url=$(this).attr('url');
                                 var nodename=$(this).attr('nodename');
                                 var processname=$(this).attr('processname');
                                 var processgroup=$(this).attr('processgroup');
                                 var classname = nodename+"_"+processgroup+"_"+processname
                                 var $dia = $("."+classname);
                                 var timer;
     
                                 if($dia.length==0){
                                     $logdiv.append('<div class="'+classname+'"></div>');
                                     $dia = $("."+classname);
                                 }
                                 $.ajax({
                                     url: url,
                                     dataType: 'json',
                                     success: function(log){
                                         if (log['status']=="success"){
                                             $dia.html('<pre>'+log['log']+'</pre>');
                                             $dia.dialog({
                                                 open: function(){
                                                     timer = setInterval(function () {
                                                         $.ajax({
                                                             url: url,
                                                             dataType: 'json',
                                                             success: function(log){
                                                                 $dia.html('<pre>'+log['log']+'</pre>');
                                                             }
                                                         });
                                                     },1000);
                                                 }, 
                                                 close: function(){
                                                     clearInterval(timer);
                                                 },
                                                 title: classname,
                                                 position: {
                                                     my: 'center top',
                                                     at: 'center center',
                                                     'of': $('#maindiv')
                                                 },
                                                 minHeight: 320,
                                                 minWidth: 640,
                                                 show: {
                                                     effect: "blind",
                                                     duration: 500
                                                 },
                                                 hide: {
                                                     effect: "clip",
                                                     duration: 500,
                                                 }
                                             }).parent().resizable({
                                                 containment: "#page-wrapper"
                                             }).draggable({
                                                 containment: "#page-wrapper",
                                                 opacity: 0.70
                                             });
                                         }else{
                                             noty({
                                                 timeout: 5000,
                                                 layout: 'bottom',
                                                 text: log['message'],
                                                 type: 'warning',
                                                 closeWith: ['click']
                                             });
                                         }
                                     }
                                 });
                             }); 
                        }    
                    }
                }
            });
        }else{
            $grouptable = $("#group"+$group_name).children('table');
            $.ajax({
                url: $url,
                dataType: 'json',
                success: function(result){
                    for(var $counter = 0; $counter < result['process_list'].length; $counter++){
                        var $pid = result['process_list'][$counter][0];
                        var $name = result['process_list'][$counter][1];
                        var $nodename = result['process_list'][$counter][2];
                        var $state = result['process_list'][$counter][4];
                        var $statename = result['process_list'][$counter][5];
                        var $uptime = result['process_list'][$counter][3];

                        if( $("tr[class^='"+$nodename+"x"+$group_name+"x"+$name+"']").length > 0 ){
                            $tr = $("tr[class^='"+$nodename+"x"+$group_name+"x"+$name+"']");
                            $newclass = $tr.attr('class')+"x"+$environment_name;
                            $tr.attr('class', $newclass);
                            if($usertype == 0 || $usertype == 1){
                                var $oldenv = $tr.children('td').first().next().next().text();
                            }else{
                                var $oldenv = $tr.children('td').first().next().text();
                            }
                            var $newenv = $oldenv+","+$environment_name;
                            if($usertype == 0 || $usertype == 1){
                                $tr.children('td').first().next().next().text($newenv);
                            }else{
                                $tr.children('td').first().next().text($newenv);
                            }
                            $tr.children('td').first().next().next().next().next().next().next().next().find('button').first().attr('env', $newenv);
                            $tr.children('td').first().next().next().next().next().next().next().next().next().find('button').first().attr('env', $newenv);
                        }else{
                        
                            $grouptable.append('<tr class="'+$nodename+'x'+$group_name+'x'+$name+'x'+$environment_name+'"></tr>');
                            $tr = $('.'+$nodename+'x'+$group_name+'x'+$name+'x'+$environment_name);
                        
                            if($usertype == 0 || $usertype == 1){
                            	//check
                            	$tr.append('<td> <input type="checkbox" class="single" node="'+$nodename+'" procname="'+$group_name+':'+$name+'"> </td>');
                            }                    
                            //pid
                            if($pid == 0){
                                $tr.append('<td> - </td>');
                            }else{
                                $tr.append('<td>'+$pid+'</td>');
                            }

                            //environment
                            $tr.append('<td>'+$environment_name+'</td>');
    
                            // nodename
                            $tr.append('<td>'+$nodename+'</td>');
    
                            //name
                            $tr.append('<td>'+$name+'</td>');
    
                            //Uptime
                                $tr.append('<td>'+$uptime+'</td>');
    
                            //Statename
                            if( $state==0 || $state==40 || $state==100 || $state==200 ){
                                $tr.append('<td class="alert alert-danger">'+$statename+ '</td>');
                            }else if($state==10 || $state==20){
                                $tr.append('<td class="alert alert-success">'+$statename+ '</td>');
                            }else{
                                $tr.append('<td class="alert alert-warning">'+$statename+ '</td>');
                            }
   			    if($usertype == 0 || $usertype == 1){ 
                            //buttons
                                if( $state==20 ){
                                    $tr.append('<td></td>');
                                    $td = $tr.children('td').last();
                                        $td.append('<button place="group" class="btn btn-primary btn-block act" env="'+$environment_name+'" name="/node/'+$nodename+'/process/'+$group_name+':'+$name+'/restart" value="Restart">Restart</button>');
                                var $btn_restart = $td.children('button').first();
                                    $btn_restart.click($buttonactions);
      
                                    $tr.append('<td></td>');
                                    var $td = $tr.children('td').last();
                                    $td.append('<button place="group" class="btn btn-primary btn-block act" env="'+$environment_name+'" name="/node/'+$nodename+'/process/'+$group_name+':'+$name+'/stop" value="Stop">Stop</button>');
                                    var $btn_stop = $td.children('button').first();
                                    $btn_stop.click($buttonactions);
                                }else if($state==0){
                                    $tr.append('<td></td>');
                                    var $td= $tr.children('td').last();;
                                    $td.append('<button place="group" class="btn btn-primary btn-block act" env="'+$environment_name+'" name="/node/'+$nodename+'/process/'+$group_name+':'+$name+'/start" value="Start">Start</button>');
                                    var $btn_restart = $td.children('button').first();
                                    $btn_restart.click($buttonactions);
      
                                    $tr.append('<td></td>');
                                    var $td = $tr.children('td').last();
                                    $td.append('<button place="group" class="btn btn-primary btn-block disabled act" value="Stop">Stop</button>');
                                    var $btn_stop = $td.children('button').first();
                                    $btn_stop.click($buttonactions);
                                }
			    }
    
			    if($usertype == 0 || $usertype == 1 || $usertype == 2){
                            //Readlog
                            $tr.append('<td><a class="btn btn-primary btn-block act" nodename="'+$nodename+'" processgroup="'+$group_name+'" processname="'+$name+'" url="/node/'+$nodename+'/process/'+$group_name+':'+$name+'/readlog"> Readlog </a></td>');
                            var $readlog = $tr.children('td').last().children('a').first();
    
                            $readlog.click(function(){
                                var url=$(this).attr('url');
                                var nodename=$(this).attr('nodename');
                                var processname=$(this).attr('processname');
                                var processgroup=$(this).attr('processgroup');
                                var classname = nodename+"_"+processgroup+"_"+processname
                                var $dia = $("."+classname);
                                var timer;
    
                            if($dia.length==0){
                                    $logdiv.append('<div class="'+classname+'"></div>');
                                    $dia = $("."+classname);
                                }
                                $.ajax({
                                    url: url,
                                    dataType: 'json',
                                    success: function(log){
                                        if (log['status']=="success"){
                                            $dia.html('<pre>'+log['log']+'</pre>');
                                            $dia.dialog({
                                                open: function(){
                                                    timer = setInterval(function () {
                                                        $.ajax({
                                                            url: url,
                                                            dataType: 'json',
                                                            success: function(log){
                                                                $dia.html('<pre>'+log['log']+'</pre>');
                                                            }
                                                        });
                                                    },1000);
                                                },
                                                close: function(){
                                                    clearInterval(timer);
                                                },
                                                title: classname,
                                                 position: {
                                                     my: 'center top',
                                                     at: 'center center',
                                                     'of': $('#maindiv')
                                                 },
                                                 minHeight: 320,
                                                 minWidth: 640,
                                                show: {
                                                    effect: "blind",
                                                    duration: 500
                                                }
                                            }).parent().resizable({
                                                containment: "#page-wrapper"
                                            }).draggable({
                                                containment: "#page-wrapper",
                                                opacity: 0.70
                                            });
                                        }else{
                                            noty({
                                                timeout: 5000,
                                                layout: 'bottom',
                                                text: log['message'],
                                                type: 'warning',
                                                closeWith: ['click']
                                            });
                                        }
                                    }
                                });
                            });
			    }
                        }
                    }
                }
            });
        }
    }    
}

var $selectnode = function(){
    $(".activity-log").remove();
    var $usertype = $(this).attr('usertype');
    var $maindiv = $("#maindiv");
    var $dashboardiv = $(".dash");
    $dashboardiv.empty();
    
    var $logdiv = $("#dialog");
    $logdiv.empty();

    var $adduserdiv = $(".addauser");
    $adduserdiv.empty();

    var $deluserdiv = $(".deleteuser");
    $deluserdiv.empty();

    var $changepassworddiv = $(".changepassworddiv");
    $changepassworddiv.empty();

    $('div[id^="group"]').each(function(){
        $(this).remove();
    });

    $( ".ajax3 > a > input:checked" ).each(function() {
       $(this).prop("checked", false);
    });

    var $checkbox = $(this).children('a').first().children('input').first();
    var ischecked = $checkbox.is(":checked");
    var $oldcheckednodelist=[];
    var $newcheckednodelist=[];
    var $olduncheckednodelist=[];
    var $newuncheckednodelist=[];
    var $appendlist=[];
    var $removelist=[];

// List of cheked unchecked node list before clik event    
    $( ".ajax2 > a > input:checked" ).each(function() {
        var name = $(this).attr('value')
        if( $oldcheckednodelist.indexOf(name) == -1 ){
            $oldcheckednodelist.push(name);
        }
    });

    $( ".ajax2 > a > input:not(:checked)" ).each(function() {
        var name = $(this).attr('value')
        if( $olduncheckednodelist.indexOf(name) == -1 ){
            $olduncheckednodelist.push(name);
        }
    });

    if( $(this).attr('class')=="showall" ){
        $( ".ajax2 > a > input:not(:checked)" ).each(function() {
            $(this).prop("checked", true);
        });
        $newuncheckednodelist=[];
        $.ajax({
            url: "/node/name/list",
            dataType: 'json',
            async: false,
            success: function(nodenames){
                $newcheckednodelist = nodenames['node_name_list'];
            }
        });
    }else{
        if(ischecked){
            $(" a input[value='"+$checkbox.attr('value')+"']").each(function(){
                $(this).prop("checked", false);
            });
        }else{
            $(" a input[value='"+$checkbox.attr('value')+"']").each(function(){
                $(this).prop("checked", true);
            });
        }

        $( ".ajax2 > a > input:checked" ).each(function() {
            var name = $(this).attr('value')
            if( $newcheckednodelist.indexOf(name) == -1 ){
                $newcheckednodelist.push(name);
            }
        });

        $( ".ajax2 > a > input:not(:checked)" ).each(function() {
            var name = $(this).attr('value')
            if( $newuncheckednodelist.indexOf(name) == -1 ){
                $newuncheckednodelist.push(name);
             }
        });
    }

    $newcheckednodelist.forEach(function(item){
        if( $olduncheckednodelist.indexOf(item) != -1 ){
            if( $appendlist.indexOf(item) == -1 ){
                $appendlist.push(item);
            }
        }
    });

    $newuncheckednodelist.forEach(function(item){
        if( $oldcheckednodelist.indexOf(item) != -1 ){
            $removelist.push(item);
        }
    });

    $removelist.forEach(function(nodename){
        var $panel = $("#panel"+nodename);
        $panel.remove();
    });

    $appendlist.forEach(function(nodename) { 
        var $url = "/node/"+nodename
        $.ajax({
            url: $url,
            dataType: 'json',
            success: function(result){
                $maindiv.prepend('<div class="panel panel-primary panel-custom" id="panel'+nodename+'"></div>');
                var $panel = $("#panel"+nodename);
                $panel.append('<div class="panel-heading"><span class="glyphicon glyphicon-th-list"></span> '+ nodename +'</div>');

                if($usertype == 0 || $usertype == 1){
                    $panel.children('div').first().append('<div style="float:right;"><button class="btn btn-warning btn-sm multibtn" name="restart" >Restart</button><button class="btn btn-warning btn-sm multibtn" name="start" >Start</button><button class="btn btn-warning btn-sm multibtn" name="stop" >Stop</button></div>'); 
                    $panel.find("button[class~='multibtn']").each(function(){
                        $(this).click($multievent);
                    });
                }
                
                $panel.append('<table class="table table-bordered" id="table'+nodename+'" ></table>');
                var $table = $("#table"+nodename);
                $table.append('<tr class="active"><th>Pid</th> <th>Name</th> <th>Group</th> <th>Uptime</th> <th>State</th> </tr>');
                if($usertype == 0 || $usertype == 1){
                    $table.find('tr').first().prepend('<th><input type="checkbox" class="multiple"></th>');
                }

                $table.find("input[class='multiple']").change($multiplecheckbox);
                for(var $counter = 0; $counter < result['process_info'].length; $counter++){
                    var description = result['process_info'][$counter]['description'];
                    $table = $table.append('<tr class="process_info" id="'+nodename+$counter+'"></tr>');
                    var $tr_p = $('#'+nodename+$counter);
                    var $pid = result['process_info'][$counter]['pid'];
                    var $name = result['process_info'][$counter]['name'];
                    var $group = result['process_info'][$counter]['group'];
                    var $uptime = description.match('uptime') != null ? description.replace(/^(.+uptime\s)*(.+)$/, '$2') : '-';
                    var $state = result['process_info'][$counter]['state'];
                    var $statename = result['process_info'][$counter]['statename'];
                    if($usertype == 0 || $usertype == 1){
                        //check
                        $tr_p.append('<td> <input type="checkbox" class="single" node="'+nodename+'" procname="'+$group+':'+$name+'"> </td>');
                    }
                    //pid
                    if( $pid == 0 ){
                        $tr_p.append('<td> - </td>');
                    }else{
                        $tr_p.append('<td>'+ $pid + '</td>');
                    }

                   //name
                   $tr_p.append('<td>'+ $name + '</td>')

                   //group
                   $tr_p.append('<td>'+ $group + '</td>');

                   //uptime
                   $tr_p.append('<td>'+ $uptime + '</td>');

                   //statename
                   if( $state==0 || $state==40 || $state==100 || $state==200 ){
                       $tr_p.append('<td class="alert alert-danger">'+ $statename + '</td>');
                   }else if($state==10 || $state==20){
                       $tr_p.append('<td class="alert alert-success">'+ $statename + '</td>');
                   }else{
                       $tr_p.append('<td class="alert alert-warning">'+ $statename + '</td>');
                   }

                   //buttons
                   if($usertype == 0 || $usertype == 1){
                       if( $state==20 ){
                           $tr_p.append('<td></td>');
                           $td_p = $tr_p.children('td').last();
                           $td_p.append('<button place="node" class="btn btn-primary btn-block act" name="/node/'+nodename+'/process/'+$group+':'+$name+'/restart" value="Restart">Restart</button>');
                           var $btn_restart = $td_p.children('button').first();
                           $btn_restart.click($buttonactions);

                           $tr_p.append('<td></td>');
                           var $td_p = $tr_p.children('td').last();
                           $td_p.append('<button place="node" class="btn btn-primary btn-block act" name="/node/'+nodename+'/process/'+$group+':'+$name+'/stop" value="Stop">Stop</button>');
                           var $btn_stop = $td_p.children('button').first();
                           $btn_stop.click($buttonactions);
                        }else if($state==0){
                           $tr_p.append('<td></td>');
                           var $td_p = $tr_p.children('td').last();;
                           $td_p.append('<button place="node" class="btn btn-primary btn-block act" name="/node/'+nodename+'/process/'+$group+':'+$name+'/start" value="Start">Start</button>');
                           var $btn_restart = $td_p.children('button').first();
                           $btn_restart.click($buttonactions);

                           $tr_p.append('<td></td>');
                           var $td_p = $tr_p.children('td').last();
                           $td_p.append('<button place="node" class="btn btn-primary btn-block disabled act" value="Stop">Stop</button>');
                           var $btn_stop = $td_p.children('button').first();
                           $btn_stop.click($buttonactions);
                        }
                    }

                    if($usertype == 0 || $usertype == 1 || $usertype == 2){
                        //Readlog
                        $tr_p.append('<td><a class="btn btn-primary btn-block act" nodename="'+nodename+'" processgroup="'+$group+'" processname="'+$name+'" url="/node/'+nodename+'/process/'+$group+':'+$name+'/readlog"> Readlog </a></td>');
                        var $readlog = $tr_p.children('td').last().children('a').first();
    
                        $readlog.click(function(){
                            var url=$(this).attr('url');
                            var nodename=$(this).attr('nodename');
                            var processname=$(this).attr('processname');
                            var processgroup=$(this).attr('processgroup');
                            var classname = nodename+"_"+processgroup+"_"+processname
                            var $dia = $("."+classname);
                            var timer;

                            if($dia.length==0){
                                $logdiv.append('<div class="'+classname+'"></div>');
                                $dia = $("div[class='"+classname+"']");
                            }
                            $.ajax({
                                url: url,
                                dataType: 'json',
                                success: function(log){
                                    if (log['status']=="success"){
                                        $dia.html('<pre>'+log['log']+'</pre>');
                                        $dia.dialog({
                                            open: function(){
                                                timer = setInterval(function () {
                                                    $.ajax({
                                                        url: url,
                                                        dataType: 'json',
                                                        success: function(log){
                                                            $dia.html('<pre>'+log['log']+'</pre>');
                                                        }
                                                    });
                                                },1000);
                                            },
                                            close: function(){
                                                console.log("kapandiii");
                                                clearInterval(timer);
                                            },
                                            title: classname,
                                            position: {
                                                my: 'center top',
                                                at: 'center center',
                                                'of': $('#maindiv')
                                            },
                                            minHeight: 320,
                                            minWidth: 640,
                                            show: {
                                                effect: "blind",
                                                duration: 500
                                            },
                                            hide: {
                                                effect: "clip",
                                                duration: 500,
                                            }
                                        }).parent().resizable({
                                            containment: "#page-wrapper"
                                        }).draggable({
                                            containment: "#page-wrapper",
                                            opacity: 0.70
                                        });
                                    }else{
                                        noty({
                                            timeout: 5000,
                                            layout: 'bottom',
                                            text: log['message'],
                                            type: 'warning',
                                            closeWith: ['click']
                                        });
    
                                    }
                                }
                            });
                        });
                    }
                }
            }  
        });
    });
}

var $multiplecheckbox = function(){
    var $checkstatus = $(this).prop('checked');
    $table = $(this).parent().parent().parent();

    $table.find("input[class='single']").each(function(){
        $(this).prop('checked', $checkstatus);
    });
}

var $multievent = function(){
    var actlist = [];
    $actname = $(this).attr('name');
    $table = $(this).parent().parent().parent().children('table').first().find('input.single');
    $table.each(function(){
        if($(this).prop("checked")== true){
            var $nodename = $(this).attr('node');
            var $procname = $(this).attr('procname');
            var $td = $(this).parent().first().next();
            var $place = $(this).parent().first().next().next().next().next().next().next().find('button').attr('place');
            var $environment = $(this).parent().first().next().next().next().next().next().next().find('button').attr('env');
            $.ajax({
                url: "/node/"+$nodename+"/process/"+$procname+"/"+$actname,
                dataType: 'json',
                success: function(data){
                    if(data['status'] == "Success"){
                        if (data['data']['pid'] == 0 ){ $td.html("-"); }else{ $td.html(data['data']['pid']); }
    
                            if( $place == "node" ){
                                $td = $td.next();
                                $td.html(data['data']['name']);
        
                                $td = $td.next();
                                $td.html(data['data']['group']);
                            }else{
                                $td = $td.next();
                                $td.html($environment);

                                $td = $td.next();
                                $td.html(data['nodename']);

                                $td = $td.next();
                                $td.html(data['data']['name']);
                            }

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
                        
                        noty({
                            layout: 'bottom',
                            text: data['message'],
                            type: 'success',
                            closeWith: ['click'],
                            timeout: 5000
                        });
                    }else{
                        noty({
                            layout: 'bottom',
                            text: data['message'],
                            type: 'error',
                            closeWith: ['click'],
                            timeout: 5000
                        });
                    }
                }
            }); 
        }
    });
}


$( document ).ready(function() {
    $(".showall").click($selectnode);
    $(".login").click($login);
    $(".ajax2").click($selectnode);
    $(".act").click($buttonactions);
    $(".adduser").click($adduser);
    $(".deluser").click($showdeluserpage);
    $(".changepassword").click($changepassword);
    $(".ajax3").click($selectgroupenv);

        $.ajax({
            url: "/activitylog",
            dataType: 'json',
            success: function(log){
                if(log['status'] == "success"){
                    $(".activity-log").children('p').first().html(function(){
                        for(var i=0; i< log['log'].length; i++){
                            log['log'][i] = '&nbsp&nbsp'+log['log'][i]+'<br>'
                        }
                        return log['log']
                    });
                }else{
                    noty({
                        layout: 'bottom',
                        text: log['message'],
                        type: 'error',
                        closeWith: ['click'],
                        timeout: 5000
                    });
                }
            }
        });
});

$(window).unload(function(){
    $( "input:checked" ).each(function() {
        $(this).prop( "checked",false );
    });   
    

 
});
