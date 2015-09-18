app.controller('InstallationCtrl', function($scope, $location, $filter, api, utils, ngTableParams, $routeParams, BreadcrumbsService, $route, $interval, AuthService) {
	window.scope = $scope;
	$scope.titel = "Installation";
	$scope.editing = false;
	$scope.filteredItems = [];
  $scope.currentPage = 0;
  $scope.numPerPage = 6;
  $scope.alarms = 0;
  $scope.warnings = 0;
  $scope.normals = 0;
  $scope.items = []
  $scope.sorting = "alarms"

  // -- AUTHENTICATION AND ACCESSABILITY --

  $scope.canView = function() {
    return AuthService.canViewCustomer($routeParams.customer)
  }

  $scope.canEdit = function() {
    return AuthService.canEditCustomer($routeParams.customer)
  }

  $scope.canCreate = function() {
    return $scope.canEdit()
  }

  $scope.isMaster = function(){
    return AuthService.isMaster()
  }

  $scope.checkAuthority = function() {
    if(!$scope.canView()){
      api.get('customer', function(result) {
        window.location = "/index.html#/customer/" + result[0].id;
      })
    }
  }

  // redirect if cant view
  AuthService.verifySessionAtServer($scope.checkAuthority)

  // -- END OF AUTHENTICATION AND ACCESSABILITY --

  // -- API CHAIN --
  $scope.getItem = function() {
    api.get('installation/' + $routeParams.installation, function(result){
      $scope.currentItem = result;
      $scope.title = $scope.currentItem.name;
      BreadcrumbsService.setInstallation(result)
      BreadcrumbsService.buildBreadcrumbs()
      $scope.getItems()
    });
  }

  $scope.getItems = function() {
    api.get('controllers/' + $routeParams.installation, function(result) {
      $scope.items = result.controllers;
      $scope.setUpItems();
    });
  }

  $scope.setUpItems = function() {
    $scope.alarms = 0;
    $scope.warnings = 0;
    $scope.normals = 0;
    $scope.items.forEach(function(item) {
      item.paragraph = item.ip;
      if(item.alarms){
        $scope.alarms++;
      }
      if(item.warnings){
        $scope.warnings++;
      }
      if(!(item.warnings + item.alarms)){
        $scope.normals++;
      }
    })
    $scope.sortBy($scope.sorting);
    $scope.$$phase || $scope.$apply();
  }
  // -- END API CHAIN --

	$scope.numPages = function () {
	    return Math.ceil($scope.items.length / $scope.numPerPage);
	};

	$scope.viewItem = function(item){
		window.location = "/index.html#/customer/" + $routeParams.customer + "/installation/" + $routeParams.installation + "/controller/" + item.ip;
	};

	$scope.firstBy = utils.firstBy;

	$scope.next = function() {
		if($scope.currentPage < $scope.numPages()-1){
			$scope.currentPage++;
		}
	};

	$scope.previous = function() {
		if($scope.currentPage > 0){
			$scope.currentPage--;
		}
	};

	$scope.toggleEditing = function() {
		$scope.editing = !$scope.editing;
		$scope.toggleCogDropdown();
	}

	$scope.deleteItem = function(item) {
    api.get("controller/" + $routeParams.installation + "?controller_ip=" + item.ip, function(result) {
      //success
      $route.reload();
    });
	}

	$scope.editItem = function(item) {
		window.location = "/index.html#/customer/" + $routeParams.customer + "/installation/" + $routeParams.installation + "/controller/" + item.ip + "/edit";
	}

	$scope.newItem = function() {
		window.location = "/index.html#/customer/" + $routeParams.customer + "/installation/" + $routeParams.installation + "/controller/new/edit";
	}

	$scope.viewUsers = function() {
    window.location = "/index.html#/users/" + $routeParams.customer;
  }

  $scope.sortBy = function(string) {
    switch(string) {
      case 'alarms':
        $scope.items.sort($scope.firstBy(function(a, b) {
          return b.alarms - a.alarms;
        }).thenBy(function(a, b){
          return b.warnings - a.warnings;
        }).thenBy(function(a, b){
          return b.connected - a.connected;
        }).thenBy(function(a, b){
          return a.name - b.name;
        }));
        break;
      case 'warnings':
        $scope.items.sort($scope.firstBy(function(a, b) {
          return b.warnings - a.warnings;
        }).thenBy(function(a, b){
          return b.alarms - a.alarms;
        }).thenBy(function(a, b){
          return b.connected - a.connected;
        }).thenBy(function(a, b){
          return a.name - b.name;
        }));
        break;
      case 'normal':
        $scope.items.sort($scope.firstBy(function(a, b) {
          return a.alarms + a.warnings - b.alarms - b.warnings;
        }).thenBy(function(a, b){
          return b.alarms - a.alarms;
        }).thenBy(function(a, b){
          return b.warnings - a.warnings;
        }).thenBy(function(a, b){
          return b.connected - a.connected;
        }).thenBy(function(a, b){
          return a.name - b.name;
        }));
        break;
    }
  }

  api.get('authentication/' + $routeParams.customer, function(result) {
    $scope.canView = true
  }, function(error) {
    api.get('customer', function(result) {
      window.location = "/index.html#/customer/" + result.id;
    })
  });
  api.get('authentication/' + $routeParams.customer + "?changes=True", function(result) {
    $scope.canEdit = result;
  });

    // -- INIT --

  $scope.getItem();

  /* -- THE LOOP -- */
  var intervalPromise = $interval(function () {
    $scope.getItem();
  }, 10000);    
  /* -- LOOP END -- */

  $scope.$on('$destroy', function () { $interval.cancel(intervalPromise); });

});