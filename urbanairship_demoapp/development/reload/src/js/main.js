
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

//alert (JSON.parse (["pete","me"]));
//forge.urbanairship.setTags(["pete","me"],success,errorfail);

function getTags ( success, error) {
    	suc_f = function (d) {
    		suc_f.cb( JSON.parse(d.tags));
    	}
    	suc_f.cb = success;
        forge.internal.call('urbanairship.getTags', {}, suc_f, error);
    } 

function get_tags_success(d) {
 
  forge.logging.log('success :: '+(JSON.parse(d.tags)));
}

 forge.internal.call('urbanairship.setTags', {"tags":["pete","me"]}, success, errorfail);
 getTags( success, errorfail);