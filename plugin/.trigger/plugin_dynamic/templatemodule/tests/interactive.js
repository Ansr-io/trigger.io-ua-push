module("templatemodule");

// In this test we call the example showAlert API method with an example string
asyncTest("Attempt to show an alert with no text", 1, function() {
	forge.templatemodule.showAlert("Hello, testing world!", function () {
		askQuestion("Did you see an alert with the message 'Hello, testing world!'?", {
			Yes: function () {
				ok(true, "User claims success");
				start();
			},
			No: function () {
				ok(false, "User claims failure");
				start();
			}
		});
	}, function () {
		ok(false, "API method returned failure");
		start();
	});
});