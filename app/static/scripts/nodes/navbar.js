'use strict';

function notify($scope, type, message) {
  $scope.notifTitle = type
  $scope.message = message
  $scope.alertType = "alert-" + type
};

function findType(type) {
  type = type + ""
  switch (type) {
    case '0':
      return "Admin"
      break;
    case '1':
      return "Standart User"
      break;
    case '2':
      return "Only Log"
      break;
    case '3':
      return "Read Only"
      break;
    default:
      return "Unknown"
      break;
  }
}

angular.module('cesiApp.navbar', [
    'ui.router',
    'cesiLib'
  ])

  .config(function ($stateProvider) {
    $stateProvider.state('users/add', {
      url: '/users/add',
      templateUrl: 'static/scripts/nodes/addUser.html',
      controller: 'AddUserCtrl'
    });

    $stateProvider.state('users/password', {
      url: '/users/password',
      templateUrl: 'static/scripts/nodes/changePassword.html',
      controller: 'ChangePasswordCtrl'
    });

    $stateProvider.state('users/delete', {
      url: '/users/delete',
      templateUrl: 'static/scripts/nodes/deleteUser.html',
      controller: 'DeleteUserCtrl'
    });

  })

  .controller('NavbarCtrl', ['$scope', 'cesiService', '$rootScope', function ($scope, cesiService, $rootScope) {
    cesiService.userInfo().then(function (data) {
      $rootScope.username = data['username'];
      $rootScope.usertype = findType(data['usertypecode']);
    });

    $scope.userLogout = function(){
      cesiService.logout().then(function(res, err){
        window.location.replace('/login');
      })
    }
  }])

  .controller('AddUserCtrl', ['$scope', 'cesiService', function ($scope, cesiService) {
    $scope.submit = function () {
      cesiService.add($scope.form).then(function (data) {
        $scope.loading = true

        switch (data.status) {
          case "success":
            notify($scope, "success", data.message);
            document.getElementById("add-user-form").reset();
            break;
          case "warning":
            notify($scope, "warning", data.message);
            break;
          case "error":
            notify($scope, "danger", data.message);
            break;
          default:
            notify($scope, "danger", "Undefined error! " +  data.message);
            break;
        }

      });
    };
  }])

  .controller('ChangePasswordCtrl', ['$scope', 'cesiService', function ($scope, cesiService) {
    $scope.submit = function () {
      $scope.loading = true
      cesiService.changepassword($scope.form).then(function (data) {
        $scope.loading = false
        switch (data.status) {
          case "success":
            notify($scope, "success", "Password Has Been changed");
            break;
          case "error":
            notify($scope, "danger", data.message);
            break;
          default:
            notify($scope, "danger", "Undefined error! " +  data.message);
            break;
        }

        document.getElementById("change-password-form").reset();
      });

    };
  }])

  .controller('DeleteUserCtrl', ['$scope', 'cesiService', function ($scope, cesiService) {
    $scope.users = [];

    $scope.refresh = function () {
      cesiService.getusers().then(function (data) {
        $scope.users = [];
        for (var i = 0; i < data['names'].length; i++) {
          $scope.users.push({
            name: data['names'][i],
            type: findType(data['types'][i])
          })
        }

      });
    };

    $scope.deleteUser = function (arg) {
      cesiService.deleteuser(arg).then(function (data) {
        switch (data.status) {
          case "success":
            notify($scope, "success", "User '" + arg + "' is Deleted");
            $scope.refresh();
            break;
          case "error":
            notify($scope, "danger", data.message);
            break;
          default:
            notify($scope, "danger", "Error!");
            break;
        }
      });
    };

    $scope.refresh();
  }])
 