'use strict';

app.service('utils', function($rootScope, $filter) {

	this.isBefore = function(someDate, someOtherDate) {
		someDate 	  = someDate 		? (new Date(someDate)) 		: false;
		someOtherDate = someOtherDate 	? (new Date(someOtherDate)) : false;
		return someDate < someOtherDate;
	};
	this.isAfter = function(someDate, someOtherDate) {
		return !this.isBefore(someDate, someOtherDate);
	};

	this.filterTable = function(params, search, data) {
		var ordered  = params.sorting ? $filter('orderBy')(data, params.orderBy()) : data;
		if(ordered) {
			if(search) {
				ordered = $filter('filter')(ordered, search);
			}
			return ordered.slice((params.page - 1) * params.count, params.page * params.count);
		}
	};

	this.isEqual = function(a, b) {
		// ng-Repeat adds a property called $$haskKey, which makes ordinary equality-comparsions false
		return _.isEqual(_.omit(a, '$$hashKey'), _.omit(b, '$$hashKey'));
	}

	this.startsAndEndWithDoubleQuote = function (s) {
		return s && s[0] == '"' && s[s.length-1] == '"';
	};

	this.showSuccess = function(success) {
		if(typeof success == "string") {
			if(this.startsAndEndWithDoubleQuote(success)) {
				success = success.slice(1, -1);
			}

			$rootScope.response = {success: [success]};
		} else {
			$rootScope.response = {success: _.uniq(_.flatten(success))};
		}
	};

	this.showError = function(error) {
		if(typeof error == "string") {
			if(this.startsAndEndWithDoubleQuote(error)) {
				error = error.slice(1, -1);
			}
			$rootScope.response = {error: [error]};
		}
		else {
			$rootScope.response = {error: _.uniq(_.flatten(error))};
		}
	};

	this.changeFieldIn = function(array, field, value, whereField, whereValue) {
		for(var i = 0; i < array.length; i++) {
			if(whereValue == array[i][whereField]) {
				array[i][field] = value;
				break;
			}
		}
	};

	this.getPercentage = function(that, ofThat) {
		return $filter('percentof')(that, ofThat);
	};

	this.firstBy = (function() {
	    /* mixin for the `thenBy` property */
	    function extend(f) {
	        f.thenBy = tb;
	        return f;
	    }
	    /* adds a secondary compare function to the target function (`this` context)
	       which is applied in case the first one returns 0 (equal)
	       returns a new compare function, which has a `thenBy` method as well */
	    function tb(y) {
	        var x = this;
	        return extend(function(a, b) {
	            return x(a,b) || y(a,b);
	        });
	    }
	    return extend;
	})();
	
});