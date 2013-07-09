//
//  ALAsset+Data.h
//  Forge
//
//  Created by Connor Dunn on 21/02/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <AssetsLibrary/AssetsLibrary.h>

@interface ALAsset (Data)

- (NSData*) dataWithFile:(id)file;
- (NSData*) data;

@end
