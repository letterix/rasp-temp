app.controller('EditInstallationCtrl', function($scope, $location, $filter, api, utils, ngTableParams, $routeParams, AuthService) {
	window.scope = $scope;
    $routeParams.installation;
    
    if($routeParams.installation == 'new') {
    	//New item
    	$scope.title = "New"
    	$scope.item = {
    		'name':"",
    		'serial_number':""
    	}
    }else{
    	//Edit
    	api.get('installation/' + $routeParams.installation, function(result) {
			$scope.item = result;
			$scope.title = $scope.item.name
		});
    }
	
  // -- AUTHENTICATION AND ACCESSABILITY --

  $scope.isMaster = function(){
    return AuthService.isMaster()
  }

  // -- END OF AUTHENTICATION AND ACCESSABILITY --

	$scope.submit = function() {
		if($routeParams.installation == 'new'){
			//populate the last fields by auto
			$scope.item.customer = $routeParams.customer;
			api.post('installation', $scope.item, function(result) {
				//success
				$scope.viewItems();
			}, function(result) {
				//fail
			})
		}else{
			api.put('installation/' + $routeParams.installation, $scope.item, function(result) {
				//success
				$scope.viewItems();
			}, function(result) {
				//fail
			})
		}
	};

	$scope.viewItems = function() {
		window.location = "/index.html#/customer/" + $routeParams.customer
	}

});