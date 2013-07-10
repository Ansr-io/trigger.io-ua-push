## trigger.io-ua-push

plugin for trigger.io platform allowing integration with push messaging service provided by Urban Airship
Ported and modified with permission, from the official phonegap plugin.

###License (BSD 2-part)

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
        // does nothing ????
        // remove this - or fix it.
    },
    enablePush: function ( success, error) {
        // Enable push notifications on the device. This sends a registration to the backend service.
    },
    disablePush: function ( success, error) {
        // Disable push notifications on the device. The device will no longer recieve push notifications.
    },
    enableLocation: function ( success, error) {
        // Enable location updates on the device.
    },
    disableLocation: function ( success, error) {
        // Disable location updates on the device.
    },
    enableBackgroundLocation: function ( success, error) {
        // Enable background location updates on the device.
    },
    disableBackgroundLocation: function (success, error) {
        // Disable background location updates on the device.
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
    }
};
forge.internal.addEventListener("urbanairship.pushReceived", function (data) {
    // Register for our native push events
    // this is called when a push is received: ONLY while the app is active
    // see also getIncoming
});
```
