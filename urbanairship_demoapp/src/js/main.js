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
        function (d) {
            success(d);

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

//    forge.urbanairship.enablePush(success, errorfail);

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
            console.log('error :: forge.urbanairship.getIncoming :: '+e);
        }
    );

    // --------------------------------------------------------------------------------------
//    forge.urbanairship.setAlias(
//        'zacksnexusphone',
//        function (d) {
//            alert('setAlias: '+JSON.stringify(d));
//        },
//        errorfail
//    );
//    forge.urbanairship.setTags(
//        ['more', 'awesomeness'],
//        function (d) {
//            alert('setTags: '+JSON.stringify(d));
//        },
//        errorfail
//    );
//    forge.urbanairship.setQuietTime(
//        22,0,10,0,
//        function (d) {
//            alert('setQuietTime: '+JSON.stringify(d));
//
//            forge.urbanairship.getQuietTime(
//                function (d) {
//                    alert('getQuietTime: '+JSON.stringify(d));
//                },
//                errorfail
//            );
//        },
//        errorfail
//    );
    // --------------------------------------------------------------------------------------
    forge.urbanairship.getPushID(
        function (d) {
            log('getPushID: '+d);
        },
        errorfail
    );
    forge.urbanairship.setAlias(
       'zacksnexusphone',
       function (d) {
           log('setAlias: '+JSON.stringify(d));
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
        function (d) {
//            var tags = JSON.parse(d.tags);
            log('getTags: '+d.join(', '));
            log('tags: '+d[0]);
        },
        errorfail
    );

    forge.urbanairship.getAlias(
        function (d) {
            log('getAlias: '+JSON.stringify(d));
        },
        errorfail
    );
    // --------------------------------------------------------------------------------------

    //startup background location services
//    forge.urbanairship.enableBackgroundLocation(
//        function (d) {
//            log('success :: forge.urbanairship.enableBackgroundLocation :: '+d);
//        },
//        function (e) {
//            log('error :: forge.urbanairship.enableBackgroundLocation :: '+JSON.stringify(e) );
//        }
//    );



}());

