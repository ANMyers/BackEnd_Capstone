"use strict";

app.controller('AuthController', function($scope, $http, $location, RootFactory, apiUrl) {
  $scope.loggedin = false;

  $scope.user = {
    username: "Tavern",
    password: "tavern123",
    email: "bob@bob.com",
    first_name: "adam",
    last_name: "myers"
  };

  $scope.register = function() {
    let user_info = {
      "username": $scope.user.username,
      "password": $scope.user.password,
      "email": $scope.user.email,
      "first_name": $scope.user.first_name,
      "last_name": $scope.user.last_name
    };
    console.log(user_info);
      $http({
        url: `${apiUrl}/register`,
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        data: {
          "username": $scope.user.username,
          "password": $scope.user.password,
          "email": $scope.user.email,
          "first_name": $scope.user.first_name,
          "last_name": $scope.user.last_name
        }
      }).then(
        res => {
          RootFactory.setToken(res.data.token);
          if (res.data.token !== "") {
            $scope.loggedin = true;
            $("#RegisterModal").modal("hide");
            $location.path('/home');
          }
        },
        console.error
      );
  };

  $scope.login = function() {
      $http({
        url: `${apiUrl}/api-token-auth/`,
        method: "POST",
        data: {
          "username": $scope.user.username,
          "password": $scope.user.password
        }
      }).then(
        res => {
          RootFactory.setToken(res.data.token);
          if (res.data.token !== "") {
            $scope.loggedin = true;
            $("#LoginModal").modal("hide");
            $location.path('/home');
          }
        },
        console.error
      );
  };

  $scope.logout = function() {
      
    RootFactory.setToken("");
      $scope.loggedin = false;
      $("#LogoutModal").modal("show");
      $location.path('/home');

  };


});
