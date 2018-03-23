'use strict'

let version = '/v2'

angular.module('cesiLib', [])
    .factory('cesiService', ['$http', '$q', '$rootScope', function ($http, $q, $rootScope) {
        return {

            dashboard: function () {
                let data = {processes: {}}
                var deferred = $q.defer();
                Promise.all(['/nodes', '/environments', '/groups'].map(path =>
                    $http.get(version + path)))
                .then(function (responses) {
                    var [nodes, environments, groups] = responses
                    data.nodes = nodes.data.nodes;
                    data.environments = environments.data.environments;
                    data.groups = groups.data.groups;
                    return Promise.all(data.nodes.connected.map(node =>
                        $http.get(version + '/nodes/' + node + '/processes')
                    ))
                })
                .then(function (responses) {
                    var processes = responses.forEach((process, index) => 
                        data.processes[data.nodes.connected[index]] = process.data.processes
                    )

                    data.nodeCount = data.nodes.connected.length + data.nodes.not_connected.length
                    data.processInfo = Object.keys(data.processes)
                    .reduce((a, c) => {
                      var n = {...a}
                      Object.keys(data.processes[c]).forEach(process => {
                        if(process.state === 20) n.running++;
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

            changepassword: function (data) {
                var deferred = $q.defer();
                $http({
                        method: 'POST',
                        url: version + '/change/password/' + ($rootScope.username || "") + '/handler',
                        data: $.param(data),
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    })
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            userInfo: function () {
                var deferred = $q.defer();
                $http.get(version + '/userinfo')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            startAllNode: function (nodeName) {
                var deferred = $q.defer();
                $http.get(version + '/nodes/' + nodeName + '/start')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            stopAllNode: function (nodeName) {
                var deferred = $q.defer();
                $http.get(version + '/nodes/' + nodeName + '/stop')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            restartAllNode: function (nodeName) {
                var deferred = $q.defer();
                $http.get(version + '/nodes/' + nodeName + '/restart')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            startAll: function () {
                var deferred = $q.defer();
                $http.get(version + '/node/all/start')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            stopAll: function () {
                var deferred = $q.defer();
                $http.get(version + '/node/all/stop')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            restartAll: function () {
                var deferred = $q.defer();
                $http.get(version + '/node/all/restart')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },


            getNodes: function () {
                var deferred = $q.defer();
                $http.get(version + '/nodes')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            getenvironments: function () {
                var deferred = $q.defer();
                $http.get(version + '/environments')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            getenvironment: function (name) {
                var deferred = $q.defer();
                $http.get(version + '/environments/' + name)
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            getgroup: function (name) {
                var deferred = $q.defer();
                $http.get(version + '/groups/' + name)
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            getnodelog: function (node, group, name) {
                var deferred = $q.defer();
                $http.get(version + '/nodes/' + node + '/process/' + group + ':' + name + '/readlog')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            getusers: function () {
                var deferred = $q.defer();
                $http.get(version + '/delete/user')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            deleteuser: function (username) {
                var deferred = $q.defer();
                $http.get(version + '/delete/user/' + username)
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            log: function () {
                var deferred = $q.defer();
                $http.get(version + '/activitylog')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            reload: function (node) {
                var deferred = $q.defer();
                $http.get(version + '/nodes/' + node)
                    .then(function (response) {

                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            login: function (data) {
                console.log($.param(data));
                var deferred = $q.defer();
                $http({
                        method: 'POST',
                        url: version + '/login/control',
                        data: $.param(data),
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    })
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            add: function (data) {
                console.log($.param(data));
                var deferred = $q.defer();
                $http({
                        method: 'POST',
                        url: version + '/add/user/handler',
                        data: $.param(data),
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    })
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            logout: function () {
                var deferred = $q.defer();
                $http.get('/logout')
                    .then(function (response) {
                        deferred.resolve(response.data);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },


            restart: function (node, process) {
                var deferred = $q.defer();
                $http.get(version + '/nodes/' + node + '/process/' + process.group + ':' + process.name + '/restart')
                    .then(function (response) {
                        deferred.resolve(response);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            start: function (node, process) {
                var deferred = $q.defer();
                $http.get(version + '/nodes/' + node + '/process/' + process.group + ':' + process.name + '/start')
                    .then(function (response) {
                        deferred.resolve(response);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;
            },

            stop: function (node, process) {
                var deferred = $q.defer();
                $http.get(version + '/nodes/' + node + '/process/' + process.group + ':' + process.name + '/stop')
                    .then(function (response) {
                        deferred.resolve(response);
                    })
                    .catch(function (response) {
                        deferred.reject(response);
                    });
                return deferred.promise;

                //return $http.get('http://127.0.0.1:5000/node/srv2/process/'+process.name+':'+process.group+'/stop')
            }
        };


    }])