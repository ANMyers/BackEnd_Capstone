"use strict";
var app = angular.module('Recognition', ['ngRoute', 'ngFileUpload']);

app.constant('apiUrl', "http://localhost:8000");

app.config(function($interpolateProvider, $routeProvider){

		$interpolateProvider.startSymbol('((');
		$interpolateProvider.endSymbol('))');

		$routeProvider
			.when('/home', {
				controller: 'HomeController',
				templateUrl: 'RecognitionClient/splash/home.html'
			})
			.when('/register', {
				controller: 'AuthController',
				templateUrl: 'RecognitionClient/auth/register.html'
			})
			.when('/login', {
				controller: 'AuthController',
				templateUrl: 'RecognitionClient/auth/login.html'
			})
			.when('/logout', {
				controller: 'AuthController',
				templateUrl: 'RecognitionClient/auth/logout.html'
			})
			.when('/About', {
				controller: 'AboutController',
				templateUrl: 'RecognitionClient/info/about.html'
			})
			.when('/Algorithms', {
				controller: 'AlgorithmsController',
				templateUrl: 'RecognitionClient/info/algorithms.html'
			})
			.when('/Try_It', {
				controller: 'TryItController',
				templateUrl: 'RecognitionClient/app/tryit.html'
			})
			.when('/My_Saved', {
				controller: 'MySavedController',
				templateUrl: 'RecognitionClient/storage/mysaved.html'
			})
			.otherwise('/home');
});
