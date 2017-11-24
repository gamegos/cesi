'use strict';

angular.module('cesiApp.nodes', [
        'ui.router',
        'cesiLib'
    ])

    .config(function ($stateProvider) {
        $stateProvider.state('nodes', {
            url: '/nodes?grouping',
            controller: 'NodesCtrl',
            templateUrl: 'static/scripts/nodes/nodes.html'
        });
    })


    .controller('NodesCtrl', ['$scope', 'cesiService', '$stateParams',
            function ($scope, cesiService, $stateParams) {

        $scope.nodeGrouping = ($stateParams.grouping + '').toLowerCase();
        if($scope.nodeGrouping != 'groups' && $scope.nodeGrouping != 'environments') $scope.nodeGrouping = ''

        $scope.nodeNames = [];
        $scope.nodeMap = {};

        $scope.processStatus = {};
        $scope.processes = {};

        $scope.checkboxModel = {};

        $scope.environments = {};
        $scope.groups = {};
        $scope.selectedGroups = [];
        $scope.logs = {}

        $scope.getEnvironmentsAndGroups = function () {
            cesiService.dashboard().then(function (data) {
                for (var i = 0; i < data.environment_name_list.length; i++) { 
                    $scope.environments[data.environment_name_list[i]] = data.environment_list[i]
                }

                for (var i = 0; i < data.g_environment_list.length; i++) { 
                    $scope.groups[data.group_list[i]] = {"name":data.group_list[i], "envs":[], "envCount":0, "processes":[], "showAll":false, checkAll: function (argument) {
                        if (!this.showAll) {    
                            for (var j = 0; j < this.envs.length; j++) {
                                
                                if (this.envs[j].show == false) {
                                    $scope.showGroupEnv(true, this.envs[j].name, this.name);
                                    this.envs[j].show = true;
                                }
                            }
                            this.showAll = true;
                        } else {
                            for (var j = 0; j < this.envs.length; j++) {
                                if (this.envs[j].show == true) {
                                    $scope.showGroupEnv(false, this.envs[j].name, this.name);
                                    this.envs[j].show = false;
                                }
                            }
                            this.showAll = false;
                        }
                    }};
                    for (var j=0; j<data.g_environment_list[i].length; j++) {
                        $scope.groups[data.group_list[i]].envs[j] = {"name":data.g_environment_list[i][j], "show":false}
                    }
                }
            });

        };

        $scope.load = function () {
            cesiService.load().then(function (data) {
                $scope.nodeNames = data.node_name_list;
                angular.forEach($scope.nodeNames, function (name) {
                    $scope.checkboxModel[name] = true
                    $scope.reload(name);
                });

            });

        };

        $scope.getNodeLog = function (node, group, name) {
            cesiService.getnodelog(node, group, name).then(function (data) {
                $scope.logs.nodeName = node
                $scope.logs.processName = name
                $scope.logs.logs = data.log
                
                $('#processLogsModal').modal({})
            });
        };

        $scope.showGroupEnv = function (check, env, group) {
            if (check) {
                if ($scope.groups[group].envCount == 0) {
                    $scope.selectedGroups.push(group);
                }
                $scope.groups[group].envCount++;
                cesiService.getenvironmentnodes(group, env).then(function (data) {
                    data = data["process_list"];
                    for (var i = 0; i < data.length; i++) {
                    var found = false;
                        for (var j = 0; j < $scope.groups[group].processes.length; j++) {
                            if ($scope.groups[group].processes[j][1]== data[i][1] && $scope.groups[group].processes[j][2]== data[i][2]) {
                                found = true;
                                $scope.groups[group].processes[j][6].push(env)
                                break;
                            }
                        }

                        if (!found) {
                            data[i][6] = [env]
                            $scope.groups[group].processes.push(data[i])
                        }
                        
                    }
                });
            } else {
                $scope.groups[group].envCount--;
                for (var i=0; i<$scope.groups[group].processes.length; i++) {
                    var pro = $scope.groups[group].processes[i]
                    var index = pro[6].indexOf(env);
                    if (index > -1) {
                        pro[6].splice(index, 1);
                        if (pro[6].length == 0) {
                            $scope.groups[group].processes.splice(i, 1);
                            i -= 1;
                        }
                    }
                }
                if ($scope.groups[group].envCount == 0) {
                    $scope.groups[group].processes = [];
                    var index = $scope.selectedGroups.indexOf(group);
                    if (index > -1) {
                        $scope.selectedGroups.splice(index, 1);
                    }
                }
                
            }
        }


        $scope.reload = function (name) {
            cesiService.reload(name).then(function (data) {
                $scope.nodeMap[name] = data.process_info;
                for (var i = 0; i < data.process_info.length; i++) {
                    $scope.processes[name + ":" + data.process_info[i].name] = data.process_info[i];
                }

                /* example process_info
                    [{
                        "description": "pid 19106, uptime 0:03:49", 
                        "exitstatus": 0, 
                        "group": "test", 
                        "logfile": "/home/cesi/logs/test.out.log", 
                        "name": "test", 
                        "now": 1511430758, 
                        "pid": 19106, 
                        "spawnerr": "", 
                        "start": 1511430529, 
                        "state": 20, 
                        "statename": "RUNNING", 
                        "stderr_logfile": "/home/cesi/logs/test.err.log", 
                        "stdout_logfile": "/home/cesi/logs/test.out.log", 
                        "stop": 1511430527
                    }]*/
            });
        };

        $scope.startAll = function () {
            cesiService.startAll().then($scope.load());
        }

        $scope.stopAll = function () {
            cesiService.stopAll().then($scope.load());
        }

        $scope.restartAll = function () {
            cesiService.restartAll().then($scope.load());
        }

        $scope.restart = function (nodeName, process) {
            setStatus(nodeName, process.name, true);
            cesiService.restart(nodeName, process).then(function (data) {
                updateProcessData(nodeName, process, data)
                setStatus(nodeName, process.name, false);
            });
        };

        $scope.start = function (nodeName, process) {
            setStatus(nodeName, process.name, true);
            cesiService.start(nodeName, process).then(function (data) {
                updateProcessData(nodeName, process, data)
                setStatus(nodeName, process.name, false);
            });
        };

        $scope.stop = function (nodeName, process) {
            setStatus(nodeName, process.name, true);
            cesiService.stop(nodeName, process).then(function (data) {
                updateProcessData(nodeName, process, data)
                setStatus(nodeName, process.name, false);
            });
        };

        function setStatus(nodeName, name, flag) {
            $scope.processStatus[nodeName + "/" + name] = flag;
        }

        function updateProcessData(nodeName, process, data) {
            if (!data || !data.data || !data.data.data) return;

            var node = $scope.nodeMap[nodeName];
            node.forEach(function (val, index) {
                if (val.name == process.name) {
                    node[index] = data.data.data
                    $scope.processes[nodeName + ":" + node[index].name] = node[index]
                }
            })
        }

        //---------------------------------------------

        $scope.getEnvironmentsAndGroups();

        $scope.load();

    }]);