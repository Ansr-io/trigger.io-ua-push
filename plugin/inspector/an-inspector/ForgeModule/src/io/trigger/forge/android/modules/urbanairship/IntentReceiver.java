/*
Copyright 2009-2011 Urban Airship Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE URBAN AIRSHIP INC ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL URBAN AIRSHIP INC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
//modified for trigger.io by Petehobson.com 2013


package io.trigger.forge.android.modules.urbanairship;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.RemoteException;
import android.util.Log;

import com.urbanairship.Logger;
import com.urbanairship.UAirship;
import com.urbanairship.location.UALocationManager;
import com.urbanairship.push.PushManager;
import com.urbanairship.util.ServiceNotBoundException;

import io.trigger.forge.android.core.ForgeActivity;
import io.trigger.forge.android.core.ForgeApp;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class IntentReceiver extends BroadcastReceiver {

    private static final String logTag = "PushSample";

    public static String APID_UPDATED_ACTION_SUFFIX = ".apid.updated";

    private Map<String, String> getNotificationExtras(Intent intent) {
        Map<String, String> extrasMap = new HashMap<String, String>();

        Set<String> keys = intent.getExtras().keySet();
        for (String key : keys) {

            // ignore standard C2DM extra key
            List<String> ignoredKeys = (List<String>) Arrays.asList(
                    "collapse_key",// c2dm collapse key
                    "from",// c2dm sender
                    PushManager.EXTRA_NOTIFICATION_ID,// int id of generated
                    // notification
                    // (ACTION_PUSH_RECEIVED
                    // only)
                    PushManager.EXTRA_PUSH_ID,// internal UA push id
                    PushManager.EXTRA_ALERT);// ignore alert
            if (ignoredKeys.contains(key)) {
                continue;
            }

            extrasMap.put(key, intent.getStringExtra(key));
        }

        return extrasMap;
    }   
 
    @Override
    public void onReceive(Context context, Intent intent) {
        Logger.info("Received intent: " + intent.toString());
        String action = intent.getAction();

        if (action.equals(PushManager.ACTION_PUSH_RECEIVED)) {
            int id = intent.getIntExtra(PushManager.EXTRA_NOTIFICATION_ID, 0);

            String alert = intent.getStringExtra(PushManager.EXTRA_ALERT);
            Map<String, String> extras = getNotificationExtras(intent);

            Logger.info("Received push notification. Alert: " + alert
                    + ". Payload: " + extras.toString() + ". NotificationID="
                    + id);

           // PushNotificationPlugin plugin = PushNotificationPlugin
            //        .getInstance();
            Logger.info("Got Extras: " + extras);
            Logger.info("Got Alert: " + alert);

            API.raisePush(alert, extras);

        } else if (action.equals(PushManager.ACTION_NOTIFICATION_OPENED)) {

            String alert = intent.getStringExtra(PushManager.EXTRA_ALERT);
            Map<String, String> extras = getNotificationExtras(intent);

            Logger.info("User clicked notification. Message: " + alert
                    + ". Payload: " + extras.toString());

            Intent launch = new Intent(Intent.ACTION_MAIN);
            launch.setClass(UAirship.shared().getApplicationContext(), 
                    ForgeActivity.class);
            //TODO set above class to dynmaic property
            launch.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP);

            API.incomingAlert = alert;
            API.incomingExtras = extras;

            Logger.info("Plugin Awesome user clicked!");

            UAirship.shared().getApplicationContext().startActivity(launch);

        } else if (action.equals(PushManager.ACTION_REGISTRATION_FINISHED)) {

            String apid = intent.getStringExtra(PushManager.EXTRA_APID);
            Boolean valid = intent.getBooleanExtra(
                    PushManager.EXTRA_REGISTRATION_VALID, false);
            Logger.info("Registration complete. APID:"
                    + intent.getStringExtra(PushManager.EXTRA_APID)
                    + ". Valid: "
                    + intent.getBooleanExtra(
                            PushManager.EXTRA_REGISTRATION_VALID, false));
            API.raiseRegistration(valid, apid);

        } else if (action
                .equals(UALocationManager.getLocationIntentAction(UALocationManager.ACTION_SUFFIX_LOCATION_SERVICE_BOUND))) {
            try {
                UALocationManager.shared().recordCurrentLocation();
                Logger.info("Location successfully recorded on Intent");
            } catch (ServiceNotBoundException e) {
                Logger.error("Recording current location on Intent failed");
                e.printStackTrace();
            } catch (RemoteException e) {
                Logger.error("zomg flailsauce");
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    } 
   
}

