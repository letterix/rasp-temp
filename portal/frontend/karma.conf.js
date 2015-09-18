// Karma configuration

module.exports = function (config) {
	config.set({
		// base path, that will be used to resolve files and exclude
		basePath: '',

		// list of files / patterns to load in the browser
		frameworks: ['jasmine'],
		files: [
		'libs/jquery/jquery.js',
		'libs/underscore/underscore.js',
		'libs/angular/angular.js',
		'libs/angular-route/angular-route.js',
		'libs/angular-route/angular-mocks.js',
		'libs/bootstrap/dist/js/bootstrap.js',

		'app/js/app.js',

		'test/mock/**/*.js',
		'test/spec/**/*.js'
		],

		// list of files to exclude
		exclude: [],

		// test results reporter to use
		// possible values: dots || progress || growl
		reporters: ['progress'],

		// web server port
		port: 9000,
		// cli runner port
		runnerPort: 9999,

		// enable / disable colors in the output (reporters and logs)
		colors: true,

		// level of logging
		// possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
		logLevel: 'karma.LOG_INFO',

		// enable / disable watching file and executing tests whenever any file changes
		autoWatch: true,

		// Start these browsers, currently available:
		// - Chrome
		// - ChromeCanary
		// - Firefox
		// - Opera
		// - Safari (only Mac)
		// - PhantomJS
		// - IE (only Windows)
		browsers: ['Chrome'],

		// If browser does not capture in given timeout [ms], kill it
		captureTimeout: 5000,

		// Continuous Integration mode
		// if true, it capture browsers, run tests and exit
		singleRun: false
	});
};