app.controller('EditCustomerCtrl', function($scope, $location, $filter, api, utils, ngTableParams, $routeParams, AuthService) {
	window.scope = $scope;
	$scope.title="";
	console.log($routeParams.customer)
    
    if($routeParams.customer == 'new') {
    	//New item
    	$scope.title = "New"
    	$scope.item = {
    		'name':""
    	}
    }else{
    	//Edit
    	api.get('customer/' + $routeParams.customer, function(result) {
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
		if($routeParams.customer == 'new'){
			api.post('customer', $scope.item, function(result) {
				//success
				$scope.viewItems();
			}, function(result) {
				//fail
			})
		}else{
			api.put('customer/' + $routeParams.customer, $scope.item, function(result) {
				$scope.viewItems();
				//success
			}, function(result) {
				//fail
			})
		}
	};

	$scope.viewItems = function() {
		window.location = /index.html#/;
	}

});