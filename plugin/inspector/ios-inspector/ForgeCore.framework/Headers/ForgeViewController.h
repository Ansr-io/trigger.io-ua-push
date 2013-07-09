//
//  ForgeViewController.h
//  Forge
//
//  Created by Connor Dunn on 26/01/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface ForgeViewController : UIViewController {
	IBOutlet UIWebView *webView;
	IBOutlet UIImageView *imageView;
	IBOutlet UIView *containingView;
	BOOL hasLoaded;
	@public BOOL forcePortrait;
}
- (void)loadInitialPage;
- (void)loadURL:(NSURL*)url;
+ (BOOL)isIPad;

@end
