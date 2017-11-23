'use strict'
angular.module('cesiLib',[])

.factory('cesiService',['$http','$q', '$rootScope', function($http,$q,$rootScope) {
     var host_ip = '';
     var path = '/node/';
     return {

        dashboard : function () {
             var deferred =$q.defer();
             $http.get(host_ip + '/dashboard')
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

         changepassword : function (data) {
             console.log($.param(data));
             console.log(host_ip + 'change/password/' + ($rootScope.username || "") + '/handler')
             var deferred =$q.defer();
             $http({
                method: 'POST',
                url: host_ip + '/change/password/' + ($rootScope.username || "") + '/handler',
                data: $.param(data),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
             })
             .then(function (response) {
                deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

        userInfo : function () {
             var deferred =$q.defer();
             $http.get(host_ip + '/userinfo')
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

        startAll : function () {
             var deferred =$q.defer();
             $http.get(host_ip + '/node/all/start')
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

        stopAll : function () {
             var deferred =$q.defer();
             $http.get(host_ip + '/node/all/stop')
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

        restartAll : function () {
             var deferred =$q.defer();
             $http.get(host_ip + '/node/all/restart')
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

         getusers : function () {
             var deferred =$q.defer();
             $http.get(host_ip + '/delete/user')
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

        deleteuser : function (username) {
             var deferred =$q.defer();
             $http.get(host_ip + '/delete/user/' + username)
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

         log : function () {
             var deferred =$q.defer();
             $http.get(host_ip + '/activitylog')
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

         reload : function (node) {
             var deferred =$q.defer();
             $http.get(path+node)
             .then(function (response) {

                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

         login : function (data) {
            console.log($.param(data));
             var deferred =$q.defer();
             $http({
                method: 'POST',
                url: host_ip + '/login/control',
                data: $.param(data),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
             })
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

         add : function (data) {
            console.log($.param(data));
             var deferred =$q.defer();
             $http({
                method: 'POST',
                url: host_ip + '/add/user/handler',
                data: $.param(data),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
             })
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

         logout : function () {
             var deferred =$q.defer();
             $http.get(host_ip + '/logout')
             .then(function (response) {
                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },

         load : function () {
             var deferred =$q.defer();
             $http.get(path+'name/list')
             .then(function (response) {


                 deferred.resolve(response.data);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return  deferred.promise;
         },


         restart : function (node,process) {
             var deferred =$q.defer();
             $http.get(path+node+'/process/'+process.name+':'+process.group+'/restart')
             .then(function (response) {
                deferred.resolve(response);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return deferred.promise;
         },
         
         start : function (node,process) {
             var deferred =$q.defer();
             $http.get(path+node+'/process/'+process.name+':'+process.group+'/start')
             .then(function (response) {
                deferred.resolve(response);
             })
             .catch(function (response) {
                 deferred.reject(response);
             });
             return deferred.promise;
         },

         stop : function (node,process) {
             var deferred =$q.defer();
             $http.get(path+node+'/process/'+process.name+':'+process.group+'/stop')
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
