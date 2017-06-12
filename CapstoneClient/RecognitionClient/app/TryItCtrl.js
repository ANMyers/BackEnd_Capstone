"use strict";

app.controller("TryItController", function($scope, $http, $location, RootFactory, apiUrl) {

  $scope.algorithms = ['Nearest Neighbor', 'Test'];

  $scope.validate_compatibilty = function() {
    $http({
    url: `${apiUrl}/validate_compatibilty/`,
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
      console.log("Algoritm: ", $scope.SelectedAlgo);
      console.log("data: ", $scope.dataset);
      $scope.validate_compatibilty();
      } else {
        console.log("Please Choose an Algorithm.");
      }
    };
    if (f) {
      r.readAsBinaryString(f);
    } else {
        console.log("Please Upload a Dataset.");
    }
  };

});