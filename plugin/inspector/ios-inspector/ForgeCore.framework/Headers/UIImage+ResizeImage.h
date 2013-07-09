//
//  UIImage+ResizeImage.h
//  Forge
//
//  Created by Connor Dunn on 21/02/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface UIImage (ResizeImage)

- (UIImage*)imageWithWidth:(float)maxwidth andHeight:(float)maxheight;
- (UIImage*)imageWithWidth:(float)maxwidth andHeight:(float)maxheight andRetina:(BOOL)allowRetina;

@end
