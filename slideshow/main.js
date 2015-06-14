'use strict';
let app = require('app');
let BrowserWindow = require('browser-window');
let ipc = require('ipc');
let zerorpc = require('zerorpc');
let watcher = require('watch');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the javascript object is GCed.
let mainWindow = null;

// Quit when all windows are closed.
app.on('window-all-closed', function () {
	if (process.platform != 'darwin')
		app.quit();
});

// This method will be called when Electron has done everything
// initialization and ready for creating browser windows.
app.on('ready', function () {
	// Create the browser window.
	mainWindow = new BrowserWindow({
		'use-content-size': true,
		'min-width': 500,
		'min-height': 400,
		resizable: true,
		center: true,
		title: 'Slide Show',
		webgl: true,
		webaudio: true,
		plugins: true,
		'experimental-features': true,
		'shared-worker': true
	});

	// and load the index.html of the app.
	mainWindow.loadUrl('file://' + __dirname + '/index.html');
	mainWindow.webContents.on('did-finish-load', function () {
		mainWindow.webContents.send('darawCarousal');
	});


	// Emitted when the window is closed.
	mainWindow.on('closed', function () {
		// Dereference the window object, usually you would store windows
		// in an array if your app supports multi windows, this is the time
		// when you should delete the corresponding element.
		mainWindow = null;
	});

	//Setup zerorpc for receiving commands
	let server = new zerorpc.Server({
		cmd: function (cmd, reply) {
			reply();
			mainWindow.webContents.send('cmd', cmd);
		},
		next: function (reply) {
			mainWindow.webContents.send('cmd', 'next');
			reply();
		},
		previous: function (reply) {
			mainWindow.webContents.send('cmd', 'previous');
			reply();
		}
	});
	watcher.watchTree('images', function () {
		mainWindow.webContents.send('darawCarousal');
	});

	server.bind("tcp://0.0.0.0:4242");
});