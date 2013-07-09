package io.trigger.forge.android.modules.urbanairship;


import com.urbanairship.UAirship;
import com.urbanairship.push.PushManager;

import io.trigger.forge.android.core.ForgeApp;

/* 
* Trigger.io does not yet allow plugging into the 
* Application onCreate event.  As we need an app context,
* create a shim instead.
* NB build hooks modify the generated manifest to launch this
* app
*/
public class UAShim extends ForgeApp {
	@Override
	public void onCreate() {
		
	    super.onCreate();
	    UAirship.takeOff(this);
	    PushManager.enablePush();
		PushManager.shared().setIntentReceiver(IntentReceiver.class);	

	    
	}
}
