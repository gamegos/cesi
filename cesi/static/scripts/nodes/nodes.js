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

                    }))

                $scope.nodes = data.processes
                
                Object.keys(data.processes).forEach(nodeName =>
                    Object.keys(data.processes[nodeName]).forEach(processName =>
                        $scope.processes[nodeName + ':' + processName] = data.processes[nodeName][processName]))
            });
        };

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
            cesiService.startAllNode(nodeName).then($scope.getEnvironmentsAndGroups());
        };

        $scope.stopAllNode = function (nodeName) {
            cesiService.stopAllNode(nodeName).then($scope.getEnvironmentsAndGroups());
        };

        $scope.restartAllNode = function (nodeName) {
            cesiService.restartAllNode(nodeName).then($scope.getEnvironmentsAndGroups());
        };

        $scope.startAll = function () {
            cesiService.startAll().then($scope.getEnvironmentsAndGroups());
        }

        $scope.stopAll = function () {
            cesiService.stopAll().then($scope.getEnvironmentsAndGroups());
        }

        $scope.restartAll = function () {
            cesiService.restartAll().then($scope.getEnvironmentsAndGroups());
        }

        $scope.restart = function (nodeName, process) {
            setStatus(nodeName, process.name, true);
            cesiService.restart(nodeName, process).then(function () {
                updateProcessData(nodeName, process)
                setStatus(nodeName, process.name, false);
            });
        };

        $scope.start = function (nodeName, process) {
            setStatus(nodeName, process.name, true);
            cesiService.start(nodeName, process).then(function () {
                updateProcessData(nodeName, process)
                setStatus(nodeName, process.name, false);
            });
        };

        $scope.stop = function (nodeName, process) {
            setStatus(nodeName, process.name, true);
            cesiService.stop(nodeName, process).then(function () {
                updateProcessData(nodeName, process)
                setStatus(nodeName, process.name, false);
            });
        };

        function setStatus(nodeName, name, flag) {
            $scope.processStatus[nodeName + "/" + name] = flag;
        }

        function updateProcessData(nodeName, process) {
            cesiService.getprocessdata(nodeName, process.name)
            .then(data => {
                var nodes = {...$scope.nodes}
                nodes[nodeName][process.name] = data
                $scope.nodes = nodes
                var groups = {...$scope.groups}
                groups[process.group].processes.forEach((val, index) => val.name === process.name && val.node === process.node ? groups[process.group].processes[index] = data : null)
                $scope.groups = groups
            })
        }

        //---------------------------------------------

        $scope.getEnvironmentsAndGroups();

        $scope.load();

    }]);