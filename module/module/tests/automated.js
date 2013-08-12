module("urbanairship");

// In this test we call the example showAlert API method with an empty string
// In the example API method an empty string will immediately call the error callback


asyncTest("disablePush", 1, function() {
	forge.urbanairship.disablePush(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("enablePush", 1, function() {
	forge.urbanairship.enablePush(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("enableLocation", 1, function() {
	forge.urbanairship.enableLocation(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("disableLocation", 1, function() {
	forge.urbanairship.disableLocation(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("enableBackgroundLocation", 1, function() {
	forge.urbanairship.enableBackgroundLocation(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("disableBackgroundLocation", 1, function() {
	forge.urbanairship.disableBackgroundLocation(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

//is tests
asyncTest("isPushEnabled", 1, function() {
	forge.urbanairship.isPushEnabled(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("isPushEnabled", 1, function() {
	forge.urbanairship.isPushEnabled(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("isVibrateEnabled", 1, function() {
	forge.urbanairship.isVibrateEnabled(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});
asyncTest("isQuietTimeEnabled", 1, function() {
	forge.urbanairship.isQuietTimeEnabled(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});
asyncTest("isInQuietTime", 1, function() {
	forge.urbanairship.isInQuietTime(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});
asyncTest("isLocationEnabled", 1, function() {
	forge.urbanairship.isLocationEnabled(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("isBackgroundLocationEnabled", 1, function() {
	forge.urbanairship.isBackgroundLocationEnabled(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("getIncoming", 1, function() {
	forge.urbanairship.getIncoming(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("getPushID", 1, function() {
	forge.urbanairship.getPushID(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("getIncoming", 1, function() {
	forge.urbanairship.getIncoming(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("getQuietTime", 1, function() {
	forge.urbanairship.getQuietTime(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("getTags", 1, function() {
	forge.urbanairship.getTags(function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("setAlias", 1, function() {
	forge.urbanairship.setAlias("hello",function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("setTags", 1, function() {
	forge.urbanairship.setTags(["loves_cats", "shops_for_games"],function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("setSoundEnabled", 1, function() {
	forge.urbanairship.setSoundEnabled(1,function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("setVibrateEnabled", 1, function() {
	forge.urbanairship.setVibrateEnabled(1,function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("setQuietTimeEnabled", 1, function() {
	forge.urbanairship.setQuietTimeEnabled(1,function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});

asyncTest("setQuietTime", 1, function() {
	forge.urbanairship.setQuietTime(10,0,12,30,function () {
		ok(true, "ok");
		start();
	}, function () {
		ok(false, "failure");
		start();
	});
});


