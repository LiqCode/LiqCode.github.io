---
layout: post
title: iOS viewcontroller
date: 2017-04-16 19:32:24.000000000 +09:00
---

许久没有看过viewcontroller，由于项目原因，重新温习了下，现在整理下

### 生命周期

启动到显示

* init
* willMoveToParentViewController
* loadView
* viewDidLoad
* viewWillAppear
* updateViewConstraints
* viewWillLayoutSubviews
* viewDidLayoutSubviews
* viewDidAppear


退出到销毁 

* didMoveToParentViewController
* viewWillDisappear
* viewDidDisappear
* dealloc

作为子控制，加入到父控制器上，分三步，周期如下

```
OneViewController *one = [[OneViewController alloc] init];
* init

[self addChildViewController:vc];
* willMoveToParentViewController
* loadView
* viewDidLoad

[self.view addSubview:vc.view];
* viewWillAppear
* updateViewConstraints
* viewWillLayoutSubviews
* viewDidLayoutSubviews
* viewDidAppear

```
### 响应链

//是否响应该手势，但只要手势开始调用，用于确定响应的view，与GestureRecongizer一样
* hitTest:withEvent
* pointInside:withEvent


