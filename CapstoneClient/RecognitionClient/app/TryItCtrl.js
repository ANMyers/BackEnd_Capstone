"use strict";

app.controller("TryItController", function($scope, $http, $location, RootFactory, apiUrl) {

  $scope.algorithms = ['Nearest Neighbor', 'Test'];
  $scope.excludes = [];
  $scope.variable = [];
  $scope.step1 = true;
  $scope.step2 = false;
  $scope.error = false;
  $scope.renamed = false;
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
        "algorithm": $scope.SelectedAlgo,
        "ignored": $scope.excludes,
        "renamed": renamed_variables
      }
    }).then(
      res => {
        console.log("Data: ", res.data);
      },
      err => {
        console.log("Error: ", err);
      });
  };

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
        $scope.sample_set2 = res.data.sample_set.slice(0);
        $scope.amount = res.data.amount;
      } else {
        $scope.error = true;
        $scope.error_message = "Please Choose a different dataset to match your algorithm.";
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
      if ($scope.SelectedAlgo) {
      format_dataset();
      } else {
        $scope.error = true;
        $scope.error_message = 'Please Choose an Algorithm.';
      }
    };
    if (f) {
      r.readAsBinaryString(f);
    } else {
        $scope.error = true;
        $scope.error_message = 'Please Upload a Dataset.';
    }
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