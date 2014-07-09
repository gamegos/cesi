<html>
 <head>
  <title>PHP Test</title>
 </head>
 <body>
<?php 
  $proc_name_re = $_POST['restart'];
  $proc_name_st = $_POST['stop'];
  $code = <<<EOD
  import php
  import xmlrpclib
  import getProcInfo
  
  address="http://%s:%s@%s:%s/RPC2" %(getProcInfo.Config.user, getProcInfo.Config.password, getProcInfo.Config.host, getProcInfo.Config.port)
  server = xmlrpclib.Server(address)
  server.supervisor.stopProcess(php.var('proc_name_st'))
  EOD;

  py_eval($code);
?>
 </body>
</html>
