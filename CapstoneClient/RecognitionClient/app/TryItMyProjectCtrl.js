"use strict";

app.controller("MyProjectController", function($scope, $http, RootFactory, apiUrl, TryItFactory) {

  let data = TryItFactory.getsavedinfo();
  $scope.step1 = false;
  $scope.step2 = true;
  $scope.error = false;
  $scope.SelectedAlgo = data.algorithm;
  $scope.variables = data.indexs;
  $scope.sample_set = data.sample_set;
  $scope.sample_set2 = data.sample_set.slice(0);
  $scope.amount = data.amount;


  let run_kmeans = function() {
    $http({
    url: `${apiUrl}/kmeans/`,
    method: "POST",
    headers: {
      'Authorization': "Token " + RootFactory.getToken()
    },
    data: {
      "algorithm": $scope.SelectedAlgo,
      "project": $scope.project_name,
      "ignored": $scope.excludes,
      "renamed": renamed_variables,
      "token": RootFactory.getToken()
    }
    }).then(
      res => {
        console.log("Data: ", res.data);
      },
      err => {
        console.log("Error: ", err);
      });
  };

});