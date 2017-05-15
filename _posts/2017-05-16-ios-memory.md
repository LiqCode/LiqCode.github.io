---
layout: post
title: 内存管理
date: 2017-05-16 01:29:43.000000000 +08:00
tags: iOS
categories: iOS
---


###  MRC和ARC
oc对象管理分2个时代，一个是MRC，另一个是ARC。
**MRC时代** 采用引用计数的方式，管理OC对象，需要手动释放oc对象，想想当初写代码多麻烦，很容易就写错。
只记得一句非常经典的话，**谁创建谁释放**，包括retain,copy, alloc, new。

**ARC时代** 记得当时苹果发布ARC时有多兴奋，瞬间感觉写代码是如此的轻松，不用管OC创建释放，开发速度加快，非常兴奋。但这些都取决于编译器的功劳，OC底层并没有发生变化，依然是引用计数，只是在编译的时候，编译器帮我们加上retain, release。

### AutoReleasePool
当我们创建xcode给我们提供的模板工程的时候，你会发现在main，有一个@autoreleasepool,这就是自动释放池。用于当大量创建临时变量时，及时释放。

{% highlight c %}
    @autoreleasepool {
        return UIApplicationMain(argc, argv, nil, NSStringFromClass([AppDelegate class]));
    }
{% endhighlight %}

ps：**整个 iOS 的应用都是包含在一个自动释放池 block 中的**。

**疑问**：测试不使用自动释放池，循环创建临时的NSString变量，内存没有什么印象（与使用自动释放池一样），代码如下

```
for (NSInteger i = 0; i < 1000000000; i++) {
        @autoreleasepool {
            NSString *string = @"Abc";
            string = [string lowercaseString];
            string = [string stringByAppendingString:@(i).stringValue];

//            UIView *v = [[UIView alloc] initWithFrame:self.view.bounds]; //当加入这行时，内存暴涨
        }
//        NSLog(@"%@", string);
    }
```

### block循环引用

### C语言手动分配空间
堆空间：与栈不同，是需要开发人员自己管理的内存空间，分配内存空间和释放都需要自己动手。
```
//分配内存
double *p = (double *)malloc(sizeof(double *));

//释放
free(p);
p = NULL;
```

### CF、CG create对象

### JS内存管理（JavascriptCore）
由于JS内存管理是垃圾回收，并且JS中的对象都是强引用，而OC是引用计数。如果双方互相引用，势必会造成循环引用，而导致内存泄漏。我们用**JSManagedValue**保存JSValue来避免
