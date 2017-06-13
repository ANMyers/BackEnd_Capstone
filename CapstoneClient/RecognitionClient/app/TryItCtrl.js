"use strict";

app.controller("TryItController", function($scope, $http, $location, RootFactory, apiUrl) {

  $scope.algorithms = ['Nearest Neighbor', 'Test'];

  let validate_compatibilty = function() {
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
    },
    err => {
      console.log("Error: ", err);
    });
  };

  $scope.test = function(){
    var f = document.getElementById('dataset').files[0],
        r = new FileReader();
    r.onloadend = function(e){
      $scope.dataset = e.target.result;
      if ($scope.SelectedAlgo) {
      validate_compatibilty();
      } else {
        // This needs to update the html page (through binding) to show the user what they must do
        console.log("Please Choose an Algorithm.");
      }
    };
    if (f) {
      r.readAsBinaryString(f);
    } else {
        // This needs to update the html page (through binding) to show the user what they must do
        console.log("Please Upload a Dataset.");
    }
  };

});