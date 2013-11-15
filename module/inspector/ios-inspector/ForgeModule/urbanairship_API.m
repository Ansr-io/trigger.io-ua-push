#import "urbanairship_API.h"
#import "UAPush.h"

#import "UAirship.h"

#import "UAAnalytics.h"

#import "UAAppDelegateSurrogate.h"

#import "UALocationService.h"

#import "UAConfig.h"

#import <Foundation/Foundation.h>

@implementation urbanairship_API

//additions petehobson.com



+(void)takeOff:(ForgeTask*) command {
	NSUserDefaults *prefs = [NSUserDefaults standardUserDefaults];
	NSString *assetsFolder = [[ForgeApp sharedApp] assetsFolderLocationWithPrefs:prefs];
	NSString *configPath = [[assetsFolder stringByAppendingPathComponent:@"src"] stringByAppendingPathComponent:[[[ForgeApp sharedApp] configForModule:@"urbanairship"] objectForKey:@"airshipConfigPlist"]];
	UAConfig* config = [UAConfig configWithContentsOfFile:configPath];
	
	[UAirship takeOff:config];    
    
    // Register for notifications
    [[UAPush shared]
     registerForRemoteNotificationTypes:(UIRemoteNotificationTypeBadge |
                                         UIRemoteNotificationTypeSound |
                                         UIRemoteNotificationTypeAlert)];
	
    [[UAPush shared] setDelegate:self];
    
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




//registration

+(void)registerForNotificationTypes:(ForgeTask*)command text:(NSNumber *)text {
    UALOG(@"PushNotificationPlugin: register for notification types");
    
   
        UIRemoteNotificationType bitmask = text ;
        UALOG(@"bitmask value: %d", text);
        [[UAPush shared] registerForRemoteNotificationTypes:bitmask];
        [command success:nil];
        //[command success:nil];
}

//general enablement

+ (void)enablePush:(ForgeTask*)command {
    [UAPush shared].pushEnabled = YES;
    //forces a reregistration
    [[UAPush shared] updateRegistration];
    [command success:nil];
    
}

+ (void)disablePush:(ForgeTask*)command {
    [UAPush shared].pushEnabled = NO;
    //forces a reregistration
    [[UAPush shared] updateRegistration];
    [command success:nil];
    
}

+ (void)enableLocation:(ForgeTask*)command {
    [UALocationService setAirshipLocationServiceEnabled:YES];
    [command success:nil];
    
}

+ (void)disableLocation:(ForgeTask*)command {
    [UALocationService setAirshipLocationServiceEnabled:NO];
    [command success:nil];
    
}

+ (void)enableBackgroundLocation:(ForgeTask*)command {
    [UAirship shared].locationService.backgroundLocationServiceEnabled = YES;
    [command success:nil];
    
}

+ (void)disableBackgroundLocation:(ForgeTask*)command {
    [self takeOff:command];
    [UAirship shared].locationService.backgroundLocationServiceEnabled = NO;
    [command success:nil];
    
}

//getters

+ (void)isVibrateEnabled:(ForgeTask*)command {
    //no vibrate on IOS
    [command success:[NSNumber numberWithBool:false]];
    
}

+ (void)isPushEnabled:(ForgeTask*)command {
    [self takeOff:command];
    BOOL enabled = [UAPush shared].pushEnabled;
    [command success:[NSNumber numberWithBool:enabled]];
    
    
}

+ (void)isQuietTimeEnabled:(ForgeTask*)command {
    BOOL enabled = [UAPush shared].quietTimeEnabled;
    [command success:[NSNumber numberWithBool:enabled]];
}

+(void)isInQuietTime:(ForgeTask*)command {
    BOOL inQuietTime;
    NSDictionary *quietTimeDictionary = [UAPush shared].quietTime;
    if (quietTimeDictionary) {
        NSString *start = [quietTimeDictionary valueForKey:@"start"];
        NSString *end = [quietTimeDictionary valueForKey:@"end"];
        
        NSDateFormatter *df = [NSDateFormatter new];
        df.locale = [[NSLocale alloc] initWithLocaleIdentifier:@"en_US_POSIX"] ;
        df.dateFormat = @"HH:mm";
        
        NSDate *startDate = [df dateFromString:start];
        NSDate *endDate = [df dateFromString:end];
        
        NSDate *now = [NSDate date];
        
        inQuietTime = ([now earlierDate:startDate] == startDate && [now earlierDate:endDate] == now);
    } else {
        inQuietTime = NO;
    }
    
    [command success:[NSNumber numberWithBool:inQuietTime]];
    
}

+ (void)isLocationEnabled:(ForgeTask*)command {
    BOOL enabled = [UALocationService airshipLocationServiceEnabled];
    [command success:[NSNumber numberWithBool:enabled]];
    
}

+ (void)isBackgroundLocationEnabled:(ForgeTask*)command {
    BOOL enabled = [UAirship shared].locationService.backgroundLocationServiceEnabled;
    [command success:[NSNumber numberWithBool:enabled]];
    
}

+ (void)getIncoming:(ForgeTask*)command {
    NSString *incomingAlert = @"";
    NSMutableDictionary *incomingExtras = [NSMutableDictionary dictionary];
   
    NSDictionary *launchOptions = [UAAppDelegateSurrogate shared].launchOptions;
    if ([[launchOptions allKeys]containsObject:@"UIApplicationLaunchOptionsRemoteNotificationKey"]) {
        NSDictionary *payload = [launchOptions objectForKey:@"UIApplicationLaunchOptionsRemoteNotificationKey"];
        incomingAlert = [self alertForUserInfo:payload];
        [incomingExtras setDictionary:[self extrasForUserInfo:payload]];
    }
    
    NSMutableDictionary *returnDictionary = [NSMutableDictionary dictionary];
    
    [returnDictionary setObject:incomingAlert forKey:@"message"];
    [returnDictionary setObject:incomingExtras forKey:@"extras"];
    
    //reset incoming push data until the next background push comes in
    //todo
    [[UAAppDelegateSurrogate shared] clearLaunchOptions];
    
    [command success:returnDictionary];
}

+ (void)getPushID:(ForgeTask*)command {
    NSString *pushID = [UAirship shared].deviceToken ?: @"";
    [command success:pushID];
}

+ (void)getQuietTime:(ForgeTask*)command {
    NSDictionary *quietTimeDictionary = [UAPush shared].quietTime;
    //initialize the returned dictionary with zero values
    NSNumber *zero = [NSNumber numberWithInt:0];
    NSDictionary *returnDictionary = [NSDictionary dictionaryWithObjectsAndKeys:zero,@"startHour",
                                      zero,@"startMinute",
                                      zero,@"endHour",
                                      zero,@"endMinute",nil];
    //this can be nil if quiet time is not set
    if (quietTimeDictionary) {
        
        NSString *start = [quietTimeDictionary objectForKey:@"start"];
        NSString *end = [quietTimeDictionary objectForKey:@"end"];
        
        NSDateFormatter *df = [NSDateFormatter new] ;
        df.locale = [[NSLocale alloc] initWithLocaleIdentifier:@"en_US_POSIX"] ;
        df.dateFormat = @"HH:mm";
        
        NSDate *startDate = [df dateFromString:start];
        NSDate *endDate = [df dateFromString:end];
        
        //these will be nil if the dateformatter can't make sense of either string
        if (startDate && endDate) {
            
            NSCalendar *gregorian = [[NSCalendar alloc] initWithCalendarIdentifier:NSGregorianCalendar];
            
            NSDateComponents *startComponents = [gregorian components:NSHourCalendarUnit|NSMinuteCalendarUnit fromDate:startDate];
            NSDateComponents *endComponents = [gregorian components:NSHourCalendarUnit|NSMinuteCalendarUnit fromDate:endDate];
            
            NSNumber *startHr = [NSNumber numberWithInt:startComponents.hour];
            NSNumber *startMin = [NSNumber numberWithInt:startComponents.minute];
            NSNumber *endHr = [NSNumber numberWithInt:endComponents.hour];
            NSNumber *endMin = [NSNumber numberWithInt:endComponents.minute];
            
            returnDictionary = [NSDictionary dictionaryWithObjectsAndKeys:startHr,@"startHour",startMin,@"startMinute",
                                endHr,@"endHour",endMin,@"endMinute",nil];
        }
    }
    [command success:returnDictionary];
    
    
}

+ (void)getTags:(ForgeTask*)command {
    NSArray *tags = [UAPush shared].tags? : [NSArray array];
    NSDictionary *returnDictionary = [NSDictionary dictionaryWithObjectsAndKeys:tags, @"tags", nil];
    [command success:returnDictionary];
    
}

+ (void)getAlias:(ForgeTask*)command {
    NSString *alias = [UAPush shared].alias ?: @"";
    [command success:alias];
    
}

//setters

+ (void)setTags:(ForgeTask*)command tags:(NSArray *)tags{
//    UALOG(@"setTags: %@", tags);
    NSMutableArray *tagsA = [NSMutableArray arrayWithArray:tags ];
    [UAPush shared].tags = tagsA;
    [[UAPush shared] updateRegistration];
    [command success:nil];
}

+ (void)setAlias:(ForgeTask*)command text:(NSString *)text {
    NSString *alias = text;
    // If the value passed in is nil or an empty string, set the alias to nil. Empty string will cause registration failures
    // from the Urban Airship API
    alias = [alias stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
    if ([alias length] == 0) {
        [UAPush shared].alias = nil;
    }
    else{
        [UAPush shared].alias = alias;
    }
    [[UAPush shared] updateRegistration];
    [command success:nil];
    
}
//API Parity with andorid
+ (void)setSoundEnabled:(ForgeTask*)command  text:(NSNumber *)text {
    [command success:nil];
}
+ (void)setVibrateEnabled:(ForgeTask*)command  text:(NSNumber *)text {
    [command success:nil];
}

+ (void)setQuietTimeEnabled:(ForgeTask*)command  text:(NSNumber *)text {
    NSNumber *value = text;
    BOOL enabled = [value boolValue];
    [UAPush shared].quietTimeEnabled = enabled;
    [[UAPush shared] updateRegistration];
    [command success:nil];
    
}

+ (void)setQuietTime:(ForgeTask*)command startHour:(NSNumber *)startHour startMinute:(NSNumber *)startMinute  endHour:(NSNumber *)endHour  endMinute:(NSNumber *)endMinute  {
    id startHr = startHour;
    id startMin = startMinute;
    id endHr = endHour;
    id endMin = endMinute;
    
    NSDate *startDate;
    NSDate *endDate;
    
    NSCalendar *gregorian = [[NSCalendar alloc] initWithCalendarIdentifier:NSGregorianCalendar] ;
    NSDateComponents *startComponents = [gregorian components:NSYearCalendarUnit fromDate:[NSDate date]] ;
    NSDateComponents *endComponents = [gregorian components:NSYearCalendarUnit fromDate:[NSDate date]] ;
    
    startComponents.hour = [startHr intValue];
    startComponents.minute =[startMin intValue];
    endComponents.hour = [endHr intValue];
    endComponents.minute = [endMin intValue];
    
    startDate = [gregorian dateFromComponents:startComponents];
    endDate = [gregorian dateFromComponents:endComponents];
    
    [[UAPush shared] setQuietTimeFrom:startDate to:endDate withTimeZone:[NSTimeZone localTimeZone]];
    [[UAPush shared] updateRegistration];
    [command success:nil];
    
}

+ (void)setAutobadgeEnabled:(ForgeTask*)command text:(NSNumber *)text{
    NSNumber *number = text;
    BOOL enabled = [number boolValue];
    [UAPush shared].autobadgeEnabled = enabled;
    [command success:nil];
    
}

+ (void)setBadgeNumber:(ForgeTask*)command text:(NSNumber *)text {
    id number = text;
    NSInteger badgeNumber = [number intValue];
    [[UAPush shared] setBadgeNumber:badgeNumber];
    [command success:nil];
    
}

//reset badge

+ (void)resetBadge:(ForgeTask*)command {
    [[UAPush shared] resetBadge];
    [[UAPush shared] updateRegistration];
    [command success:nil];
    
}

//location recording

+ (void)recordCurrentLocation:(ForgeTask*)command {
    [[UAirship shared].locationService reportCurrentLocation];
    [command success:nil];
    
}











@end

