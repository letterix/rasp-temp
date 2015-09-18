app.controller('UsersCtrl', function($scope, $location, $filter, api, utils, $routeParams, $route, $interval, AuthService) {
  window.scope = $scope;
  $scope.title = "Users"
  $scope.cogDropdown = false;
  $scope.editing = false;
  $scope.filteredItems = [];
  $scope.currentPage = 0;
  $scope.numPerPage = 6;
  $scope.currentUser = {}
  $scope.items = []


  // -- AUTHENTICATION AND ACCESSABILITY --

  $scope.canCreate = function() {
    return AuthService.isAdmin() || AuthService.isMaster()
  }

  $scope.isMaster = function(){
    return AuthService.isMaster()
  }

  // -- END OF AUTHENTICATION AND ACCESSABILITY --

  $scope.getItems = function() {
    api.get('users', function(result) {
      $scope.items = result;
      angular.forEach( $scope.items, function( value, key ) {
        if(value.customers && value.customers.length){
          value.customer = value.customers[0]
        }
      });
      $scope.sortItems();
    });
  }

  $scope.sortItems = function() {
    $scope.items.sort($scope.firstBy(function(a, b) {
      return a.surname - b.surname;
    }).thenBy(function(a, b){
      return a.name - b.name;
    }));
  }

  $scope.numPages = function () {
      return Math.ceil($scope.items.length / $scope.numPerPage);
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

  $scope.toggleCogDropdown = function() {
    $scope.cogDropdown = !$scope.cogDropdown;
  }

  $scope.toggleEditing = function() {
    $scope.editing = !$scope.editing;
    $scope.toggleCogDropdown();
  }

  $scope.deleteItem = function(item) {
      api.doDelete('user/' + item.username, function(result) {
      //success
      $route.reload();
    });
  }

  $scope.editItem = function(item) {
    window.location = "/index.html#/user/" + item.username + "/edit";
  }

  $scope.newItem = function() {
    window.location = "/index.html#/user/new/edit";
  }

  $scope.viewItems = function() {
    window.location = "/index.html#/";
  }

  $scope.getPrettyRole = function(role) {
    switch (role) {
      case "super_user":
          return "Super User"
      case "master_admin":
          return "Master Admin"
      case "master_user":
          return "Master User"
      case "admin":
          return "Admin"
      case "user":
          return "User"
    }
  }

  $scope.firstBy = utils.firstBy;

  $scope.getItems();
  
    /* -- THE LOOP -- */
  var intervalPromise = $interval(function () {
    $scope.getItems();
  }, 10000);    
  /* -- LOOP END -- */

  $scope.$on('$destroy', function () { $interval.cancel(intervalPromise); });

});
