//
//  UIViewController+dismissViewControllerHelper.h
//  ForgeCore
//
//  Created by Connor Dunn on 26/02/2013.
//  Copyright (c) 2013 Trigger Corp. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface UIViewController (dismissViewControllerHelper)

- (void)dismissViewControllerHelper:(void (^)(void))completion;

@end
