package io.trigger.forge.android.modules.urbanairship;

import io.trigger.forge.android.core.ForgeApp;
import io.trigger.forge.android.core.ForgeEventListener;

import com.urbanairship.UAirship;
import com.urbanairship.location.UALocationManager;
import com.urbanairship.push.PushManager;
import android.util.Log;

public class EventListener extends ForgeEventListener {
	
	private static final String TAG = ">>>>> UA_MODULE";
	
	@Override
	public void onApplicationCreate() {	
		Log.v(TAG, "onApplicationCreate");
		UAirship.takeOff(ForgeApp.getApp());
		PushManager.enablePush();
		UALocationManager.init();
		PushManager.shared().setIntentReceiver(IntentReceiver.class);
	}
	
	@Override
    public void onStart() {
		Log.v(TAG, "onStop");
        UAirship.shared().getAnalytics().activityStarted(ForgeApp.getActivity());
    }

    @Override
    public void onStop() {
    	Log.v(TAG, "onStop");
        UAirship.shared().getAnalytics().activityStopped(ForgeApp.getActivity());
    }
}
