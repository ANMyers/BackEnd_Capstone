"use strict";

app.controller('AuthController', function($scope, $http, $location, RootFactory, apiUrl, $timeout) {

  $scope.user = {
    username: "Tavern",
    password: "tavern123",
    email: "bob@bob.com",
    first_name: "adam",
    last_name: "myers"
  };

  $scope.register = function() {
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
            $location.path('/home');
          }
        },
        console.error
      );
  };

  // $timeout($scope.login(), 500);  


});
