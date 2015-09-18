app.filter('percentof', function() {
	return function(that, ofthat, precision) {
		precision = precision || 2;
		var percent = (100 * (that / ofthat).toFixed(precision));
		return percent > 100 ? (100.0).toFixed(precision) : percent.toFixed(precision);
	}
});