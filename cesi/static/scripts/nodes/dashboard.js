'use strict';

angular.module('cesiApp.dashboard', [
    'ui.router', 
    'cesiLib'
  ])

  .config(function($stateProvider) {
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

  .controller('DashboardCtrl', ['cesiService', '$scope', '$rootScope', function(cesiService, $scope, $rootScope) {
    $scope.environment = {nodeCount:0, processCount:0};
    $scope.nodes = {nodeCount:0, connected:0, notConnected:0};
    $scope.process = {processCount:0, running:0, stoped:0};

    var refreshButton = document.getElementById('refresh-button');

    $scope.refresh = function () {
        cesiService.dashboard().then(function (data) {
        $scope.environment.nodeCount = data['node_count'];
        $scope.environment.processCount = data['all_process_count'];
        $scope.nodes.nodeCount = data['node_count'];
        $scope.nodes.connected = data['connected_count'];
        $scope.nodes.notConnected = data['not_connected_count'];
        $scope.process.processCount = data['all_process_count'];
        $scope.process.running = data['running_process_count'];
        $scope.process.stoped = data['stopped_process_count'];
        refreshButton.disabled = false;
        refreshButton.innerHTML = "<strong>Refresh</strong>";
      });

      cesiService.log().then(function (data) {
        if (data['status'] === 'success') {
          $scope.logs = data['log'];
        }
      });

      refreshButton.disabled = true;
      refreshButton.innerHTML = "Refreshing";
    }

    $scope.refresh();
  }]);