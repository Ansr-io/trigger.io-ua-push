trigger.io-ua-push
==================

plugin for trigger.io platform allowing integration with push messaging service provided by Urban Airship
Ported and modified with permission, from the official phonegap plugin.

**************************************************************************************
****IMPORTANT THIS PLUGIN REQUIRES THE USE OF BUILD HOOKS - SEE BELOW FOR DETAILS!****
**************************************************************************************

project url
===========
https://github.com/Ansr-io/trigger.io-ua-push

project author
==============
petehobo @ gmail DOT com

project status
==============
Alpha

setup
=====
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

Build Plugin (optional)
=======================

Import the plugin inspectors to your forge workspace.  
Build and upload the libiary versions of the plugin following:

https://trigger.io/docs/current/api/native_plugins/index.html (Section Building/packaging your plugin)


Run Test App
============
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

Android
=======
Update the UA settings file in hooks/postbuild/uaplugin/airshipconfig.properties
Open hooks/postbuild/hook.py - replace the string ‘com.plugtester’ with your app package name


iOS
====
Update the UA settings file in hooks/postbuild/uaplugin/airshipConfig.plist


API
===
For full API details see 
http://docs.urbanairship.com/build/phonegap.html#javascript-api 
https://github.com/urbanairship/phonegap-ua-push
