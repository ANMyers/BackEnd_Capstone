"use strict";

app.controller("MySavedController", function($scope, $http, RootFactory, apiUrl) {

  $scope.my_projects = [];

  $http({
  url: `${apiUrl}/my_saved/`,
  method: "POST",
  headers: {
    'Authorization': "Token " + RootFactory.getToken()
  },
  data: {
    "token": RootFactory.getToken()
  }
  }).then(
    res => {
      console.log("Data: ", res.data);
      $scope.my_projects = res.data.my_saved;
    },
    err => {
      console.log("Error: ", err);
    });

  $scope.project = function(project) {
    
  };

});