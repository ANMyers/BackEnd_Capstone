"use strict";

app.controller("TryItController", function($scope, $http, $location, RootFactory, apiUrl) {

  $scope.algorithms = ['Nearest Neighbor', 'Test'];
  $scope.step1 = true;
  $scope.step2 = false;
  $scope.error = false;
  $scope.variable = [];

  let format_dataset = function() {
    $http({
    url: `${apiUrl}/format_dataset/`,
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
      if (res.data['continue']) {
      $scope.step1 = false;
      $scope.step2 = true;
      $scope.error = false;
      $scope.variables = res.data.indexs;
      $scope.sample_set = res.data.sample_set;
      } else {
      $scope.error = true;
      $scope.error_message = "Please Choose a different dataset to match your algorithm.";
      }
    },
    err => {
      console.log("Error: ", err);
    });
  };

  $scope.step_1 = function(){
    var f = document.getElementById('dataset').files[0],
        r = new FileReader();
    r.onloadend = function(e){
      $scope.dataset = e.target.result;
      if ($scope.SelectedAlgo) {
      format_dataset();
      } else {
        // This needs to update the html page (through binding) to show the user what they must do
        $scope.error = true;
        $scope.error_message = 'Please Choose an Algorithm.';
      }
    };
    if (f) {
      r.readAsBinaryString(f);
    } else {
        // This needs to update the html page (through binding) to show the user what they must do
        $scope.error = true;
        $scope.error_message = 'Please Upload a Dataset.';
    }
  };

  $scope.step_2 = function() {

  };

});