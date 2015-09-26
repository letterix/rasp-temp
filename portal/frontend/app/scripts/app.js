'use strict';
var app = angular.module('app', ['ngRoute', 'ngTable', 'ngTableExport', 'cgBusy', 'ajoslin.promise-tracker', 'ui.bootstrap', 'ng-breadcrumbs', 'angular-loading-bar', 'isteven-multi-select']);


app.config(function ($routeProvider, $provide) {
    $provide.constant('API_PATH', '/api/');
    $provide.constant('LOGIN_PATH', '/login.html');
    $provide.constant('LOGOUT_PATH', '/logout');

    $routeProvider
	.when('/', {
		templateUrl: 'views/default-view.html',
		controller: 'CustomersCtrl',
        label: 'Master'
	})
	.when('/customer/:customer', {
		templateUrl: 'views/default-view.html',
		controller: 'CustomerCtrl',
        label: 'Customer'
	})
    .when('/customer/:customer/edit', {
        templateUrl: 'views/edit-customer-view.html',
        controller: 'EditCustomerCtrl',
        label: 'Configure Customer'
    })
	.when('/customer/:customer/installation/:installation',{
		templateUrl: 'views/default-view.html',
		controller: 'InstallationCtrl',
        label: 'Installation'
	})
    .when('/customer/:customer/installation/:installation/edit',{
        templateUrl: 'views/edit-installation-view.html',
        controller: 'EditInstallationCtrl',
        label: 'Configure Installation'
    })
    .when('/customer/:customer/installation/:installation/controller/:controller',{
        templateUrl: 'views/controller-view.html',
        controller: 'ControllerCtrl',
        label: 'Controller'
    })
    .when('/customer/:customer/installation/:installation/controller/:controller/edit',{
        templateUrl: 'views/edit-controller-view.html',
        controller: 'EditControllerCtrl',
        label: 'Configure Controller'
    })
    .when('/customer/:customer/installation/:installation/controller/:controller/tag/:tag/edit',{
        templateUrl: 'views/edit-tag-view.html',
        controller: 'EditTagCtrl',
        label: 'Configure Tag'
    })
    .when('/users/:customer', {
        templateUrl: 'views/users-view.html',
        controller: 'UsersCtrl',
        label: 'Users'
    })
    .when('/user/:user/edit', {
        templateUrl: 'views/edit-user-view.html',
        controller: 'EditUserCtrl',
        label: 'User'
    })
	.when('/log/:installation',{
		templateUrl: 'views/log-view.html',
		controller: 'LogCtrl'
	})

	.when('/logout', {
		templateUrl: 'views/logout-view.html',
		controller: 'LogoutCtrl'
	})
	.otherwise({redirectTo: '/'});
});

//Makes strings capitalize the first letter.
String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

app.run(function($rootScope, $location, AuthService, BreadcrumbsService) {
    window.scope = $rootScope;
    AuthService.verifySessionAtServer( function() {
        $rootScope.logout = AuthService.logout;
    });

    $rootScope.$on('$routeChangeStart', function(next, current) {
    });
});


function createAdminTabs($rootScope) {
    $rootScope.viewTabs = [
        {
            name: 'Ny..',
            fontawesome: 'fa-plus',
        },
        {
            name: 'Remove..',
            fontawesome: 'fa-minus',
        },
        {
            name: 'Update..',
            fontawesome: 'fa-edit',
        }
    ]
}

function createLogoutTab($rootScope) {
    $rootScope.logoutTab =  {
        name: 'Logga ut',
        url: '#/logout',
        click: 'logout()',
        fontawesome: 'fa-sign-out',
        show:  true
    }
}
