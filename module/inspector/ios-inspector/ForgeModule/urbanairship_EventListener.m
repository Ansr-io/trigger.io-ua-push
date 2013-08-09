#import "urbanairship_EventListener.h"
#import "UAPush.h"
#import "UAirship.h"
#import "UAAnalytics.h"
#import "UAAppDelegateSurrogate.h"
#import "UALocationService.h"
#import "UA_SBJsonWriter.h"
#import "urbanairship_API.h"

@implementation urbanairship_EventListener

//
// Here you can implement event listeners.
// These are functions which will get called when certain native events happen.
//

+ (void)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
	[urbanairship_API takeOff:nil];
}

+ (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken {
    // Updates the device token and registers the token with UA
    UALOG(@"PushNotificationPlugin: registered for remote notifications");
    [[UAPush shared] registerDeviceToken:deviceToken];
    NSMutableDictionary *json =[self raiseRegistration:YES withpushID:[UAirship shared].deviceToken];
    [[ForgeApp sharedApp] event:@"urbanairship.registration" withParam:json];
}

+ (void)application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(NSError *) error {
    UALOG(@"PushNotificationPlugin: Failed To Register For Remote Notifications With Error: %@", error);
     NSMutableDictionary *json =[self raiseRegistration:NO withpushID:@""];
     [[ForgeApp sharedApp] event:@"urbanairship.registration" withParam:json];
}

+ (void)application:(UIApplication *)application didReceiveRemoteNotification:(NSDictionary *)userInfo {
    UALOG(@"PushNotificationPlugin: Received remote notification: %@", userInfo);
    
    [[UAPush shared] handleNotification:userInfo applicationState:application.applicationState];
    [[UAPush shared] setBadgeNumber:0]; // zero badge after push received
    
    NSString *alert = [self alertForUserInfo:userInfo];
    NSMutableDictionary *extras = [self extrasForUserInfo:userInfo];
    
    NSMutableDictionary *json = [self raisePush:alert withExtras:extras];
    [[ForgeApp sharedApp] event:@"urbanairship.pushReceived" withParam:json];
}


+ (NSString *)alertForUserInfo:(NSDictionary *)userInfo {
    NSString *alert = @"";
    
    if ([[userInfo allKeys] containsObject:@"aps"]) {
        NSDictionary *apsDict = [userInfo objectForKey:@"aps"];
        //TODO: what do we want to do in the case of a localized alert dictionary?
        if ([[apsDict valueForKey:@"alert"] isKindOfClass:[NSString class]]) {
            alert = [apsDict valueForKey:@"alert"];
        }
    }
    
    return alert;
}

+ (NSMutableDictionary *)extrasForUserInfo:(NSDictionary *)userInfo {
    
    // remove extraneous key/value pairs
    NSMutableDictionary *extras = [NSMutableDictionary dictionaryWithDictionary:userInfo];
    
    if([[extras allKeys] containsObject:@"aps"]) {
        [extras removeObjectForKey:@"aps"];
    }
    if([[extras allKeys] containsObject:@"_uamid"]) {
        [extras removeObjectForKey:@"_uamid"];
    }
    if([[extras allKeys] containsObject:@"_"]) {
        [extras removeObjectForKey:@"_"];
    }
    
    return extras;
}

//events

+ (NSMutableDictionary *)raisePush:(NSString *)message withExtras:(NSDictionary *)extras {
    
    if (!message || !extras) {
        UALOG(@"PushNotificationPlugin: attempted to raise push with nil message or extras");
        message = @"";
        extras = [NSMutableDictionary dictionary];
    }
    
    NSMutableDictionary *data = [NSMutableDictionary dictionary];
    
    [data setObject:message forKey:@"message"];
    [data setObject:extras forKey:@"extras"];
    


    return data;
}

+ (NSMutableDictionary *)raiseRegistration:(BOOL)valid withpushID:(NSString *)pushID {
    
    if (!pushID) {
        UALOG(@"PushNotificationPlugin: attempted to raise registration with nil pushID");
        pushID = @"";
        valid = NO;
    }
    
    NSMutableDictionary *data = [NSMutableDictionary dictionary];
    [data setObject:[NSNumber numberWithBool:valid] forKey:@"valid"];
    [data setObject:pushID forKey:@"pushID"];

    

    return data;
}

@end
