'use strict';

app.controller('LogoutCtrl', function($scope, AuthService) {
	AuthService.logout();
});