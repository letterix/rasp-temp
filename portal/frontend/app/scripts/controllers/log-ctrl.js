app.controller('LogCtrl', function($scope, $location, $filter, api, utils, ngTableParams, $routeParams, $sce, promiseTracker, $q) {
	window.scope = $scope;

	$scope.installationId = $routeParams.installationid;
	$scope.logEntries = [];
	$scope.logEntriesOrdered = [];
	$scope.search = "";

	var dateOffset = (24*60*60*1000) * 1
	$scope.fromDate = new Date();

	$scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'shortDate'];
	$scope.format = $scope.formats[1];

	$scope.toDate = new Date();

	function getLog() {
		var loadPromise = $q.defer();
		promiseTracker('loading').addPromise(loadPromise.promise);
		var toDate = $scope.toDate.getTime() + dateOffset;
		api.get('log/' + $scope.installationId + 
			'?fromDate=' + $filter('date')($scope.fromDate, $scope.format) + 
			'&toDate=' +  $filter('date')(toDate, $scope.format), 
			function(result) {
				$scope.logEntries = result;
				for( var i = 0; i < $scope.logEntries.length; i++) {
					if($scope.logEntries[i].name.indexOf("CR") == 0) {
						var min = ($scope.logEntries[i].value & 0xf00) >> 8;
						var max = ($scope.logEntries[i].value & 0xf000) >> 12;
						var set = $scope.logEntries[i].value & 0xff;
						$scope.logEntries[i].value = min + " " + max + " " + set + " (" + $scope.logEntries[i].value + ")";
					}
				}
				loadPromise.resolve();
				setupTable();
		});
	}
	getLog();

	$scope.tableParams = new ngTableParams();
	$scope.tableParams.settings().$scope = $scope
	function setupTable() {
		$scope.tableParams = new ngTableParams({
	        page: 1,            // show first page
	        count: 100,          // count per page
	        sorting: {
	            time: 'desc'     // initial sorting
	        }
	    }, {
	        total: $scope.logEntries.length, // length of data
	        getData: function($defer, params) {
	            
	            var filteredData = params.filter() ?
	                        $filter('filter')($scope.logEntries, $scope.search) :
	                        $scope.logEntries;

	            var orderedData = params.sorting() ?
	                                $filter('orderBy')(filteredData, params.orderBy()) :
	                                filteredData;
	            params.total(orderedData.length);
	            $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
	        }
	    });
	    $scope.$watch('search', function() {
			$scope.tableParams.reload()
		}, true);
		$scope.tableParams.settings().$scope = $scope
	}

	$scope.reloadLog = function() {
		$scope.tableParams = new ngTableParams();
		$scope.tableParams.settings().$scope = $scope
		$scope.logEntries = [];
		getLog();
	}



	function filter(params) {
		params = $scope.tableParams || params;
		$scope.logEntriesOrdered = utils.filterTable(params, $scope.search, $scope.logEntries);
	};

	$scope.returnPrevPage = function(){
		window.history.back();
	}

	$scope.showAll = function(){
		$scope.tableParams.count($scope.logEntries.length);
		$scope.tableParams.reload()
	}

	// DATE SELECTORS:

	$scope.toggleMax = function() {
		$scope.maxDate = ( $scope.maxDate ) ? null : new Date();
	};
	$scope.toggleMax();

	$scope.open = function($event) {
		$event.preventDefault();
		$event.stopPropagation();

		$scope.opened = true;
	};

	$scope.openTo = function($event) {
		$event.preventDefault();
		$event.stopPropagation();

		$scope.openedTo = true;
	};

	$scope.dateOptions = {
		'year-format': "'yy'",
		'starting-day': 1
	};
});