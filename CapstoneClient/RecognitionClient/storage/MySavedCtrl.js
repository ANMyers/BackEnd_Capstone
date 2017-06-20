"use strict";

app.controller("MySavedController", function($scope, $http, RootFactory, apiUrl, TryItFactory, $location) {

  $scope.my_projects = [];

  let load_data = function(){
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
      if (res.data['continue']) {
        console.log("Data: ", res.data);
        $scope.my_projects = res.data.my_saved;
      } else {
        $scope.error = true;
        $scope.error_message = res.data.error;
      }
    },
    err => {
      console.log("Error: ", err);
    });
  };

  $scope.project = function(project) {
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

    $scope.delete_project = function(project) {
    $http({
    url: `${apiUrl}/delete_project/`,
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
        load_data();
      },
      err => {
        console.log("Error: ", err);
      });
    };

    load_data();

});