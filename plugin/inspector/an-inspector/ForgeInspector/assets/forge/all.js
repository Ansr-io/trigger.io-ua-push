/*! Copyright 2011 Trigger Corp. All rights reserved. */
(function(){var k={};var g={};k.config=window.forge.config;g.listeners={};var c={};var f=[];var e=null;var j=false;var l=function(){if(f.length>0){if(!g.debug||window.catalystConnected){j=true;while(f.length>0){var m=f.shift();if(m[0]=="logging.log"){console.log(m[1].message)}g.priv.call.apply(g.priv,m)}j=false}else{e=setTimeout(l,500)}}};g.priv={call:function(t,s,r,n){if((!g.debug||window.catalystConnected||t==="internal.showDebugWarning")&&(f.length==0||j)){var m=k.tools.UUID();var p=true;if(t==="button.onClicked.addListener"||t==="message.toFocussed"){p=false}if(r||n){c[m]={success:r,error:n,onetime:p}}var o={callid:m,method:t,params:s};g.priv.send(o);if(window._forgeDebug){try{o.start=(new Date().getTime())/1000;window._forgeDebug.forge.APICall.apiRequest(o)}catch(q){}}}else{f.push(arguments);if(!e){e=setTimeout(l,500)}}},send:function(m){throw new Error("Forge error: missing bridge to privileged code")},receive:function(m){if(m.callid){if(typeof c[m.callid]===undefined){k.log("Nothing stored for call ID: "+m.callid)}var o=c[m.callid];var n=(typeof m.content==="undefined"?null:m.content);if(o&&o[m.status]){o[m.status](m.content)}if(o&&o.onetime){delete c[m.callid]}if(window._forgeDebug){try{m.end=(new Date().getTime())/1000;window._forgeDebug.forge.APICall.apiResponse(m)}catch(p){}}}else{if(m.event){if(g.listeners[m.event]){g.listeners[m.event].forEach(function(q){if(m.params){q(m.params)}else{q()}})}if(g.listeners["*"]){g.listeners["*"].forEach(function(q){if(m.params){q(m.event,m.params)}else{q(m.event)}})}if(window._forgeDebug){try{m.start=(new Date().getTime())/1000;window._forgeDebug.forge.APICall.apiEvent(m)}catch(p){}}}}}};g.addEventListener=function(m,n){if(g.listeners[m]){g.listeners[m].push(n)}else{g.listeners[m]=[n]}};g.generateQueryString=function(n){if(!n){return""}if(!(n instanceof Object)){return new String(n).toString()}var o=[];var m=function(t,s){if(t===null){return}else{if(t instanceof Array){var q=0;for(var p in t){var r=(s?s:"")+"["+q+"]";q+=1;if(!t.hasOwnProperty(p)){continue}m(t[p],r)}}else{if(t instanceof Object){for(var p in t){if(!t.hasOwnProperty(p)){continue}var r=p;if(s){r=s+"["+p+"]"}m(t[p],r)}}else{o.push(encodeURIComponent(s)+"="+encodeURIComponent(t))}}}};m(n);return o.join("&").replace("%20","+")};g.generateMultipartString=function(n,p){if(typeof n==="string"){return""}var o="";for(var m in n){if(!n.hasOwnProperty(m)){continue}if(n[m]===null){continue}o+="--"+p+"\r\n";o+='Content-Disposition: form-data; name="'+m.replace('"','\\"')+'"\r\n\r\n';o+=n[m].toString()+"\r\n"}return o};g.generateURI=function(n,m){var o="";if(n.indexOf("?")!==-1){o+=n.split("?")[1]+"&";n=n.split("?")[0]}o+=this.generateQueryString(m)+"&";o=o.substring(0,o.length-1);return n+(o?"?"+o:"")};g.disabledModule=function(m,n){var o="The '"+n+"' module is disabled for this app, enable it in your app config and rebuild in order to use this function";k.logging.error(o);m&&m({message:o,type:"UNAVAILABLE",subtype:"DISABLED_MODULE"})};k.enableDebug=function(){g.debug=true;g.priv.call("internal.showDebugWarning",{},null,null);g.priv.call("internal.hideDebugWarning",{},null,null)};setTimeout(function(){if(window.forge&&window.forge.debug){alert("Warning!\n\n'forge.debug = true;' is no longer supported\n\nUse 'forge.enableDebug();' instead.")}},3000);k.is={mobile:function(){return false},desktop:function(){return false},android:function(){return false},ios:function(){return false},chrome:function(){return false},firefox:function(){return false},safari:function(){return false},ie:function(){return false},web:function(){return false},orientation:{portrait:function(){return false},landscape:function(){return false}},connection:{connected:function(){return true},wifi:function(){return true}}};k.is["mobile"]=function(){return true};k.is["android"]=function(){return true};k.is["orientation"]["portrait"]=function(){return g.currentOrientation=="portrait"};k.is["orientation"]["landscape"]=function(){return g.currentOrientation=="landscape"};k.is["connection"]["connected"]=function(){return g.currentConnectionState.connected};k.is["connection"]["wifi"]=function(){return g.currentConnectionState.wifi};var d=function(s,q,t){var o=[];stylize=function(v,u){return v};function m(u){return u instanceof RegExp||(typeof u==="object"&&Object.prototype.toString.call(u)==="[object RegExp]")}function n(u){return u instanceof Array||Array.isArray(u)||(u&&u!==Object.prototype&&n(u.__proto__))}function p(w){if(w instanceof Date){return true}if(typeof w!=="object"){return false}var u=Date.prototype&&Object.getOwnPropertyNames(Date.prototype);var v=w.__proto__&&Object.getOwnPropertyNames(w.__proto__);return JSON.stringify(v)===JSON.stringify(u)}function r(G,D){try{if(G&&typeof G.inspect==="function"&&!(G.constructor&&G.constructor.prototype===G)){return G.inspect(D)}switch(typeof G){case"undefined":return stylize("undefined","undefined");case"string":var u="'"+JSON.stringify(G).replace(/^"|"$/g,"").replace(/'/g,"\\'").replace(/\\"/g,'"')+"'";return stylize(u,"string");case"number":return stylize(""+G,"number");case"boolean":return stylize(""+G,"boolean")}if(G===null){return stylize("null","null")}if(G instanceof Document){return(new XMLSerializer()).serializeToString(G)}var A=Object.keys(G);var H=q?Object.getOwnPropertyNames(G):A;if(typeof G==="function"&&H.length===0){var v=G.name?": "+G.name:"";return stylize("[Function"+v+"]","special")}if(m(G)&&H.length===0){return stylize(""+G,"regexp")}if(p(G)&&H.length===0){return stylize(G.toUTCString(),"date")}var w,E,B;if(n(G)){E="Array";B=["[","]"]}else{E="Object";B=["{","}"]}if(typeof G==="function"){var z=G.name?": "+G.name:"";w=" [Function"+z+"]"}else{w=""}if(m(G)){w=" "+G}if(p(G)){w=" "+G.toUTCString()}if(H.length===0){return B[0]+w+B[1]}if(D<0){if(m(G)){return stylize(""+G,"regexp")}else{return stylize("[Object]","special")}}o.push(G);var y=H.map(function(J){var I,K;if(G.__lookupGetter__){if(G.__lookupGetter__(J)){if(G.__lookupSetter__(J)){K=stylize("[Getter/Setter]","special")}else{K=stylize("[Getter]","special")}}else{if(G.__lookupSetter__(J)){K=stylize("[Setter]","special")}}}if(A.indexOf(J)<0){I="["+J+"]"}if(!K){if(o.indexOf(G[J])<0){if(D===null){K=r(G[J])}else{K=r(G[J],D-1)}if(K.indexOf("\n")>-1){if(n(G)){K=K.split("\n").map(function(L){return"  "+L}).join("\n").substr(2)}else{K="\n"+K.split("\n").map(function(L){return"   "+L}).join("\n")}}}else{K=stylize("[Circular]","special")}}if(typeof I==="undefined"){if(E==="Array"&&J.match(/^\d+$/)){return K}I=JSON.stringify(""+J);if(I.match(/^"([a-zA-Z_][a-zA-Z_0-9]*)"$/)){I=I.substr(1,I.length-2);I=stylize(I,"name")}else{I=I.replace(/'/g,"\\'").replace(/\\"/g,'"').replace(/(^"|"$)/g,"'");I=stylize(I,"string")}}return I+": "+K});o.pop();var F=0;var x=y.reduce(function(I,J){F++;if(J.indexOf("\n")>=0){F++}return I+J.length+1},0);if(x>50){y=B[0]+(w===""?"":w+"\n ")+" "+y.join(",\n  ")+" "+B[1]}else{y=B[0]+w+" "+y.join(", ")+" "+B[1]}return y}catch(C){return"[No string representation]"}}return r(s,(typeof t==="undefined"?2:t))};var h=function(n,o){if("logging" in k.config){var m=k.config.logging.marker||"FORGE"}else{var m="FORGE"}n="["+m+"] "+(n.indexOf("\n")===-1?"":"\n")+n;g.priv.call("logging.log",{message:n,level:o});if(typeof console!=="undefined"){switch(o){case 10:if(console.debug!==undefined&&!(console.debug.toString&&console.debug.toString().match("alert"))){console.debug(n)}break;case 30:if(console.warn!==undefined&&!(console.warn.toString&&console.warn.toString().match("alert"))){console.warn(n)}break;case 40:case 50:if(console.error!==undefined&&!(console.error.toString&&console.error.toString().match("alert"))){console.error(n)}break;default:case 20:if(console.info!==undefined&&!(console.info.toString&&console.info.toString().match("alert"))){console.info(n)}break}}};var a=function(m,n){if(m in k.logging.LEVELS){return k.logging.LEVELS[m]}else{k.logging.__logMessage("Unknown configured logging level: "+m);return n}};var b=function(n){var q=function(r){if(r.message){return r.message}else{if(r.description){return r.description}else{return""+r}}};if(n){var p="\nError: "+q(n);try{if(n.lineNumber){p+=" on line number "+n.lineNumber}if(n.fileName){var m=n.fileName;p+=" in file "+m.substr(m.lastIndexOf("/")+1)}}catch(o){}if(n.stack){p+="\r\nStack trace:\r\n"+n.stack}return p}return""};k.logging={LEVELS:{ALL:0,DEBUG:10,INFO:20,WARNING:30,ERROR:40,CRITICAL:50},debug:function(n,m){k.logging.log(n,m,k.logging.LEVELS.DEBUG)},info:function(n,m){k.logging.log(n,m,k.logging.LEVELS.INFO)},warning:function(n,m){k.logging.log(n,m,k.logging.LEVELS.WARNING)},error:function(n,m){k.logging.log(n,m,k.logging.LEVELS.ERROR)},critical:function(n,m){k.logging.log(n,m,k.logging.LEVELS.CRITICAL)},log:function(n,m,q){if(typeof(q)==="undefined"){var q=k.logging.LEVELS.INFO}try{var o=a(k.config.logging.level,k.logging.LEVELS.ALL)}catch(p){var o=k.logging.LEVELS.ALL}if(q>=o){h(d(n,false,10)+b(m),q)}}};k.internal={ping:function(n,o,m){g.priv.call("internal.ping",{data:[n]},o,m)},call:g.priv.call,addEventListener:g.addEventListener,listeners:g.listeners};var i={};g.currentOrientation=i;g.currentConnectionState=i;g.addEventListener("internal.orientationChange",function(m){if(g.currentOrientation!=m.orientation){g.currentOrientation=m.orientation;g.priv.receive({event:"event.orientationChange"})}});g.addEventListener("internal.connectionStateChange",function(m){if(m.connected!=g.currentConnectionState.connected||m.wifi!=g.currentConnectionState.wifi){g.currentConnectionState=m;g.priv.receive({event:"event.connectionStateChange"})}});k.event={menuPressed:{addListener:function(n,m){g.addEventListener("event.menuPressed",n)}},backPressed:{addListener:function(n,m){g.addEventListener("event.backPressed",function(){n(function(){g.priv.call("event.backPressed_closeApplication",{})})})},preventDefault:function(n,m){g.priv.call("event.backPressed_preventDefault",{},n,m)},restoreDefault:function(n,m){g.priv.call("event.backPressed_restoreDefault",{},n,m)}},messagePushed:{addListener:function(n,m){g.addEventListener("event.messagePushed",n)}},orientationChange:{addListener:function(n,m){g.addEventListener("event.orientationChange",n);if(i&&g.currentOrientation!==i){g.priv.receive({event:"event.orientationChange"})}}},connectionStateChange:{addListener:function(n,m){g.addEventListener("event.connectionStateChange",n);if(i&&g.currentConnectionState!==i){g.priv.receive({event:"event.connectionStateChange"})}}},appPaused:{addListener:function(n,m){g.addEventListener("event.appPaused",n)}},appResumed:{addListener:function(n,m){g.addEventListener("event.appResumed",n)}}};k.reload={updateAvailable:function(n,m){g.priv.call("reload.updateAvailable",{},n,m)},update:function(n,m){g.priv.call("reload.update",{},n,m)},pauseUpdate:function(n,m){g.priv.call("reload.pauseUpdate",{},n,m)},applyNow:function(n,m){k.logging.error("reload.applyNow has been disabled, please see docs.trigger.io for more information.");m({message:"reload.applyNow has been disabled, please see docs.trigger.io for more information.",type:"UNAVAILABLE"})},applyAndRestartApp:function(n,m){g.priv.call("reload.applyAndRestartApp",{},n,m)},switchStream:function(n,o,m){g.priv.call("reload.switchStream",{streamid:n},o,m)},updateReady:{addListener:function(n,m){g.addEventListener("reload.updateReady",n)}},updateProgress:{addListener:function(n,m){g.addEventListener("reload.updateProgress",n)}}};k.tools={UUID:function(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(o){var n=Math.random()*16|0;var m=o=="x"?n:(n&3|8);return m.toString(16)}).toUpperCase()},getURL:function(n,o,m){g.priv.call("tools.getURL",{name:n.toString()},o,m)}};g.priv.send=function(n){if(window.__forge["callJavaFromJavaScript"]===undefined){return}var m=((n.params!==undefined)?JSON.stringify(n.params):"");window.__forge["callJavaFromJavaScript"](n.callid,n.method,m)};g.priv.send({callid:"ready",method:""});k._receive=g.priv.receive;window.forge=k})();(function () {
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
    	suc_f = function (d) {
    		suc_f.cb( JSON.parse(d.tags));
    	}
    	suc_f.cb = success;
    	
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
    setBadgeNumber: function ( text, success, error) {
     if (forge.is.ios())
        forge.internal.call('urbanairship.setBadgeNumber', {text:text}, success, error);
    },
    
//location stuff
	recordCurrentLocation: function (  success) {
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
    registerForNotificationTypes: function ( types, callback) {
     if (forge.is.ios())
        forge.internal.call('urbanairship.registerForNotificationTypes', {text:types}, callback, callback);
    },
    

    
};





})();