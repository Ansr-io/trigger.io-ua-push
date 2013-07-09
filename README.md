## trigger.io-ua-push

plugin for trigger.io platform allowing integration with push messaging service provided by Urban Airship
Ported and modified with permission, from the official phonegap plugin.

**************************************************************************************
****IMPORTANT THIS PLUGIN REQUIRES THE USE OF BUILD HOOKS - SEE BELOW FOR DETAILS!****
**************************************************************************************

### project url
https://github.com/Ansr-io/trigger.io-ua-push

### project author
petehobo @ gmail DOT com

### project status
Alpha

### setup
setup urbanship account

Follow setup steps for ios and Android from : 

ios :http://docs.urbanairship.com/build/ios.html
android : http://docs.urbanairship.com/build/android.html

You will end with two configured services:

Apple Push Notification Service (APNS)
& 

Google Cloud Messaging (GCM)
NB. set ‘gcmSender’ in ‘hooks/postbuild/uaplugin/airshipconfig.properties’ equal to GCM Project Number, 
see https://code.google.com/apis/console/ > project overview.

### Build Plugin (optional)

Import the plugin inspectors to your forge workspace.  
Build and upload the libiary versions of the plugin following:

https://trigger.io/docs/current/api/native_plugins/index.html (Section Building/packaging your plugin)


### Run Test App
Import the plugin
Import the demo app /UA

IMPORTANT - USE OF HOOKS.  The Urban Airship system needs to modify the generated forge project during 
the build process.  This is accomplished by use of build hooks 
( https://trigger.io/docs/current/tools/hooks.html ) .  
When developing your own project you must copy the Hooks folder from the demo project.  
PLEASE NOTE - special attention will be required if your project uses build hooks. 
 Further, the Android version of the plugin makes direct modifications to the generated 
 Android-manifest .xml file - this could potentially cause unexpected results.  
 ***************USE WITH CAUTION**************


Modify local UA settings:

#### Android

Update the UA settings file in hooks/postbuild/uaplugin/airshipconfig.properties

Open hooks/postbuild/hook.py - replace the string ‘com.plugtester’ with your app package name.
N.B. package name is defined in src/config.json


#### iOS

Update the UA settings file in hooks/postbuild/uaplugin/airshipConfig.plist


### API documentation

For full API details see:

http://docs.urbanairship.com/build/phonegap.html#javascript-api
https://github.com/urbanairship/phonegap-ua-push



```
forge.urbanairship = {
    showAlert: function (text, success, error) {
        // does nothing ?
    },
    enablePush: function ( success, error) {
        //
    },
    disablePush: function ( success, error) {
        //
    },
    enableLocation: function ( success, error) {
        //
    },
    disableLocation: function ( success, error) {
        //
    },
    enableBackgroundLocation: function ( success, error) {
        //
    },
    disableBackgroundLocation: function (success, error) {
        //
    },
    // ------------------------------------------------------------
    isPushEnabled: function (callback) {},
    isSoundEnabled: function (callback) {},
    isVibrateEnabled: function (callback) {},
    isQuietTimeEnabled: function (callback) {},
    isInQuietTime: function (callback) {},
    isLocationEnabled: function (callback) {},
    isBackgroundLocationEnabled: function (callback) {},
    // ------------------------------------------------------------
    getIncoming: function ( success, error) {
        // Will bring up any existing notification if launched from one
        // i.e. is only called when the app is NOT running and is launched from a push notification
    },
    getPushID: function ( success, error) {
        //
    },
    getQuietTime: function (success, error) {
        // @return : Object : {"startHour":0,"startMinute":0,"endHour":0,"endMinute":0}
    },
    getTags: function (success, error) {
        // @return : Array : array of tags
    },
    getAlias: function ( success, error) {
        // tested: ..working ?
        // returns success, but value is empty string
    },
    // ------------------------------------------------------------
    setAlias: function (text, success, error) {
        // tested: ..working ?
        // returns success but no value is set.
        //
        // @text : String : alias
        // Set alias for the device.
    },
    setTags: function (tags, success, error) {
        // @tags: Array : list of Strings to set
    },
    setSoundEnabled: function (enabled, callback) {
        // Note: Android Only, iOS sound settings come in the push
        // Set whether the device makes sound on push.
    },
    setVibrateEnabled: function (enabled, callback) {
        // Note: Android Only
        // Set whether the device vibrates on push.
    },
    setQuietTimeEnabled: function (enabled, callback) {
        //
    },
    setQuietTime: function (startHour, startMinute, endHour, endMinute, success, error) {
        // tested:working
        // expected arguments: [QuietTime, success, error]
        // i.e. QuietTime : Object : same format as returned by getQuietTime
        // e.g. {"startHour":0,"startMinute":0,"endHour":0,"endMinute":0}
    },
    setAutobadgeEnabled: function (enabled, callback) {
        // Note: iOS only
    },
    setBadgeNumber: function (number, success, error) {
        // Note: iOS only
    }
};
forge.internal.addEventListener("urbanairship.pushReceived", function (data) {
    // Register for our native push events
    // this is called when a push is received: ONLY while the app is active
});
```