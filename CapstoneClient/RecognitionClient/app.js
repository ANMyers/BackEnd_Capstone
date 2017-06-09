"use strict";
var app = angular.module('Recognition', ['ngRoute']);

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
			.otherwise('/home');
});

app.factory('RootFactory', function($http, apiUrl){
		let secure_token = null;

		return {
			getApiRoot () {
				return $http({
					url: apiUrl,
					headers: {
						'Authorization': "Token " + secure_token
					}
				}).then(res => res.data);
			},
			setToken (token) {
				secure_token = token;
			},
			getToken () {
				return secure_token;
			}
		};
});
