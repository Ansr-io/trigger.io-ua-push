package io.trigger.forge.android.modules.urbanairship;

import io.trigger.forge.android.core.ForgeApp;
import io.trigger.forge.android.core.ForgeParam;
import io.trigger.forge.android.core.ForgeTask;

import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import android.os.RemoteException;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonIOException;
import com.google.gson.JsonObject;
import com.urbanairship.Logger;
import com.urbanairship.location.UALocationManager;
import com.urbanairship.push.PushManager;
import com.urbanairship.util.ServiceNotBoundException;

public class API {
	
    static public String incomingAlert = "";
    static public Map<String, String> incomingExtras = new HashMap<String, String>();	
	
    public static Boolean locationTakeOff = true;
	public static Boolean takeOff = true;
	
    private static JsonObject notificationObject(String message, Map<String, String> extras) {
    	JsonObject data = new JsonObject();
        try {
            data.addProperty("message", message);
            Gson gson = new GsonBuilder().create();
            String json = gson.toJson(extras);
            data.addProperty("extras", json);
        } catch (JsonIOException e) {
            //Logger.error("Error constructing notification object", e);
        }
        return data;
    }
 
   //Event emitters
    public static  void raisePush(String message, Map<String, String> extras) {
    	
        JsonObject data = notificationObject(message, extras);
        Logger.info("raisePush: " + data);

        try {
        	ForgeApp.event("urbanairship.pushReceived", data);
        }
        catch (Exception e) {
            Logger.error("unexpected exception in raisePush", e);
        }
        
    }

    public static  void raiseClick(String message, Map<String, String> extras) {
        
        JsonObject data = notificationObject(message, extras);
        Logger.info("raiseClick: " + data);

        try {
            ForgeApp.event("urbanairship.clickReceived", data);
        }
        catch (Exception e) {
            Logger.error("unexpected exception in raiseClick", e);
        }
        
    }
    
    public static void raiseRegistration(Boolean valid, String pushID) {
    	
    	JsonObject data = new JsonObject();
        try {
            data.addProperty("valid", valid);
            data.addProperty("pushID", pushID);
        } catch (Exception e) {
            Logger.error("Error In raiseRegistration", e);
        }
 

        try {
        	ForgeApp.event("urbanairship.registration", data);
        } catch (NullPointerException npe) {
            Logger.info("unable to send javascript in raiseRegistration");
        } catch (Exception e) {
            Logger.error("unexpected exception in raisePush", e);
        }
        
    }
   
	// Top level enabling/disabling
    


	public static void enablePush(final ForgeTask callbackContext) {
		if (requirePushServiceEnabled(callbackContext)) {
            PushManager.enablePush();
           // PushManager.shared().setIntentReceiver(PushNotificationPluginIntentReceiver.class);
            callbackContext.success();
        }
	}
	public static void disablePush(final ForgeTask callbackContext) {
		if (requirePushServiceEnabled(callbackContext)) {
	        PushManager.disablePush();
	        callbackContext.success();
	    }
	}
	public static void enableLocation(final ForgeTask callbackContext) {
		if (requireLocationServiceEnabled(callbackContext)) {
            UALocationManager.enableLocation();            
            callbackContext.success();
        }
	}
	public static void disableLocation(final ForgeTask callbackContext) {
        if (requireLocationServiceEnabled(callbackContext)) {
            UALocationManager.disableLocation();
            callbackContext.success();
        }
	}
	public static void enableBackgroundLocation(final ForgeTask callbackContext) {
        if (requireLocationServiceEnabled(callbackContext)) {
            UALocationManager.enableBackgroundLocation();
            callbackContext.success();
        }
	}
	public static void disableBackgroundLocation(final ForgeTask callbackContext) {
        if (requireLocationServiceEnabled(callbackContext)) {
            UALocationManager.disableBackgroundLocation();
            callbackContext.success();
        }
	}
	
	// is* functions
	
