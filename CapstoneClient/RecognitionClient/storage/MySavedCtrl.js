"use strict";

app.controller("MySavedController", function($scope, $http, RootFactory, apiUrl, TryItFactory, $location) {

  $scope.my_projects = [];

  $http({
  url: `${apiUrl}/my_saved/`,
  method: "POST",
  headers: {
    'Authorization': "Token " + RootFactory.getToken()
  },
  data: {
    "token": RootFactory.getToken(),
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
    console.log("hello she fired");
    $http({
    url: `${apiUrl}/my_project/`,
    method: "POST",
    headers: {
      'Authorization': "Token " + RootFactory.getToken()
    },
    data: {
      "token": RootFactory.getToken(),
      "project": project
    }
    }).then(
      res => {
        console.log("Data: ", res.data);
        TryItFactory.setsavedinfo(res.data);
        $location.path('/Try_It/My_Project');
      },
      err => {
        console.log("Error: ", err);
      });
    };

});