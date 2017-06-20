"use strict";

app.controller("MyResultsController", function($scope, $http, RootFactory, apiUrl, TryItFactory, $location) {

    let data = TryItFactory.getresultsinfo();
    $scope.display = [];
    $scope.cluster_amount = data.cluster_amount;
    $scope.prediction = [];
    console.log("data after results controller", data);

    for (let key in data.accuracy) {
        for (let name in data.accuracy[key]) {
            let display = [];
            display.push(name); 
            display.push(data.accuracy[key][name]);
            display.push(data.centroids[key]); 
            $scope.display.push(display);
        }
    }

    for (let pred in data.results) {
        $scope.prediction.push(data.results[pred]);
    }

    $scope.back = function() {
        $http({
        url: `${apiUrl}/my_project/`,
        method: "POST",
        headers: {
          'Authorization': "Token " + RootFactory.getToken()
        },
        data: {
          "token": RootFactory.getToken(),
          "project": data.project
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