	public static void isPushEnabled(final ForgeTask callbackContext) {
        if (requirePushServiceEnabled(callbackContext)) {
            Boolean value =PushManager.shared().getPreferences().isPushEnabled();
            callbackContext.success(value);
        }
	}
	public static void isSoundEnabled(final ForgeTask callbackContext) {
        if (requirePushServiceEnabled(callbackContext)) {
            Boolean value =PushManager.shared().getPreferences().isSoundEnabled();
            callbackContext.success(value);
        }
	}
	public static void isVibrateEnabled(final ForgeTask callbackContext) {
        if (requirePushServiceEnabled(callbackContext)) {
            Boolean value =PushManager.shared().getPreferences().isVibrateEnabled();
            callbackContext.success(value);
        }
	}
	public static void isQuietTimeEnabled(final ForgeTask callbackContext) {
        if (requirePushServiceEnabled(callbackContext)) {
            Boolean value =PushManager.shared().getPreferences().isQuietTimeEnabled();
            callbackContext.success(value);
        }
	}
	public static void isInQuietTime(final ForgeTask callbackContext) {
        if (requirePushServiceEnabled(callbackContext)) {
            Boolean value =PushManager.shared().getPreferences().isInQuietTime();
            callbackContext.success(value);
        }
	}
	public static void isLocationEnabled(final ForgeTask callbackContext) {
       // if (requireLocationServiceEnabled(callbackContext)) {
            Boolean value =  UALocationManager.shared().getPreferences().isLocationEnabled();
            callbackContext.success(value);
        //}
	}
	
	public static void isBackgroundLocationEnabled(final ForgeTask callbackContext) {
        if (requireLocationServiceEnabled(callbackContext)) {
            Boolean value =  UALocationManager.shared().getPreferences().isBackgroundLocationEnabled();
            callbackContext.success(value);
        }
	}
	
// Getters
	public static void getIncoming(final ForgeTask callbackContext) {
		String alert = incomingAlert;
		Map<String, String> extras = incomingExtras;
	    JsonObject obj = notificationObject(alert, extras);

	    callbackContext.success(obj);

	    //reset incoming push data until the next background push comes in
	    incomingAlert = "";
	    incomingExtras = new HashMap<String,String>();
	}
	public static void getPushID(final ForgeTask callbackContext) {
        if (requirePushServiceEnabled(callbackContext)) {
            String pushID = PushManager.shared().getAPID();
            pushID = pushID != null ? pushID : "";
            callbackContext.success(pushID);
        }
	}
	public static void getQuietTime(final ForgeTask callbackContext) {
        if (!requirePushServiceEnabled(callbackContext)) {
            return;
        }

        Date[] quietTime = PushManager.shared().getPreferences().getQuietTimeInterval();

        int startHour = 0;
        int startMinute = 0;
        int endHour = 0;
        int endMinute = 0;

        if (quietTime != null) {
            Calendar start 		= new GregorianCalendar();
            Calendar end 		= new GregorianCalendar();
            start.setTime		(quietTime[0]);
            end.setTime			(quietTime[1]);

            startHour 			= start.get(Calendar.HOUR_OF_DAY);
            startMinute 		= start.get(Calendar.MINUTE);
            endHour 			= end.get(Calendar.HOUR_OF_DAY);
            endMinute 			= end.get(Calendar.MINUTE);
        }

        try {
            JsonObject returnObject = new JsonObject();
            returnObject.addProperty("startHour", startHour);
            returnObject.addProperty("startMinute", startMinute);
            returnObject.addProperty("endHour", endHour);
            returnObject.addProperty("endMinute", endMinute);
          
            callbackContext.success(returnObject);
        } catch (JsonIOException e ) {
            callbackContext.error("Error building quietTime JSON");
        }
	}
	public static void getTags(final ForgeTask callbackContext) {
        if (!requirePushServiceEnabled(callbackContext)) {
            return;
        }

        Set<String> tags = PushManager.shared().getTags();
        try {
        	JsonObject returnObject = new JsonObject();
            Gson gson = new GsonBuilder().create();
            String json = gson.toJson(tags);
            
            returnObject.addProperty("tags", json);           
            callbackContext.success(returnObject);
        } catch (JsonIOException e) {
           
            callbackContext.error("Error building tags JSON");
        }
	}
	
	public static void getAlias(final ForgeTask callbackContext) {

        if (requirePushServiceEnabled(callbackContext)) {
            String alias = PushManager.shared().getAlias();
            alias = alias != null ? alias : "";
            callbackContext.success(alias);
        }
	}

//setters

