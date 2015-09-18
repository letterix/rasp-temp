app.controller('EditControllerCtrl', function($scope, $location, $filter, api, utils, ngTableParams, $routeParams, AuthService) {
	window.scope = $scope;
  
  // -- AUTHENTICATION AND ACCESSABILITY --

  $scope.isMaster = function(){
    return AuthService.isMaster()
  }

  // -- END OF AUTHENTICATION AND ACCESSABILITY --

  if($routeParams.controller == 'new') {
  	//New item
  	$scope.title = "New"
  	$scope.item = {
  		'name':"",
  		'ip':""
  	}
  }else{
  	//Edit
  	api.get("controller/" + $routeParams.installation + "?controller_ip=" + $routeParams.controller, function(result) {
		$scope.item = result;
		$scope.title = $scope.item.name
	});
  }

  $scope.submit = function() {
    $scope.item.installation = $routeParams.installation;
  	if($routeParams.controller == 'new'){
  		//populate the last fields by auto
  		api.post("controller/", $scope.item, function(result) {
  			//success
  			$scope.viewItems();
  		}, function(result) {
  			//fail
  		})
  	}else{
  		api.put("controller/", $scope.item, function(result) {
  			//success
  			$scope.viewItems();
  		}, function(result) {
  			//fail
  		})
  	}
  };

  $scope.viewItems = function() {
  	window.location = "/index.html#/customer/" + $routeParams.customer + "/installation/" + $routeParams.installation;
  }

});