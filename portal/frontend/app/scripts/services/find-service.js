'use strict';

app.service('find', function() {
	this.indexOfObjectByField = function(list, field, needle) {
		if(list && list.length > 0) {
			for(var i = 0, len = list.length; i < len; i++) {
				if(list[i][field] === needle) {
					return i;
				}
			}
		}
		return -1; // No user found
	};

	this.objectByIndex = function(list, index) {
		return (typeof list[index] !== 'undefined' && list[index] !== null) ? list[index] : -1;
	};

	this.objectByField = function(list, field, needle) {
		var index = this.indexOfObjectByField(list, field, needle);
		return this.objectByIndex(list, index);
	};
});