	public static void setAlias(final ForgeTask callbackContext, @ForgeParam("text") final String text) {
		Logger.debug("setAlias"+ text.toString());
		PushManager.shared().setAlias(text);
        callbackContext.success();
	}
	public static void setTags(final ForgeTask callbackContext,  @ForgeParam("tags") final JsonArray tagsArray) {
		if (!requirePushServiceEnabled(callbackContext)) {
            return;
        }
		try {
           HashSet<String> tagSet = new HashSet<String>();
         
           for (int i = 0; i < tagsArray.size(); ++i) {
               tagSet.add(tagsArray.get(i).getAsString());
           }

           PushManager.shared().setTags(tagSet);
           Logger.debug("Settings tags: " + tagSet);  
           callbackContext.success();
           
		} catch (JsonIOException e) {
           Logger.error("Error reading tags JSON", e);
           callbackContext.error("Error reading tags JSON");
		}	 
	}
	public static void setSoundEnabled(final ForgeTask callbackContext, @ForgeParam("text") final int text) {
        if (!requirePushServiceEnabled(callbackContext)) {
            return;
        }

        try {
            boolean soundPreference = text !=0;
            PushManager.shared().getPreferences().setSoundEnabled(soundPreference);
            Logger.debug("Settings Sound: " + soundPreference);
            callbackContext.success();
        } catch (JsonIOException e) {
            Logger.error("Error reading soundEnabled in callback", e);
            callbackContext.error("Error reading soundEnabled in callback");
        }
	}
	public static void setVibrateEnabled(final ForgeTask callbackContext, @ForgeParam("text") final int text) {
        if (!requirePushServiceEnabled(callbackContext)) {
            return;
        }

        try {
            boolean preference = text !=0;
            PushManager.shared().getPreferences().setVibrateEnabled(preference);
            Logger.debug("Settings Sound: " + preference);
            callbackContext.success();
        } catch (JsonIOException e) {
            Logger.error("Error reading soundEnabled in callback", e);
            callbackContext.error("Error reading soundEnabled in callback");
        }
	}
	public static void setQuietTimeEnabled(final ForgeTask callbackContext, @ForgeParam("text") final int text) {
        if (!requirePushServiceEnabled(callbackContext)) {
            return;
        }

        try {
            boolean preference = text !=0;
            PushManager.shared().getPreferences().setQuietTimeEnabled(preference);
            Logger.debug("Settings Sound: " + preference);
            callbackContext.success();
        } catch (JsonIOException e) {
            Logger.error("Error reading soundEnabled in callback", e);
            callbackContext.error("Error reading soundEnabled in callback");
        }
	}
	
	public static void setQuietTime(final ForgeTask callbackContext,  @ForgeParam("startHour") final int startHour, @ForgeParam("startMinute") final int startMinute, @ForgeParam("endHour") final int endHour, @ForgeParam("endMinute") final int endMinute) {
        if (!requirePushServiceEnabled(callbackContext)) {
            return;
        }

        try {
            Calendar start = new GregorianCalendar();
            Calendar end = new GregorianCalendar();

            start.set(Calendar.HOUR_OF_DAY, startHour);
            start.set(Calendar.MINUTE, startMinute);
            end.set(Calendar.HOUR_OF_DAY, endHour);
            end.set(Calendar.MINUTE, endMinute);

            Logger.debug("Settings QuietTime. Start: " + start.getTime() + ", End: " + end.getTime());
            PushManager.shared().getPreferences().setQuietTimeInterval(start.getTime(), end.getTime());
            callbackContext.success();
        } catch (JsonIOException e) {
            Logger.error("Error reading quietTime JSON", e);
            callbackContext.error("Error reading quietTime JSON");
        }
	}

	//location stuff
	public static void recordCurrentLocation(final ForgeTask callbackContext) {	
	    if (!requireLocationServiceEnabled(callbackContext)) {
	        return;
	    }

	    try {
	        Logger.debug("LOGGING LOCATION");	
	        UALocationManager.shared().recordCurrentLocation();
	    } catch (ServiceNotBoundException e) {
	        Logger.debug("Location not bound, binding now");
	        UALocationManager.bindService();
	    } catch (RemoteException e) {
	        Logger.error("Caught RemoteException in recordCurrentLocation", e);
	    } catch (Exception e) {
	    	 Logger.error("Exception in recordCurrentLocation", e);
	    }
	    
	    callbackContext.success();
	}
	

	// Helpers
    public static  boolean requirePushServiceEnabled(final ForgeTask callbackContext) {
    	/*
        if (!UAirship.shared().getAirshipConfigOptions().pushServiceEnabled) {
           // Logger.warn("pushServiceEnabled must be enabled in the airshipconfig.properties file");
            callbackContext.error("pushServiceEnabled must be enabled in the airshipconfig.properties file");
            return false;
        }
		*/
        return true;
        
    }

    private static boolean requireLocationServiceEnabled(final ForgeTask callbackContext) {
    	if (locationTakeOff == false) {
    		UALocationManager.init();
    		locationTakeOff = true;
    	}
        return true;
    }
	
}
