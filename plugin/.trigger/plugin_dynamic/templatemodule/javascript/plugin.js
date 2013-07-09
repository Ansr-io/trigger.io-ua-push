// Expose the native API to javascript
forge.templatemodule = {
    showAlert: function (text, success, error) {
        forge.internal.call('templatemodule.showAlert', {text: text}, success, error);
    }
};

// Register for our native event
forge.internal.addEventListener("templatemodule.resume", function () {
	alert("Weclome back!");
});
