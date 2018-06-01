'use strict'

let version = '/v2'

angular.module('cesiLib', [])
    .factory('cesiService', ['$http', '$q', '$rootScope', function ($http, $q, $rootScope) {
        let postFormHeaders = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        let service = {
            request: function(method, path, data, headers){
                let deferred = $q.defer();
                let req = {
                    method: method,
                    url: version + path
                }
                if(data) req.data = data;
                if(headers) req.headers = headers;

                $http(req)
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            dashboard: function () {
                let data = {processes: {}}
                let deferred = $q.defer();
                Promise.all(['/nodes', '/environments', '/groups'].map(path => service.request('GET', path)))
                .then(function (responses) {
                    let [nodes, environments, groups] = responses
                    data.nodes = nodes.nodes;
                    data.environments = environments.environments;
                    data.groups = groups.groups;
                    return Promise.all(data.nodes.connected.map(node => service.request('GET', '/nodes/' + node + '/processes')))
                })
                .then(function (responses) {
                    let processes = responses.forEach((process, index) => {
                        data.processes[data.nodes.connected[index]] = process.processes
                    })

                    data.nodeCount = data.nodes.connected.length + data.nodes.not_connected.length
                    data.processInfo = Object.keys(data.processes)
                    .reduce((a, c) => {
                      let n = {...a}
                      Object.keys(data.processes[c]).forEach(processName => {
                        if(data.processes[c][processName].state === 20) n.running++;
                        n.count++;
                      })
                      return n
                    }, {count: 0, running: 0})

                    deferred.resolve(data)
                })
                .catch(function (response) {
                    deferred.reject(response);
                });

                return deferred.promise;
            },

            getprocessdata: function(nodeName, processName){
                return service.request("GET", '/nodes/' + nodeName + '/processes/' + processName)
            },

            changepassword: function (data) {
                let path = '/change/password/' + ($rootScope.username || "") + '/handler'
                return service.request('POST', path, $.param(data), postFormHeaders);
            },

            userInfo: function () {
                return service.request("GET", '/userinfo');
            },

            startAllNode: function (nodeName) {
                return service.request("GET", '/nodes/' + nodeName + '/all-processes/start');
            },

            stopAllNode: function (nodeName) {
                return service.request("GET", '/nodes/' + nodeName + '/all-processes/stop');
            },

            restartAllNode: function (nodeName) {
                return service.request("GET", '/nodes/' + nodeName + '/all-processes/restart');
            },

            startAll: function () {
                return service.request("GET", '/node/all/start');
            },

            stopAll: function () {
                return service.request("GET", '/node/all/stop');
            },

            restartAll: function () {
                return service.request("GET", '/node/all/restart');
            },


            getNodes: function () {
                return service.request("GET", '/nodes');
            },

            getenvironments: function () {
                return service.request("GET", '/environments');
            },

            getenvironment: function (name) {
                return service.request("GET", '/environments/' + name);
            },

            getgroup: function (name) {
                return service.request("GET", '/groups/' + name);
            },

            getnodelog: function (node, group, name) {
                return service.request("GET", '/nodes/' + node + '/processes/' + name + '/log');
            },

            getusers: function () {
                return service.request("GET", '/user');
            },

            deleteuser: function (username) {
                return service.request("GET", '/delete/user/' + username);
            },

            log: function () {
                return service.request("GET", '/activitylog');
            },

            reload: function (node) {
                return service.request("GET", '/nodes/' + node);
            },

            login: function (data) {
                return service.request('POST', '/login/control', $.param(data), postFormHeaders);
            },

            add: function (data) {
                return service.request('POST','/add/user/handler', $.param(data), postFormHeaders);
            },

            logout: function () {
                return service.request("GET", '/logout');
            },

            restart: function (node, process) {
                return service.request("GET", '/nodes/' + node + '/processes/' + process.name + '/restart');
            },

            start: function (node, process) {
                return service.request("GET", '/nodes/' + node + '/processes/' + process.name + '/start');
            },

            stop: function (node, process) {
                return service.request("GET", '/nodes/' + node + '/processes/' + process.name + '/stop');
            }
            
        };

        return service;

    }])