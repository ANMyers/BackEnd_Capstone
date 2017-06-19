"use strict";

app.controller("MyProjectController", function($scope, $http, RootFactory, apiUrl, TryItFactory, $location) {

  let data = TryItFactory.getsavedinfo();
  $scope.SelectedAlgo = data.algorithm;
  $scope.variables = data.indexs;
  $scope.sample_set = data.sample_set;
  $scope.sample_set2 = data.sample_set.slice(0);
  $scope.amount = data.amount;

  $scope.excludes = [];
  $scope.error = false;
  $scope.renamed = false;
  $scope.renamed_each = {};
  $scope.train_values_set = false;

  let renamed_variables = [];

  let run_kmeans = function() {
    $http({
    url: `${apiUrl}/kmeans/`,
    method: "POST",
    headers: {
      'Authorization': "Token " + RootFactory.getToken()
    },
    data: {
      "algorithm": data.algorithm,
      "project": data.project,
      "ignored": $scope.excludes,
      "renamed": renamed_variables,
      "train_on": $scope.train_on,
      "train_against": $scope.train_against,
      "token": RootFactory.getToken()
    }
    }).then(
      res => {
        console.log("Data: ", res.data);
        TryItFactory.setresultsinfo(res.data);
        $location.path('/Try_It/My_Results');
      },
      err => {
        console.log("Error: ", err);
      });
  };

    $scope.step_3 = function() {
    $scope.save_training();
    if ($scope.train_values_set === false) {
      $scope.error = true;
      $scope.error_message = "Please Set the Values you want to train on and train against.";
    } else if ($scope.renamed === false) {
      $scope.error = true;
      $scope.error_message = "Please Rename all variables listed on the right and remember to exclude any variables you don't need.";
    } else {
      $scope.error = false;
      if ($scope.SelectedAlgo == 'Nearest Neighbor') {
        run_kmeans();
      }
    }
  };

  $scope.variables_to_exclude = function(exclude_me) {
    let variable_index2 = $scope.sample_set2.indexOf(exclude_me);
    let excluded = {
      'index': variable_index2,
      'value': $scope.sample_set2[variable_index2]
    };
    $scope.excludes.push(excluded);
    $scope.sample_set.splice($scope.sample_set.indexOf(exclude_me), 1);
  };

  $scope.rename_value = function(v1) {
    let name = document.getElementById(v1[1]).value;
    let renamed = {
      'index': v1[0],
      'value': v1[1],
      'renamed': name
    };
    check_if_variable_is_already_named(renamed);
    check_if_variables_are_named();
    console.log(renamed_variables);
  };

  let check_if_variable_is_already_named = function(variable) {
    let has_been_named = false;
    for (var i = 0; i < renamed_variables.length; i++) {
      if (renamed_variables[i].index == variable.index && renamed_variables[i].value == variable.value) {
        renamed_variables[i].renamed = variable.renamed;
        has_been_named = true;
      }
    }
    if (has_been_named === false) {
      renamed_variables.push(variable);
    }
  };

  let check_if_variables_are_named = function () {
    if (renamed_variables.length == $scope.variables.length) {
      $scope.renamed = true;
    } else {
      $scope.renamed = false;
    }
  };

  $scope.variables_to_undo = function(undo_me) {
    let index_value = $scope.excludes.indexOf(undo_me);
    $scope.excludes.splice(index_value, 1);
    $scope.sample_set = $scope.sample_set2.slice(0);

    for (var i = 0; i < $scope.excludes.length; i++) {
      let index = $scope.sample_set.indexOf($scope.excludes[i].value);
      $scope.sample_set.splice(index, 1);
    }
  };

  $scope.save_training = function() {
    if ($scope.train_on <= 0 || $scope.train_on === null || $scope.train_on === undefined) {
      $scope.train = true;
      $scope.train_message = `Quantity to train on Must be higher than 0`; 
      $scope.train_values_set = false;
    } else if ($scope.train_against <= 0 || $scope.train_against === null || $scope.train_against === undefined) {
      $scope.train = true;
      $scope.train_message = `Quantity to against Must be higher than 0`;
      $scope.train_values_set = false; 
    } else if ($scope.train_on > $scope.amount){
      $scope.train = true;
      $scope.train_message = `Quantity to train on Must be lower than total quantity of ${$scope.amount}`;
      $scope.train_values_set = false; 
    } else if ($scope.train_against > $scope.amount - $scope.train_on) {
      $scope.train = true;
      $scope.train_message = `Quantity to train against Must be lower than total quantity (${$scope.amount}) minus quantity to train on (${$scope.train_on}) ( hint: lower than ${$scope.amount - $scope.train_on} )`;
      $scope.train_values_set = false;
    } else {
      $scope.train = false;
      $scope.train_message = "";
      $scope.train_values_set = true;
    }
  };

});