app.controller('EditTagCtrl', function($scope, $location, $filter, api, utils, ngTableParams, $routeParams, AuthService) {
	window.scope = $scope;
	$scope.types = ["value", "alarm", "warning"]
    
    if($routeParams.tag == 'new') {
    	//New item
    	$scope.title = "New"
    	$scope.item = {
    		'name':"",
    		'address':"",
    		'type':""
    	}
    }else{
    	//Edit
    	api.get("tag/" + $routeParams.installation + "?controller_ip=" + $routeParams.controller + "&tag_name=" + $routeParams.tag, function(result) {
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
    $scope.item.installation = $routeParams.installation;
    $scope.item.controller_ip = $routeParams.controller;
		if($routeParams.tag == 'new'){
			//populate the last fields by auto
			api.post("tag/", $scope.item, function(result) {
				//success
				$scope.viewItems();
			}, function(result) {
				//fail
			})
		}else{
			api.put("tag/", $scope.item, function(result) {
				//success
				$scope.viewItems();
			}, function(result) {
				//fail
			})
		}
	};

	$scope.viewItems = function() {
		window.location = "/index.html#/customer/" + $routeParams.customer + "/installation/" + $routeParams.installation + "/controller/" + $routeParams.controller;
	}

});