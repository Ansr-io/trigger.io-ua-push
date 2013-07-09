//
//  ForgeApp.h
//  ForgeCore
//
//  Created by Connor Dunn on 03/10/2012.
//  Copyright (c) 2012 Trigger Corp. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "JSONKit.h"
#import "ForgeAppDelegate.h"

@interface ForgeApp : NSObject {
	
}

/// Main webView used for Forge
@property UIWebView* webView;
/// appConfig dictionary
@property NSDictionary* appConfig;
/// Forge app delegate
@property ForgeAppDelegate* appDelegate;
/// Forge view controller
@property ForgeViewController* viewController;
@property NSMutableArray* eventListeners;
/// Whether the inspector module is enabled - used to enable extra debug events
@property BOOL inspectorEnabled;

+ (ForgeApp*)sharedApp;
- (id)nativeEvent:(SEL)selector withArgs:(NSArray*)args;
- (void)event:(NSString*)name withParam:(id)params;
- (NSDictionary*)configForPlugin:(NSString*)name;
- (NSString*)assetsFolderLocationWithPrefs:(NSUserDefaults*)prefs;
- (NSString*)bundleLocationRelativeToAssets;

@end
