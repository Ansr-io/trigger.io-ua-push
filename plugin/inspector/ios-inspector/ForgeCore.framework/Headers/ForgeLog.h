//
//  ForgeLog.h
//  Forge
//
//  Created by Connor Dunn on 25/01/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface ForgeLog : NSObject {
	
}

+ (void) d:(id)msg;
+ (void) i:(id)msg;
+ (void) w:(id)msg;
+ (void) e:(id)msg;
+ (void) c:(id)msg;

@end
