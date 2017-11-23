'use strict';

angular.module('cesiApp.nodes', [
        'ui.router',
        'cesiLib'
    ])

    .config(function ($stateProvider) {
        $stateProvider.state('nodes', {
            url: '/nodes',
            controller: 'NodesCtrl',
            templateUrl: 'static/scripts/nodes/nodes.html'
        });
    })


    .controller('NodesCtrl', ['$scope', 'cesiService', function ($scope, cesiService) {
        $scope.nodeMenu = []

        $scope.nodeNames = [];
        $scope.nodeMap = {};

        $scope.processStatus = {};

        $scope.environments = [];
        $scope.groups = [];


        $scope.load = function () {
            cesiService.load().then(function (data) {
                $scope.nodeNames = data.node_name_list;
                angular.forEach($scope.nodeNames, function (name) {
                    $scope.reload(name);
                });

            });

        };


        $scope.reload = function (name) {
            cesiService.reload(name).then(function (data) {
                $scope.nodeMap[name] = data.process_info;

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
            setStatus(nodeName, process.pid, true);
            cesiService.restart(nodeName, process).then(function (data) {
                updateProcessData(nodeName, process, data)
                setStatus(nodeName, process.pid, false);
            });
        };

        $scope.start = function (nodeName, process) {
            setStatus(nodeName, process.pid, true);
            cesiService.start(nodeName, process).then(function (data) {
                updateProcessData(nodeName, process, data)
                setStatus(nodeName, process.pid, true);
            });
        };

        $scope.stop = function (nodeName, process) {
            setStatus(nodeName, process.pid, true);
            cesiService.stop(nodeName, process).then(function (data) {
                updateProcessData(nodeName, process, data)
                setStatus(nodeName, process.pid, true);
            });
        };

        function setStatus(nodeName, pid, flag) {
            $scope.processStatus[nodeName + "/" + pid] = flag;
        }

        function updateProcessData(nodeName, process, data) {
            if (!data || !data.data || !data.data.data) return;

            var node = $scope.nodeMap[nodeName];
            node.forEach(function (val, index) {
                if (val.pid == process.pid) {
                    node[index] = data.data.data
                }
            })
        }

        //---------------------------------------------

        $scope.load();

    }]);