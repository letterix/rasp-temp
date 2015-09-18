app.controller('EditUserCtrl', function($scope, $location, $filter, api, utils, ngTableParams, $routeParams, AuthService) {
  window.scope = $scope;
  $scope.currentUser = {}
  $scope.customers = []
  $scope.userCustomers = []
  $scope.masterCustomers = []
  $scope.customersPristine = true
  $scope.selectedCustomers = []
  $scope.master = {"id":1, "name":"master", "ticked":false}
  $scope.customer = {"id":1, "name":"master", "ticked":false}
  $scope.emailRegex = /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i

  $scope.masterRoles = ["Super User", "Master Admin", "Master User", "Admin", "User"]
  $scope.normalRoles = ["Admin", "User"]
  $scope.roles = $scope.normalRoles
    

  // -- AUTHENTICATION AND ACCESSABILITY --

  $scope.isMaster = function(){
    return AuthService.isMaster()
  }

  // -- END OF AUTHENTICATION AND ACCESSABILITY --

  $scope.initCustomers = function() {
    api.get('customers', function(result) {
      $scope.customers = result.customers
      angular.forEach( $scope.customers, function( customer, key ) {
        customer.name.capitalize()
        angular.forEach( $scope.userCustomers, function( userCustomer, key ) {
          if(userCustomer.id === customer.id){
            customer.ticked = true
            if($scope.isNormalRole($scope.item.role)){
              $scope.customer = customer
            }
          }
          if(userCustomer.id === $scope.master.id){
            $scope.master.ticked = true
          }
        });
      });
      $scope.masterCustomers = $scope.customers.slice(0)
      $scope.masterCustomers.splice(0,0,$scope.master)
      if($scope.isNormalRole($scope.currentUser.role) || ($scope.isMasterRole($scope.currentUser.role) && !$scope.isAdminRole($scope.currentUser.role))){
        $scope.roles = $scope.normalRoles
      }else{
        $scope.roles = $scope.masterRoles
      }
    });
  }

  $scope.initCurrentUser = function() {
    api.get('user/', function(result) {
      $scope.currentUser = result
      $scope.initCustomers();
    });
  }

  $scope.submit = function() {
    $scope.item.role = $scope.getUnPrettyRole($scope.item.role)
    $scope.setCustomers()
    if($routeParams.user == 'new'){
      api.post("user/", $scope.item, function(result) {
        //success
        $scope.viewItems();
      }, function(result) {
        //fail
      })
    }else{
      api.put("user/" + $routeParams.user, $scope.item, function(result) {
        //success
        $scope.viewItems();
      }, function(result) {
        //fail
      })
    }
  };

  $scope.viewItems = function() {
    api.get('customer/', function(result){
      console.log(result)
      if(result.length > 1){
        window.location = "/index.html#/users/all";
      }else{
        window.location = "/index.html#/users/" + result[0].id;
      }
    })
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

  $scope.getUnPrettyRole = function(role) {
    switch (role) {
      case "Super User":
          return "super_user"
      case "Master Admin":
          return "master_admin"
      case "Master User":
          return "master_user"
      case "Admin":
          return "admin"
      case "User":
          return "user"
    }
  }

  $scope.isNormalRole = function(role) {
    switch (role) {
      case "admin":
          return true
      case "Admin":
          return true
      case "user":
          return true
      case "User":
          return true
    }
    return false
  }


  $scope.isAdminRole = function(role) {
    switch (role) {
      case "admin":
          return true
      case "Admin":
          return true
      case "master_admin":
          return true
      case "Master Admin":
          return true
      case "super_user":
          return true
      case "Super User":
          return true
    }
    return false
  }


  $scope.isMasterRole = function(role) {
    switch (role) {
      case "master_user":
          return true
      case "Master User":
          return true
      case "master_admin":
          return true
      case "Master Admin":
          return true
      case "super_user":
          return true
      case "Super User":
          return true
    }
    return false
  }


  $scope.isSuperRole = function(role) {
    switch (role) {
      case "master_admin":
          return true
      case "Master Admin":
          return true
      case "super_user":
          return true
      case "Super User":
          return true
    }
    return false
  }

  $scope.customersChanged = function() {
    $scope.customersPristine = false
  }

  scope.setCustomers = function() {
    if($scope.isNormalRole($scope.currentUser.role)){
      $scope.item.customers=[scope.currentUser.customers[0].id]
    }else{
      if($scope.isNormalRole($scope.item.role)){
        $scope.item.customers = [$scope.customer.id]
      }else{
        $scope.item.customers = []
        angular.forEach( $scope.selectedCustomers, function( value, key ) {
          $scope.item.customers.push(value.id)
        });
      }
    }
  }


  if($routeParams.user == 'new') {
    //New item
    $scope.title = "New"
    $scope.item = {
      'name':"",
      'surname':"",
      'phone':"",
      'role':"",
      'username':"",
      'password':"",
      'confirmPassword':"",
      'email':"",
    }
    $scope.initCurrentUser();
  }else{
    //Edit
    console.log(decodeURIComponent($routeParams.user))
    api.get("user/" + $routeParams.user, function(result) {
      $scope.item = result;
      if($scope.item.customers && $scope.item.customers.length){
        $scope.customer = $scope.item.customers[0]
        $scope.userCustomers = $scope.item.customers
      }
      $scope.item.role = $scope.getPrettyRole($scope.item.role)
      $scope.title = $scope.item.name.capitalize() + " " + $scope.item.surname.capitalize();
      $scope.initCurrentUser();
    });
  }
  api.get('authentication', function(result) {
    $scope.canEdit = result;
    if($scope.canEdit){

    }
  });
});