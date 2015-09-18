app.controller('ControllerCtrl', function($scope, $location, $filter, api, utils, ngTableParams, $routeParams, BreadcrumbsService, $route, $interval, AuthService) {
	window.scope = $scope;
	$scope.title = "Controller"
	$scope.alarms = [];
	$scope.values = [];
  $scope.alarmsView = true;
  $scope.valuesView = false;
	$scope.editing = false;
	$scope.filteredItems = [];
  $scope.currentPage = 0;
  $scope.numPerPage = 6;
  $scope.items = []
  $scope.sorting="address"

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

  // redirect if cant view
  if(AuthService.verifySessionAtServer() && !$scope.canView()){
    api.get('customer', function(result) {
      window.location = "/index.html#/customer/" + result[0].id;
    })
  }

  // -- END OF AUTHENTICATION AND ACCESSABILITY --

  // -- API CHAIN --
  $scope.getItem = function() {
    api.get('controller/' + $routeParams.installation + "?controller_ip=" + $routeParams.controller, function(result){
      $scope.currentItem = result;
      $scope.title = $scope.currentItem.name;
      BreadcrumbsService.setController(result)
      BreadcrumbsService.buildBreadcrumbs()
      $scope.getItems()
    });
  }

  $scope.getItems = function() {
    api.get('tags/' + $routeParams.installation + "?controller_ip=" + $routeParams.controller, function(result) {
      $scope.items = result.tags;
      $scope.setUpItems();
    });
  }

	$scope.setUpItems = function() {
    $scope.alarms = [];
    $scope.values = [];
		$scope.items.forEach(function(item) {
			if(!(item.type == 'value') && item.value == 1) {
				$scope.alarms.push(item);
			}
			$scope.values.push(item);
		})
    if($scope.alarmsView){
      $scope.items = $scope.alarms;
    }else{
      $scope.items = $scope.values;
    }
    $scope.sortBy($scope.sorting);
    $scope.$$phase || $scope.$apply();
	}

  // -- END API CHAIN

	$scope.numPages = function () {
	    return Math.ceil($scope.items.length / $scope.numPerPage);
	};

	$scope.firstBy = utils.firstBy;

	$scope.items.sort($scope.firstBy(function(a, b) {
		return b.errors - a.errors;
	}).thenBy(function(a, b){
		return b.warnings - a.warnings;
	}).thenBy(function(a, b){
    return b.connected - a.connected;
  }).thenBy(function(a, b){
    return a.name - b.name;
  }));

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

	$scope.setAlarmsTab = function() {
    $scope.alarmsView = true;
    $scope.valuesView = false;
		$scope.items = $scope.alarms;
		$scope.currentPage = 0;
    $scope.sortBy($scope.sorting);
	}

	$scope.setValuesTab = function() {
    $scope.valuesView = true;
    $scope.alarmsView = false;
		$scope.items = $scope.values;
		$scope.currentPage = 0;
    $scope.sortBy($scope.sorting);
	}

	$scope.toggleEditing = function() {
		$scope.editing = !$scope.editing;
	}

	$scope.deleteItem = function(item) {
    api.doDelete("tag/" + $routeParams.installation + "?controller_ip=" + $routeParams.controller + "&tag_name=" + item.name, function(result) {
    	//success
    	$route.reload();
    })
	}

	$scope.editItem = function(item) {
    console.log("/index.html#/customer/" + $routeParams.customer + "/installation/" + $routeParams.installation + "/controller/" + $routeParams.controller + "/tag/" + item.name + "/edit")
		window.location = "/index.html#/customer/" + $routeParams.customer + "/installation/" + $routeParams.installation + "/controller/" + $routeParams.controller + "/tag/" + item.name + "/edit";
	}

	$scope.newItem = function() {
		window.location = "/index.html#/customer/" + $routeParams.customer + "/installation/" + $routeParams.installation + "/controller/" + $routeParams.controller + "/tag/new/edit";
	}

	$scope.viewUsers = function() {
    window.location = "/index.html#/users/" + $routeParams.customer;
  }

  $scope.sortBy = function(string) {
    $scope.sorting = string
    switch(string) {
      case 'address':
        $scope.items.sort($scope.firstBy(function(a, b) {
          var a_reg = a.address.match(/\%[A-Z]*[a-z]*/g)[0]
          var b_reg = b.address.match(/\%[A-Z]*[a-z]*/g)[0]
          var a_list = a.address.match(/\d+/g);
          var b_list = b.address.match(/\d+/g);
          var a_main = parseInt(a_list[0])
          var b_main = parseInt(b_list[0])
          if(a_reg == b_reg){
            if(a_main == b_main){
              if(a_list.length == b_list.length){
                var a_alt = parseInt(a_list[1])
                var b_alt = parseInt(b_list[1])
                return a_alt - b_main;
              }else{
                return a_list.length - b_list.length;
              }
            }else{
              return a_main - b_main;
            }
          }else{
            return a_reg > b_reg;
          }

        }));
        break;
    }
  }

  // -- INIT --

  $scope.getItem();

  /* -- REFRESH -- */
  var intervalPromise = $interval(function () {
    $scope.getItem();
  }, 10000);    
  /* -- REFRESH END -- */

  $scope.$on('$destroy', function () { $interval.cancel(intervalPromise); });

});