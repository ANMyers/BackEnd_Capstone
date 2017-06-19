"use strict";

app.controller("MyResultsController", function($scope, $http, RootFactory, apiUrl, TryItFactory, $location) {

    $scope.display = [];
    let data = TryItFactory.getresultsinfo();
    console.log("data after results controller", data);

    for (var key in data.accuracy) {
        for (var name in data.accuracy[key]) {
            let display = [];
            console.log("key: ", name, "value: ", data.accuracy[key][name]);
            display.push(name); 
            display.push(data.accuracy[key][name]);
            $scope.display.push(display);
        }
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