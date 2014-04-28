	// Expose the native API to javascript
forge.urbanairship	 = {

    enablePush: function ( success, error) {
        forge.internal.call('urbanairship.enablePush', {}, success, error);
    } 
,
    disablePush: function ( success, error) {
        forge.internal.call('urbanairship.disablePush', {}, success, error);
    }  
,
    enableLocation: function ( success, error) {
        forge.internal.call('urbanairship.enableLocation', {}, success, error);
    }  
,
    disableLocation: function ( success, error) {
        forge.internal.call('urbanairship.disableLocation', {}, success, error);
    }  
,
    enableBackgroundLocation: function ( success, error) {
        forge.internal.call('urbanairship.enableBackgroundLocation', {}, success, error);
    }  
,
    disableBackgroundLocation: function ( success, error) {
        forge.internal.call('urbanairship.disableBackgroundLocation', {}, success, error);
    }  
,
// is* functions

    isPushEnabled: function ( success) {
        forge.internal.call('urbanairship.isPushEnabled', {}, success, function(){});
    } ,   
    isSoundEnabled: function ( success) {
        forge.internal.call('urbanairship.isSoundEnabled', {}, success, function(){});
    } ,   
    isVibrateEnabled: function ( success) {
        forge.internal.call('urbanairship.isVibrateEnabled', {}, success, function(){});
    } ,   
    isQuietTimeEnabled: function ( success) {
        forge.internal.call('urbanairship.isQuietTimeEnabled', {}, success, function(){});
    } ,   
    isInQuietTime: function ( success) {
        forge.internal.call('urbanairship.isInQuietTime', {}, success, function(){});
    } ,   
    isLocationEnabled: function ( success) {
        forge.internal.call('urbanairship.isLocationEnabled', {}, success, function(){});
    } ,   
    isBackgroundLocationEnabled: function ( success) {
        forge.internal.call('urbanairship.isBackgroundLocationEnabled', {}, success, function(){});
    },  
    
// Getters  
    getIncoming: function ( success, error) {
        forge.internal.call('urbanairship.getIncoming', {}, success, error);
    },   
    getPushID: function ( success, error) {
        forge.internal.call('urbanairship.getPushID', {}, success, error);
    },   
    getQuietTime: function ( success, error) {
        forge.internal.call('urbanairship.getQuietTime', {}, success, error);
    },   
    getTags: function ( success, error) {
    	var suc_f = function (d) {
    		success( JSON.parse(d.tags) );
    	}
        forge.internal.call('urbanairship.getTags', {}, suc_f, error);
    },   
    getAlias: function ( success, error) {
        forge.internal.call('urbanairship.getAlias', {}, success, error);
    },      

//setters
    setAlias: function (text, success, error) {
        forge.internal.call('urbanairship.setAlias', {text:text}, success, error);
    },  
    setTags: function (tags, success, error) {
        forge.internal.call('urbanairship.setTags', {"tags":tags}, success, error);
    },   
    setSoundEnabled: function (text, success, error) {
        forge.internal.call('urbanairship.setSoundEnabled', {text:(text ? 1 :0)}, success, error);
    },   
    setVibrateEnabled: function (text, success, error) {
     if (forge.is.android())
        forge.internal.call('urbanairship.setVibrateEnabled', {text:(text ? 1 :0)}, success, error);
    else {
    	success();
    }
    },   
    setQuietTimeEnabled: function (text,  success, error) {
        forge.internal.call('urbanairship.setQuietTimeEnabled', {text:(text ? 1 :0)}, success, error);
    },   
    setQuietTime: function (quiteTimeDef, success, error) {
        forge.internal.call('urbanairship.setQuietTime', quiteTimeDef, success, error);
    },
    setAutobadgeEnabled: function (text, success, error) {
        if (forge.is.ios())
            forge.internal.call('urbanairship.setAutobadgeEnabled', {text:(text ? 1 :0)}, success, error);
    },
    setBadgeNumber: function (text, success, error) {
        if (forge.is.ios())
            forge.internal.call('urbanairship.setBadgeNumber', {text:text}, success, error);
    },
    
//location stuff
	recordCurrentLocation: function (success) {
        forge.internal.call('urbanairship.recordCurrentLocation', {}, success, success);
    },
//registration  
// Types

	notificationType : {
 		none: 0,
    	badge: 1,
      	sound: 2,
        alert: 4
    } ,
    registerForNotificationTypes: function (types, callback) {
     if (forge.is.ios())
        forge.internal.call('urbanairship.registerForNotificationTypes', {text:types}, callback, callback);
    },

    // Event handlers
    pushReceived: {
        addListener: function (callback) {
            forge.internal.addEventListener("urbanairship.pushReceived", callback);
        }
    },
    clickReceived: {
        addListener: function (callback) {
            forge.internal.addEventListener("urbanairship.clickReceived", callback);
        }
    }
};