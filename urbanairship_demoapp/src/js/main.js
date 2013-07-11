(function () {
    var success = function (d) {
            forge.logging.log('success :: '+JSON.stringify(d));
        },
        errorfail = function (e) {
            forge.logging.log('errorfail :: '+JSON.stringify(e));
        },
        log = function () {
          return forge.logging.log.apply(this, arguments);
            //return alert.apply(this, arguments);
        }


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

//    forge.urbanairship.enableLocation(
//        function () {
//            alert('enableLocation success');
//        },
//        function (e) {
//            alert('enableLocation fail:'+JSON.stringify(e));
//        }
//    );


    // Register for our native push events
    // this is called when a push is received while the app is active
    forge.internal.addEventListener("urbanairship.pushReceived", function (d) {
        var txt = 'pushReceived: '+JSON.stringify(d);
        log(txt);
//        forge.urbanairship.showAlert(txt); // does nothing
    });

    // Will bring up any existing notification if launched from one
    // i.e. is only called when the app is NOT running and is launched from a push notification
    forge.urbanairship.getIncoming(
        function (d) {
            log('getIncoming: '+JSON.stringify(d));
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
    forge.urbanairship.getPushID(
        function (d) {
            log('getPushID: '+d);
        },
        errorfail
    );
    forge.urbanairship.getQuietTime(
        function (d) {
            log('getQuietTime: '+JSON.stringify(d));
        },
        errorfail
    );
    forge.urbanairship.getTags(
        function (tags) {
            log('getTags: '+tags.join(', '));
        },
        errorfail
    );

    forge.urbanairship.getAlias(
        function (alias) {
            log('getAlias: '+alias);
        },
        errorfail
    );

    // --------------------------------------------------------------------------------------

    forge.urbanairship.setSoundEnabled(1, function () {
        log('setSoundEnabled :: success');

        forge.urbanairship.isSoundEnabled(function (enabled) {
            log('isSoundEnabled :: '+enabled);
        });
    });

    forge.urbanairship.setVibrateEnabled(1, function () {
        log('setVibrateEnabled :: success');

        forge.urbanairship.isVibrateEnabled(function (enabled) {
            log('isVibrateEnabled :: '+enabled);
        });
    });

    forge.urbanairship.setQuietTimeEnabled(1, function () {
        log('setQuietTimeEnabled :: success');

        forge.urbanairship.isQuietTimeEnabled(function (enabled) {
            log('isQuietTimeEnabled :: '+enabled);
        });
    });

    // startup background location services
    // record location
    forge.urbanairship.enableBackgroundLocation(
        function () {
            log('success :: forge.urbanairship.enableBackgroundLocation');
                 //record location 
				forge.urbanairship.recordCurrentLocation(
					function () {
						log('success :: forge.urbanairship.recordCurrentLocation');
					}
				);
        },
        function (e) {
            log('error :: forge.urbanairship.enableBackgroundLocation :: '+JSON.stringify(e) );
        }
    );
    
  
	



}());

