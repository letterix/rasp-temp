'use strict';

describe('The tests are loaded correctly', function(){
	it('Test-suite should not crash', function() {
		expect(true).not.toBe(false);
		expect(false).not.toBe(true);
	});
});