app.controller('CustomersCtrl', function($scope, $location, $filter, api, utils, $routeParams, BreadcrumbsService, $route, $interval, AuthService) {
	window.scope = $scope;
	$scope.title = "Customers"
	$scope.editing = false;
	$scope.filteredItems = [];
  $scope.currentPage = 0;
  $scope.numPerPage = 6;
  $scope.alarms = 0;
  $scope.warnings = 0;
  $scope.normals = 0;
  $scope.items = []
  $scope.firstBy = utils.firstBy;
  $scope.sorting = "alarms"

  // -- AUTHENTICATION AND ACCESSABILITY --

  $scope.canView = function() {
    return AuthService.canViewCustomer()
  }

  $scope.canEdit = function() {
    return AuthService.canEditCustomer()
  }

  $scope.canCreate = function() {
    return AuthService.isSuper()
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
  $scope.getItems = function() {
    api.get('customers', function(result) {
      $scope.items = result.customers;
      $scope.setUpItems();
    });
  }

  $scope.setUpItems = function() {
    $scope.alarms = 0;
    $scope.warnings = 0;
    $scope.normals = 0;
    $scope.items.forEach(function(item) {
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
		window.location="/index.html#/customer/"+ item.id;
	};

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
	}

	$scope.deleteItem = function(item) {
    api.doDelete('customer/' + item.id, function(result) {
      //success
      $route.reload();
    });
	}

	$scope.editItem = function(item) {
		window.location = "/index.html#/customer/" + item.id + "/edit";
	}

	$scope.newItem = function() {
		window.location = "/index.html#/customer/new/edit";
	}

  $scope.viewUsers = function() {
    window.location = "/index.html#/users/all";
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

  // -- INIT --

  $scope.getItems();

  /* -- THE LOOP -- */
  var intervalPromise = $interval(function () {
    $scope.getItems();
  }, 10000);    
  /* -- LOOP END -- */

  $scope.$on('$destroy', function () { $interval.cancel(intervalPromise); });
});
