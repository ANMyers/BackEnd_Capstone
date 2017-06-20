"use strict";

app.controller("TryItController", function($scope, $http, $location, RootFactory, apiUrl, TryItFactory) {

  $scope.algorithms = ['Nearest Neighbor', 'Support Vector Classification'];
  $scope.error = false;

  let format_dataset = function() {
    $http({
    url: `${apiUrl}/format_dataset/`,
    method: "POST",
    headers: {
      'Authorization': "Token " + RootFactory.getToken()
    },
    data: {
      "algorithm": $scope.SelectedAlgo,
      "dataset": $scope.dataset,
      "project": $scope.project_name,
      "token": RootFactory.getToken()
    }
  }).then(
    res => {
      console.log("Data: ", res.data);
      $("#LoadingModal").modal("hide");
      if (res.data['continue']) {
        TryItFactory.setsavedinfo(res.data);
        $location.path('/Try_It/My_Project');
      } else {
        $scope.error = true;
        $scope.error_message = res.data.error;
      }
    },
    err => {
      console.log("Error: ", err);
    });
  };

  $scope.step_2 = function(){
    var f = document.getElementById('dataset').files[0],
        r = new FileReader();
    r.onloadend = function(e){
      $scope.dataset = e.target.result;
      if ($scope.SelectedAlgo && $scope.project_name) {
        $("#LoadingModal").modal("show");
        format_dataset();
      } else {
        $scope.error_message = 'Please Choose an Algorithm and a Project Name.';
        $scope.error = true;
      }
    };
    if (f) {
      r.readAsBinaryString(f);
    } else {
        $scope.error = true;
        $scope.error_message = 'Please Upload a Dataset.';
    }
  };



});