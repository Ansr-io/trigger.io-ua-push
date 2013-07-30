(function () {
    var success = function (d) {
            forge.logging.log('success :: '+JSON.stringify(d));
        },
        errorfail = function (e) {
            forge.logging.log('errorfail :: '+JSON.stringify(e));
        },
        log = function () {
          return forge.logging.log.apply(this, arguments);
        },
        registered = false;


//    forge.urbanairship.disablePush(
//        function (d) {
//            alert('disabled push');
//
//            forge.urbanairship.enablePush(function (d) {
//                alert('enabled push');
//            }, errorfail);
//        },
//        errorfail
//    );

    forge.urbanairship.enablePush(
        function () {
            success('enablePush');

            forge.urbanairship.isPushEnabled(function (d) {
                log('isPushEnabled: '+d);
            });
        },
        errorfail
    );

    forge.internal.addEventListener("urbanairship.registration", function (d) {
        var txt;

        if (!registered) {
            registered = d;
            txt = 'registration: '+JSON.stringify(registered);
            console.log(txt);
            alert(txt);
        }
    });

    // Register for our native push events
    // this is called when a push is received while the app is active
    forge.internal.addEventListener("urbanairship.pushReceived", function (push) {
        if (push && push.message && push.message !== '') {
            txt = 'pushReceived: '+push.message;
            log(txt);
            alert(txt);
        }
    });

    // Will bring up any existing notification if launched from one
    // i.e. is only called when the app is NOT running and is launched from a push notification
    forge.urbanairship.getIncoming(
        function (push) {
            if (push && push.message && push.message !== '') {
                txt = 'getIncoming: '+push.message;
                log(txt);
                alert(txt);
            }
        },
        function (e) {
            log('error :: forge.urbanairship.getIncoming :: '+e);
        }
    );

    // --------------------------------------------------------------------------------------
    forge.urbanairship.setAlias(
        'zacksnexusphone',
        function () {
            log('success :: setAlias');
        },
        errorfail
    );
    forge.urbanairship.setTags(
        ['more', 'awesomeness'],
        function () {
            log('success :: setTags');
        },
        errorfail
    );
    forge.urbanairship.setQuietTime(
        {"startHour":22,"startMinute":0,"endHour":10,"endMinute":0},
        function () {
            log('success :: setQuietTime');

            forge.urbanairship.getQuietTime(
                function (d) {
                    log('getQuietTime: '+JSON.stringify(d));
                },
                errorfail
            );
        },
        errorfail
    );
    // --------------------------------------------------------------------------------------
//    forge.urbanairship.getPushID(
//        function (d) {
//            log('getPushID: '+d);
//        },
//        errorfail
//    );
//    forge.urbanairship.getQuietTime(
//        function (d) {
//            log('getQuietTime: '+JSON.stringify(d));
//        },
//        errorfail
//    );
//    forge.urbanairship.getTags(
//        function (tags) {
//            log('getTags: '+tags.join(', '));
//        },
//        errorfail
//    );
//
//    forge.urbanairship.getAlias(
//        function (alias) {
//            log('getAlias: '+alias);
//        },
//        errorfail
//    );
//

    if (forge.is.ios()) {
        forge.urbanairship.setAutobadgeEnabled(true, function () {
            log('setAutobadgeEnabled :: success');
        });

        forge.urbanairship.registerForNotificationTypes(
            forge.urbanairship.notificationType.alert | forge.urbanairship.notificationType.sound | forge.urbanairship.notificationType.badge,
            function (d) {
                log('registerForNotificationTypes: '+d);
            }
        );
    }

    if (forge.is.android()) {
        forge.urbanairship.setSoundEnabled(true, function () {
            log('setSoundEnabled :: success');

            forge.urbanairship.isSoundEnabled(function (enabled) {
                log('isSoundEnabled :: '+enabled);
            });
        });

        forge.urbanairship.setVibrateEnabled(true, function () {
            log('setVibrateEnabled :: success');

            forge.urbanairship.isVibrateEnabled(function (enabled) {
                log('isVibrateEnabled :: '+enabled);
            });
        });
    }

    // --------------------------------------------------------------------------------------
//    forge.urbanairship.setQuietTimeEnabled(true, function () {
//        log('setQuietTimeEnabled :: success');
//
//        forge.urbanairship.isQuietTimeEnabled(function (enabled) {
//            log('isQuietTimeEnabled :: '+enabled);
//        });
//    });
    // --------------------------------------------------------------------------------------
//    forge.urbanairship.enableLocation(
//        function () {
//            log('enableLocation :: success');
//
//            forge.urbanairship.isLocationEnabled(function (d) {
//                log('isLocationEnabled: '+d);
//            });
//
//            forge.urbanairship.recordCurrentLocation(
//                function () {
//                    log('success :: forge.urbanairship.recordCurrentLocation');
//                }
//            );
//        },
//        function (e) {
//            alert('error :: enableLocation :: '+JSON.stringify(e));
//        }
//    );

    // --------------------------------------------------------------------------------------
//    forge.urbanairship.enableBackgroundLocation(
//        function () {
//            log('enableBackgroundLocation :: success');
//
//            forge.urbanairship.isBackgroundLocationEnabled(function (d) {
//                log('isBackgroundLocationEnabled: '+d);
//            });
//
//            forge.urbanairship.recordCurrentLocation(
//                function () {
//                    log('success :: forge.urbanairship.recordCurrentLocation');
//                }
//            );
//        },
//        function (e) {
//            log('error :: forge.urbanairship.enableBackgroundLocation :: '+JSON.stringify(e) );
//        }
//    );

}());

