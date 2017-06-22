"use strict";

app.controller("MyResultsController", function($scope, $http, RootFactory, apiUrl, TryItFactory, $location) {

    let data = TryItFactory.getresultsinfo();
    $scope.SelectedAlgo = data.algorithm;
    console.log($scope.SelectedAlgo);
    $scope.display = [];
    $scope.cluster_amount = data.cluster_amount;
    $scope.prediction = [];
    console.log("data after results controller", data);

    if (data.algorithm == "Nearest Neighbor"){
        for (let key in data.accuracy) {
            for (let name in data.accuracy[key]) {
                let display = [];
                display.push(name); 
                display.push(data.accuracy[key][name]);
                display.push(data.centroids[key]); 
                $scope.display.push(display);
            }
        }
    } else if (data.algorithm == "Support Vector Classification") {
        for (let key in data.accuracy) {
            let display = [];
            display.push(key);
            display.push(data.accuracy[key]);
            $scope.display.push(display);
            console.log("SVC??", $scope.display);
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