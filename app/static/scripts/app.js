'use strict';

angular.module('cesiApp', [
        'ui.router',
        'cesiLib',
        'cesiApp.dashboard',
        'cesiApp.nodes',
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
        function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
            $locationProvider.hashPrefix('!');
            $httpProvider.interceptors.push('authInterceptorService');

            //default url
            $urlRouterProvider
                .when('/', '/dashboard')
                .when('', '/dashboard')

        }
    ])
    .filter('secondsToTime', function () {
        function padTime(t) {
            return t < 10 ? "0" + t : t;
        }

        return function (_seconds) {
            if (typeof _seconds !== "number" || _seconds < 0)
                return "00:00:00";

            var hours = Math.floor(_seconds / 3600),
                minutes = Math.floor((_seconds % 3600) / 60),
                seconds = Math.floor(_seconds % 60);

            return padTime(hours) + ":" + padTime(minutes) + ":" + padTime(seconds);
        };
    });