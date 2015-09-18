'use strict';

app.service('BreadcrumbsService', function($rootScope, SessionService, breadcrumbs) {

  $rootScope.breadcrumbs = breadcrumbs

  function initOptions() {
    if(!$rootScope.breadcrumbs.options){
      $rootScope.breadcrumbs.options = {}
    }
  }

  function cacheCustomer(customer) {
    SessionService.set('customer', angular.toJson(customer));
  }

  function uncacheCustomer() {
    SessionService.unset('customer');
  }

  function cacheInstallation(installation) {
    SessionService.set('installation', angular.toJson(installation));
  }

  function uncacheInstallation() {
    SessionService.unset('installation');
  }

  function cacheController(controller) {
    SessionService.set('controller', angular.toJson(controller));
  }

  function uncacheController() {
    SessionService.unset('controller');
  }

  function getCustomer() {
    return angular.fromJson(SessionService.get('customer'));
  };

  function getInstallation() {
    return angular.fromJson(SessionService.get('installation'));
  };

  function getController() {
    return angular.fromJson(SessionService.get('controller'));
  };

  function buildCustomerCrumb() {
    var customer = getCustomer()
    if(customer){
      $rootScope.breadcrumbs.options['Customer'] = customer.name
    }
  }

  function buildInstallationCrumb() {
    var installation = getInstallation()
    if(installation){
      $rootScope.breadcrumbs.options['Installation'] = installation.name
    }
  }

  function buildControllerCrumb() {
    var controller = getController()
    if(controller){
      $rootScope.breadcrumbs.options['Controller'] = controller.name
    }
  }

  this.buildBreadcrumbs = function() {
    initOptions()
    buildCustomerCrumb()
    buildInstallationCrumb()
    buildControllerCrumb()
    $rootScope.breadcrumbs.generateBreadcrumbs()
  }

  this.setCustomer = function(customer) {
    var old = getCustomer()
    if(old){
      uncacheCustomer()
    }
    cacheCustomer(customer)
  }

  this.setInstallation = function(installation) {
    var old = getInstallation()
    if(old){
      uncacheInstallation()
    }
    cacheInstallation(installation)
  }

  this.setController = function(controller) {
    var old = getController()
    if(old){
      uncacheController()
    }
    cacheController(controller)
  }
});