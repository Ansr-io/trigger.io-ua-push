module("urbanairship");

asyncTest("Attempt to receive a push notitication", 1, function() {
	askQuestion("Create a push notification that this device should receive in the Urban Airship console", {
		"OK: nothing happened": function () {
			ok(false, "User claims failure");
			start();
		}
	});
	forge.urbanairship.pushReceived.addListener(function (msg) {
		ok(true, JSON.stringify(msg));
		start();
	});
});