
// Register for our native push events
//this is called when a push is received while the app is active
forge.internal.addEventListener("urbanairship.pushReceived", function (data) {
	alert(data);
});

//generic success 
function success(d) {
   forge.logging.log('success :: '+JSON.stringify(d));
}

//generic error callback
function errorfail(e) {
	 forge.logging.log('errorfail :: '+JSON.stringify(e));
}

//*******************
// Minimal App startup 
//*******************

//Enable push services
forge.urbanairship.enablePush(success,errorfail);

//Will bring up any existing notification if launched from one
//forge.urbanairship.getIncoming(function (d) {alert(JSON.stringify(d)) },errorfail);

//*******************
// Optional Startup 
//*******************

//startup background location services
forge.urbanairship.enableBackgroundLocation(success,errorfail);

//shutdown background location services
//forge.urbanairship.disableBackgroundLocation(success,errorfail);

//*******************
// Test functionality
//*******************



forge.urbanairship.setTags( ["pete","me"], success, errorfail);
forge.urbanairship.getTags( function (d)  { forge.logging.log(d[0]);} , errorfail);
