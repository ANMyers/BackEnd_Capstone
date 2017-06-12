"use strict";

app.controller("TryItController", function($scope, $http, $location, RootFactory, apiUrl) {

  $scope.algorithms = ['Nearest Neighbor', 'Test'];

  $scope.validate_compatibilty = function() {
    $http({
    url: `${apiUrl}/validate_compatibilty`,
    method: "POST",
    headers: {
      'Authorization': "Token " + RootFactory.getToken()
    },
    data: {
      "algorithm": $scope.SelectedAlgo,
      "dataset": $scope.dataset
    }
  }).then(
    res => {
      console.log("Data: ", res.data);
    },
    err => {
      console.log("Error: ", err);
    });
  };

  $scope.test = function() {
    if ($scope.SelectedAlgo && $scope.dataset) {
    console.log("Algoritm: ", $scope.SelectedAlgo);
    console.log("dataset: ", $scope.dataset);
    $scope.validate_compatibilty();
    } else {
      console.log("Please Choose an Algorithm and a dataset.");
    }
  };

  $scope.onFileSelect = function(file) {
    $scope.dataset = file;
  };

});