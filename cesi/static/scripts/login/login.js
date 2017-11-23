'use strict';

var app = angular.module('login', ['cesiLib']);

app.controller('LoginCtrl', ['$scope', 'cesiService', function ($scope, cesiService) {
  $scope.submit = function () {
    cesiService.login($scope.form).then(function (data) {
      document.getElementById('login-button').disabled = false;
      document.getElementById('login-button').value = "Login";

      switch (data.status) {
        case "success":
          window.location.replace('/');
          break;
        case "warning":
          alert(data.message);
          break;
        default:
          alert('Error!');
          break;
      }
    });

    document.getElementById('login-button').disabled = true;
    document.getElementById('login-button').value = "Please Wait";
  }
}]);