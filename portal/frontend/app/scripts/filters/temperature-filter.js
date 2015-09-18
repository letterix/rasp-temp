
function celciusToFarenheit(deg) {
	return (deg * 1.8) + 32
}
function farenheitToCelcius(deg) {
	return (deg - 32) / 1.8
}

app.filter('deg', function() {
	return function(val, from, to) {
		var output,
			celcius = 'C',
			farenheit = 'F';

		from = from ? from.toUpperCase() : celcius;
		to = to ? to.toUpperCase() : from;

		if(from == celcius && to == farenheit) {
			output = celciusToFarenheit(val);
		}
		else if(from == farenheit && to == celcius) {
			output = farenheitToCelcius(val);
		}
		else {
			output = val;
		}

		output = output ? output.toFixed(2) : '?';
		return output + ' °' + to;
	}
});