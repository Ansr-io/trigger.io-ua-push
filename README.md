## trigger.io-ua-push

plugin for trigger.io platform allowing integration with push messaging service provided by Urban Airship
Ported and modified with permission, from the official phonegap plugin.


**************************************************************************************
****IMPORTANT THIS PLUGIN REQUIRES THE USE OF BUILD HOOKS - SEE BELOW FOR DETAILS!****
**************************************************************************************

### project url
[https://github.com/Ansr-io/trigger.io-ua-push](https://github.com/Ansr-io/trigger.io-ua-push)

### project author
petehobo @ gmail DOT com

### project status
Alpha

### setup
setup urbanship account

Follow setup steps for ios and Android from : 

[http://docs.urbanairship.com/build/ios.html](http://docs.urbanairship.com/build/ios.html)

[http://docs.urbanairship.com/build/android.html](http://docs.urbanairship.com/build/android.html)


You will end with two configured services:

- Apple Push Notification Service (APNS)
- Google Cloud Messaging (GCM)

NB. set `gcmSender` in `hooks/postbuild/uaplugin/airshipconfig.properties` equal to GCM Project Number, 
see https://code.google.com/apis/console/ > project overview.


### Build Plugin (optional)

Import the plugin inspectors to your forge workspace.  
Build and upload the libiary versions of the plugin following:

[https://trigger.io/docs/current/api/native_plugins/index.html](https://trigger.io/docs/current/api/native_plugins/index.html) (see section 'Building/packaging your plugin').


### Run Test App
Import the plugin
Import the demo app /UA

** IMPORTANT - USE OF HOOKS. **  
The Urban Airship system needs to modify the generated forge project during 
the build process.  This is accomplished by use of build hooks 
[https://trigger.io/docs/current/tools/hooks.html](https://trigger.io/docs/current/tools/hooks.html).  
When developing your own project you must copy the Hooks folder from the demo project.  
PLEASE NOTE - special attention will be required if your project uses build hooks. 

 Further, the Android version of the plugin makes direct modifications to the generated 
 
 `Android-manifest.xml` file - this could potentially cause unexpected results.  
 
** >>> USE WITH CAUTION <<< **


### Modify local UrbanAirship settings

#### Android

Update the UA settings file `hooks/postbuild/uaplugin/airshipconfig.properties`

Open `hooks/postbuild/hook.py`, and set `APP_PACKAGE_NAME` to your app package name.

N.B. package_names is defined in `src/config.json`.
- package name must be a valid Java package name (lowercase, no hyphens)
- package name may not contain underscores - Apple rejects bundle identifiers with underscores as invalid.


#### iOS

Update the UA settings file `hooks/postbuild/uaplugin/airshipConfig.plist`


## API documentation

All methods without a return value return null or undefined.

### enablePush()
Enable push notifications on the device. This sends a registration request to the backend service.


```
forge.urbanairship = {
    enablePush: function (success, error) {
        // Enable push notifications on the device. This sends a registration request to the backend service.
    },
    disablePush: function (success, error) {
        // Disable push notifications on the device. The device will no longer recieve push notifications.
    },
    enableLocation: function (success, error) {
        // Enable location updates on the device.
    },
    disableLocation: function (success, error) {
        // Disable location updates on the device.
    },
    enableBackgroundLocation: function (success, error) {
        // Enable background location updates on the device.
    },
    disableBackgroundLocation: function (success, error) {
        // Disable background location updates on the device.
    },
    registerForNotificationTypes: function (bitmask) {
        // Note:: iOS Only
        //
        // On iOS, registration for push requires specifying what combination of badges,
        // sound and alerts are desired. This function must be explicitly called in order
        // to begin the registration process. For example:
        //
        // push.registerForNotificationTypes(push.notificationType.sound | push.notificationType.alert)
        //
        // If your are unfamiliar with bitmasks, see: https://en.wikipedia.org/wiki/Bitmask#Uses_of_bitmasks
        //
        // Available notification types:
        //
        // notificationType.sound
        // notificationType.alert
        // notificationType.badge
    },
    // ------------------------------------------------------------
    isPushEnabled: function (callback) {
        // Callback arguments : Boolean : enabled
    },
    isSoundEnabled: function (callback) {
        // Note: Android Only
        // Callback arguments : Boolean : enabled
    },
    isVibrateEnabled: function (callback) {
        // Note: Android Only
        // Callback arguments : Boolean : enabled
    },
    isQuietTimeEnabled: function (callback) {
        // Callback arguments : Boolean : enabled
    },
    isInQuietTime: function (callback) {
        // Callback arguments : Boolean : enabled
    },
    isLocationEnabled: function (callback) {
        // Callback arguments : Boolean : enabled
    },
    isBackgroundLocationEnabled: function (callback) {
        // Callback arguments : Boolean : enabled
    },
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
    getAlias: function (success, error) {
        // @return : String : alias
        // Get alias for the device.
    },
    // ------------------------------------------------------------
    setAlias: function (alias, success, error) {
        // @alias : String : alias
        // Set alias for the device.
    },
    setTags: function (tags, success, error) {
        // @tags: Array : tags
        // The maximum length of a tag is 128 characters.
    },
    setSoundEnabled: function (enabled, callback) {
        // Note: Android Only, iOS sound settings come in the push
        // Set whether the device makes sound on push.
        // @enabled : Boolean : enabled
    },
    setVibrateEnabled: function (enabled, callback) {
        // Note: Android Only
        // Set whether the device vibrates on push.
    },
    setQuietTimeEnabled: function (enabled, callback) {
        // @enabled : Boolean : enabled
    },
    setQuietTime: function (startHour, startMinute, endHour, endMinute, success, error) {
        // tested:working
        // expected arguments: [QuietTime, success, error]
        // i.e. QuietTime : Object : same format as returned by getQuietTime
        // e.g. {"startHour":0,"startMinute":0,"endHour":0,"endMinute":0}
    },
    setAutobadgeEnabled: function (enabled, callback) {
        // Note: iOS only
        // Enable/disable the Urban Airship Autobadge feature.
    },
    setBadgeNumber: function (number, success, error) {
        // Note: iOS only
    },
    //
    recordCurrentLocation: function (callback) {
        // Report the location of the device.
    }
};
```

## Events

### Incoming Push

This is called when a push is received, but ONLY while the app is active.
See also getIncoming.

```
forge.internal.addEventListener("urbanairship.pushReceived", function (data) {
   var txt = 'pushReceived: '+JSON.stringify(d);
   console.log(txt);
});
```

### Registration

Callback arguments: (Boolean error, String id)

This event is trigerred when your application recieves a registration response from Urban Airship.

```
forge.internal.addEventListener("urbanairship.registration", function (d) {
        var registered = false,
            txt;

        if (!registered) {
            registered = d;
            txt = 'registration: '+JSON.stringify(registered);
            console.log(txt);
        }
});
```



## License (BSD 2-part)

Copyright (c) 2013, On Device Research Ltd.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.