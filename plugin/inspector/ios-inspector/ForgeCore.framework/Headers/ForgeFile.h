//
//  ForgeFile.h
//  ForgeCore
//
//  Created by Connor Dunn on 14/01/2013.
//  Copyright (c) 2013 Trigger Corp. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <AssetsLibrary/AssetsLibrary.h>

typedef void (^ForgeFileExistsResultBlock)(BOOL exists);
typedef void (^ForgeFileDataResultBlock)(NSData* data);
typedef void (^ForgeFileErrorBlock)(NSError* error);

@interface ForgeFile : NSObject {
	NSDictionary* file;
}

- (ForgeFile*) initWithPath:(NSString*)path;
- (ForgeFile *)initWithAssetsPath:(NSString *)assetsPath;
- (ForgeFile*) initWithFile:(NSDictionary*)withFile;
- (ForgeFile*) initWithObject:(NSObject*)object;
- (NSString*) url;
- (void) exists:(ForgeFileExistsResultBlock)resultBlock;
- (void) data:(ForgeFileDataResultBlock)resultBlock errorBlock:(ForgeFileErrorBlock)errorBlock;
- (BOOL) remove;
- (NSString*) mimeType;
- (NSDictionary*) toJSON;

@end
