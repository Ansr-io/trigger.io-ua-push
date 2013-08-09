module("urbanairship");

asyncTest("Attempt to activate push notifications", 1, function() {
	forge.urbanairship.getPushID(function (pushID) {
		ok(pushID, "Push ID received");
		start();
	}, function (content) {
		ok(false, JSON.stringify(content));
	});
});

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