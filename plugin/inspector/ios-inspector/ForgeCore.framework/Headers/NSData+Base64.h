//
//  NSData+Base64.m
//
// Derived from http://colloquy.info/project/browser/trunk/NSDataAdditions.h?rev=1576
// Created by khammond on Mon Oct 29 2001.
// Formatted by Timothy Hatcher on Sun Jul 4 2004.
// Copyright (c) 2001 Kyle Hammond. All rights reserved.
// Original development by Dave Winer.
//

@interface NSData (Base64)

+ (NSData *) dataWithBase64EncodedString:(NSString *) string;

- (id) initWithBase64EncodedString:(NSString *) string;

- (NSString *) base64EncodingWithLineLength:(unsigned int) lineLength;

@end