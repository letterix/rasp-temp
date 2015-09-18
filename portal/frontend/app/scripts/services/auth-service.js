'use strict';

app.service('AuthService', function($location, $rootScope, $http, api, SessionService, LOGIN_PATH, LOGOUT_PATH) {

	function cachSession(user) {
		SessionService.set('authenticated', true);
		SessionService.set('role', user.role);
		SessionService.set('user', angular.toJson(user));
		SessionService.set('lang', user.lang);
	}

	function uncacheSession() {
		SessionService.unset('authenticated');
		SessionService.unset('role');
		SessionService.unset('user');
		SessionService.unset('lang');
	}

	function getUser() {
		return angular.fromJson(SessionService.get('user'));
	}

  function getCustomers() {
  	return getUser().customers
  }

	function toLogin() {
		window.location = LOGIN_PATH;
	}
	function toLogout() {
		window.location = LOGOUT_PATH;
	}

	function isNormal() {
    switch (SessionService.get('role')) {
      case "admin":
          return true
      case "user":
          return true
    }
    return false
  }


  function isAdmin(){
    switch (SessionService.get('role')) {
      case "admin":
          return true
      case "master_admin":
          return true
      case "super_user":
          return true
    }
    return false
  }


  function isMaster() {
    switch (SessionService.get('role')) {
      case "master_user":
          return true
      case "master_admin":
          return true
      case "super_user":
          return true
    }
    return false
  }


  function isSuper() {
    switch (SessionService.get('role')) {
      case "master_admin":
          return true
      case "super_user":
          return true
    }
    return false
  }

  function isAssignedMaster() {
  	return getCustomers().indexOf(1) > -1
  }

  function isAssignedCustomer(customer){
    var id = parseInt(customer)
  	return getCustomers().indexOf(id) > -1
  }


	this.verifySessionAtServer = function(callback) {
		api.get('session', function(user) {
			cachSession(user);
			if(typeof callback == 'function') {
				callback();
			}
			return true;

		}, function() {
			uncacheSession();
			toLogin();
			return false;
		});
	};

	this.toLogin = function() {
		toLogin()
	};

	this.logout = function() {
		uncacheSession();
		toLogout();
	};

	this.isOnline = function() {
		return SessionService.get('authenticated') == "true";
	};

	this.isNormal = function() {
		return this.isOnline() && isNormal();
	};

	this.isAdmin = function() {
		return this.isOnline() && isAdmin();
	};

	this.isMaster = function() {
		return this.isOnline() && isMaster();
	};

	this.isSuper = function() {
		return this.isOnline() && isSuper();
	};

	this.getUser = function() {
		return getUser();
	};

	this.canViewCustomer = function(customer) {
		if(customer){
			// Single Customer
			return isSuper() || isAssignedMaster() || isAssignedCustomer(customer)
		}else{
			// Multiple Customers
			return isMaster()
		}
	}

	this.canEditCustomer = function(customer) {
		if(customer){
			// Single Customer
			return isSuper() || isAssignedMaster() || (isAssignedCustomer(customer) && (isAdmin() || isMaster()))
		}else{
			// Multiple Customers
			return isMaster()
		}
	}


});