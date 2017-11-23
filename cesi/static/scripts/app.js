'use strict';

angular.module('cesiApp', [
    'ui.router',
    'cesiLib',
    // 'ngTable',
    'cesiApp.dashboard',
    'cesiApp.nodes',
    // 'myApp.groups',
    'cesiApp.navbar'
])
.factory('authInterceptorService', ['$q', '$location', function ($q, $location) {
    var responseError = function (rejection) {
        if (rejection.status === 403) {
            window.location.replace('/login');
        }
        return $q.reject(rejection);
    };

    return {
        responseError: responseError
    };
}])
.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', '$httpProvider', 
    function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
        $locationProvider.hashPrefix('!');
        $httpProvider.interceptors.push('authInterceptorService');

        //default url
        $urlRouterProvider
            .when('/', '/dashboard')
            .when('', '/dashboard')
    
    }])

