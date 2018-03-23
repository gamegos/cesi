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

        $scope.isAllHidden = true;

        $scope.updateProcesses = (checked, groupName) => 
        Array.from(new Set(Object.keys(checked)
            .filter(envName => 
                checked[envName])
            .map(checkedEnvName =>
                $scope.environments[checkedEnvName].nodes)
            .reduce((a, c) => {
                c.forEach(nodeName => 
                    Object.keys($scope.nodes[nodeName])
                    .map(processName => 
                        $scope.processes[nodeName + ':' + processName])
                    .forEach(process => 
                        process.group === groupName
                        ? a.push(process)
                        : null))
                return a
            }, [])
        ))
        .sort((a, b) =>
            a.node > b.node ? 1 : -1) 

        $scope.getEnvironmentsAndGroups = function () {
            cesiService.dashboard().then(function (data) {
                data.environments.forEach(environmentName => 
                    cesiService.getenvironment(environmentName)
                    .then(environmentData => $scope.environments[environmentName] = environmentData))

                data.groups.forEach(groupName =>                     
                    cesiService.getgroup(groupName)
                    .then(groupData => {
                        console.log(groupData)
                        $scope.groups[groupName] = {
                            processes: [],
                            nodes: [],
                            envs: groupData,
                            checked: Object.keys(groupData).reduce((a, c) => {
                                a[c] = true
                                return a
                            }, {}),                           
                        }
                        $scope.groups[groupName].processes = $scope.updateProcesses($scope.groups[groupName].checked, groupName)

                        console.log($scope.groups)
                    }))

                $scope.nodes = data.processes
                
                Object.keys(data.processes).forEach(nodeName =>
                    Object.keys(data.processes[nodeName]).forEach(processName =>
                        $scope.processes[nodeName + ':' + processName] = data.processes[nodeName][processName]))
            });
        };

        /*

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

        */

        $scope.load = function () {
            cesiService.getNodes().then(function (data) {
                var nodes = []
                Object.keys(data.nodes).forEach( key => 
                    data.nodes[key].forEach(node => nodes.push(node)));
                $scope.nodeNames = nodes
                
                nodes.forEach(function (name) {
                    $scope.checkboxModel[name] = true
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

        $scope.startAllNode = function (nodeName) {
            cesiService.startAllNode(nodeName).then($scope.load());
        };

        $scope.stopAllNode = function (nodeName) {
            cesiService.stopAllNode(nodeName).then($scope.load());
        };

        $scope.restartAllNode = function (nodeName) {
            cesiService.restartAllNode(nodeName).then($scope.load());
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