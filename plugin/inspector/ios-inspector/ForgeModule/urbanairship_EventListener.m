#import "urbanairship_EventListener.h"
#import "UAPush.h"
#import "UAirship.h"
#import "UAAnalytics.h"
#import "UAAppDelegateSurrogate.h"
#import "UALocationService.h"
#import "UA_SBJsonWriter.h"

@implementation urbanairship_EventListener

//
// Here you can implement event listeners.
// These are functions which will get called when certain native events happen.
//

//
// Here you can implement event listeners.
// These are functions which will get called when certain native events happen.
//



+ (void)applicationWillTerminate:(UIApplication *)application {
    [UAirship land];
}

+ (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken {
    // Updates the device token and registers the token with UA
    UALOG(@"PushNotificationPlugin: registered for remote notifications");
    [[UAPush shared] registerDeviceToken:deviceToken];
    [self raiseRegistration:YES withpushID:[UAirship shared].deviceToken];
}

+ (void)application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(NSError *) error {
    UALOG(@"PushNotificationPlugin: Failed To Register For Remote Notifications With Error: %@", error);
    [self raiseRegistration:NO withpushID:@""];
}

+ (void)application:(UIApplication *)application didReceiveRemoteNotification:(NSDictionary *)userInfo {
    UALOG(@"PushNotificationPlugin: Received remote notification: %@", userInfo);
    
    [[UAPush shared] handleNotification:userInfo applicationState:application.applicationState];
    [[UAPush shared] setBadgeNumber:0]; // zero badge after push received
    
    NSString *alert = [self alertForUserInfo:userInfo];
    NSMutableDictionary *extras = [self extrasForUserInfo:userInfo];
    
    NSString *json = [self raisePush:alert withExtras:extras];
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

+ (NSString *)raisePush:(NSString *)message withExtras:(NSDictionary *)extras {
    
    if (!message || !extras) {
        UALOG(@"PushNotificationPlugin: attempted to raise push with nil message or extras");
        message = @"";
        extras = [NSMutableDictionary dictionary];
    }
    
    NSMutableDictionary *data = [NSMutableDictionary dictionary];
    
    [data setObject:message forKey:@"message"];
    [data setObject:extras forKey:@"extras"];
    
    UA_SBJsonWriter *writer = [[UA_SBJsonWriter alloc] init] ;
    NSString *json = [writer stringWithObject:data];
    //NSString *js = [NSString stringWithFormat:@"window.pushNotification.pushCallback(%@);", json];
    
    //[self writeJavascript:js];
    
    //UALOG(@"js callback: %@", js);
    return json;
}

+ (void)raiseRegistration:(BOOL)valid withpushID:(NSString *)pushID {
    
    if (!pushID) {
        UALOG(@"PushNotificationPlugin: attempted to raise registration with nil pushID");
        pushID = @"";
        valid = NO;
    }
    
    NSMutableDictionary *data = [NSMutableDictionary dictionary];
    [data setObject:[NSNumber numberWithBool:valid] forKey:@"valid"];
    [data setObject:pushID forKey:@"pushID"];
    
    //UA_SBJsonWriter *writer = [[[UA_SBJsonWriter alloc] init] autorelease];
    //NSString *json = [writer stringWithObject:data];
    //NSString *js = [NSString stringWithFormat:@"window.pushNotification.registrationCallback(%@);", json];
    
    //[self writeJavascript:js];
    
    //UALOG(@"js callback: %@", js);
}

@end
