package io.trigger.forge.android.modules.urbanairship;

import io.trigger.forge.android.core.ForgeApp;
import io.trigger.forge.android.core.ForgeEventListener;

import com.urbanairship.UAirship;
import com.urbanairship.location.UALocationManager;
import com.urbanairship.push.PushManager;

public class EventListener extends ForgeEventListener {
	@Override
	public void onApplicationCreate() {
		UAirship.takeOff(ForgeApp.getApp());
		PushManager.enablePush();
		UALocationManager.init();
		PushManager.shared().setIntentReceiver(IntentReceiver.class);
	}
	
	@Override
    public void onStop() {
        UAirship.land();
    }
}
