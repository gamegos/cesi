'use strict';

angular.module('cesiApp.dashboard', [
    'ui.router',
    'cesiLib'
  ])

  .config(function ($stateProvider) {
    $stateProvider.state('dashboard', {
      url: '/dashboard',
      controller: 'DashboardCtrl',
      templateUrl: 'static/scripts/nodes/dashboard.html'
    });
  })

  // dashboard.config(['$routeProvider', function($routeProvider) {
  //   $routeProvider
  //   .when('/dashboard', {
  //     templateUrl: 'static/scripts/nodes/dashboard.html',
  //     controller: 'DashboardCtrl'
  //   });
  // }]);

  .controller('DashboardCtrl', ['cesiService', '$scope', '$rootScope', function (cesiService, $scope, $rootScope) {
    $scope.environment = {
      nodeCount: 0,
      processCount: 0
    };
    $scope.nodes = {
      nodeCount: 0,
      connected: 0,
      notConnected: 0
    };
    $scope.process = {
      processCount: 0,
      running: 0,
      stoped: 0
    };

    var refreshButton = document.getElementById('refresh-button');

    $scope.refresh = function () {
      cesiService.dashboard().then(function (data) {
        $scope.environment.nodeCount = data.nodeCount;
        $scope.environment.processCount = data.processInfo.count;
        $scope.nodes.nodeCount = data.nodeCount;
        $scope.nodes.connected = data.nodes.connected.length;
        $scope.nodes.notConnected = data.nodes.not_connected.length;
        $scope.process.processCount = data.processInfo.count;
        $scope.process.running = data.processInfo.running;
        $scope.process.stoped = data.processInfo.count - data.processInfo.running;
        refreshButton.disabled = false;
        //refreshButton.innerHTML = "<strong>Refresh</strong>";
      });

      cesiService.log().then(function (data) {
        if (data['status'] === 'success') {
          $scope.logs = data['log'];
        }
      });

      refreshButton.disabled = true;
      //refreshButton.innerHTML = "Refreshing";
    }

    $scope.refresh();
  }]);