## trigger.io-ua-push demo app


### dependencies

The demo app depends on the following forge modules:
 - logging
 - package names


TODO: add instructions to setup via Trigger-Toolkit.app

### manual setup

cd urbanairship_demoapp

edit:
 local_config.json
 src/identity.json




## running the demo app

First you will need to setup Urban Airship account.

Read the [getting started guide](http://docs.urbanairship.com/dashboard/getting_started.html), and follow the setup steps for ios and Android:

[http://docs.urbanairship.com/build/ios.html](http://docs.urbanairship.com/build/ios.html)
[http://docs.urbanairship.com/build/android.html](http://docs.urbanairship.com/build/android.html)

You should then have configured services, e.g.:

Apple Push Notification Service (APNS)
Google Cloud Messaging (GCM)


### module config

The module requires three config files. These files should be stored under the `src/` directory of your app, e.g in `src/fixtures/urbanairship/`.

Review these files, set your API keys and configure location settings.


NB. set gcmSender in airshipconfig.properties equal to GCM Project Number, see [https://code.google.com/apis/console/](https://code.google.com/apis/console/).