---
layout: post
title: 内存管理
date: 2017-05-16 01:29:43.000000000 +08:00
tags: iOS
categories: iOS
---
申明：本文由LiqCode原创，转载请声明出处。

###  MRC和ARC
oc对象管理分2个时代，一个是MRC，另一个是ARC。
**MRC时代** 采用引用计数的方式，管理OC对象，需要手动释放oc对象，想想当初写代码多麻烦，很容易就写错。
只记得一句非常经典的话，**谁创建谁释放**，包括retain,copy, alloc, new。

**ARC时代** 记得当时苹果发布ARC时有多兴奋，不在需要管OC创建释放，开发速度瞬间提升。但这些都取决于编译器的功劳，OC底层并没有发生变化，依然是引用计数，只是在编译的时候，编译器帮我们加上retain, release。

### AutoReleasePool
当我们创建xcode给我们提供的模板工程的时候，你会发现在main，有一个@autoreleasepool,这就是自动释放池。用于当大量创建临时变量时，及时释放内存。

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

### NSTimer
对于NSTimer，有个我们经常忽略的问题，它会保留其目标对象。如果NSTimer不停重复执行的话，直到开发者稍后手动关闭为止。由于计时器会保留目标对象，如果不手动取消计时器，目标对象是不会释放的，很容易形成“保留环”。

解决方法：开发者手动关闭计时器。

### 循环引用
循环引用，其实就是对象之间互相引用，形成闭环，有点类似互锁。

#### block循环引用
Block循环引用的问题已是老生常谈，Block是将外部对象copy给自己一份，而且只是浅拷贝。在没有加修饰的情况下（__block、__weak），对于OC对象来说，就是引用计数加一，对于基础数据类型（int，float，bool）就是直接copy。
所以当一个对象拥有block，而block又copy了这个对象，就会出现“保留环”

解决办法：对象前面加加上修饰 “__weak”, 但需要注意的是，block作为回调时，如果多个线程同时操作该对象，__weak对象会在执行到block一半时，可能会被释放，继续执行可能会有问题。所以在block里面第一行，就用“__strong”重新修饰。 示例代码如下（基于RAC框架封装）：

```
@weakify(self); //相当于 __weak typeof(self) weakself = self;
void ^(block)() = ^{
  @strongify(self); //相当于 __strong typeof(weakself) self = weakself;
};

```

#### delegate循环引用
delegate循环引用问题比较基础，只需注意将代理属性修饰为weak即可

#### 如何判断循环引用
简单粗暴实用的方法就是在delloc方法中，加个断点，看是否能正常释放。

### C语言手动分配空间
堆空间：与栈不同，是需要开发人员自己管理的内存空间，分配内存空间和释放都需要自己动手。
```
//分配内存
double *p = (double *)malloc(sizeof(double *));

//释放
free(p);
p = NULL;
```

### JS内存管理（JavascriptCore）
由于JS内存管理是垃圾回收，并且JS中的对象都是强引用，而OC是引用计数。如果双方互相引用，势必会造成循环引用，而导致内存泄漏。我们用**JSManagedValue**保存JSValue来避免

### 野指针
当我们使用assign修饰一个属性变量时，它的赋值是不会改变引用计数，与weak相同，但是与weak也有一个差别，当这个变量指向对象的计数为0，被清除时，weak修饰的指针值会置空，assign修饰的不会，指向一片未知区域，成为一个“野指针”，如果运气好，指向地址的内存数据没被清，app还可以跑，否则就会carsh.

解决办法：修饰OC对象时，请避免使用“assign”，有weak替代。
ps：ios中UITableView中delegate以前的版本就是assign，在特定的情况下引发carsh。后面应该是苹果发现了，统一改成weak。
```
@property (nonatomic, weak) people *man;
```

### CF、CT、CG对象
使用过iOS底层框架时，常常会看到带有含create创建方法，创建CF、CG对象，这些就需要我们手动释放内存，如果没有手动释放，可以通过leak内存检测工具查出来。示例代码：
```
CGImageRef imageRef = CGImageCreateWithImageInRect(imageRef, myImageRect); //创建
CGImageRelease(imageRef); //释放

CTFontRef ctFont = CTFontCreateWithName((__bridge CFStringRef) self.font.fontName, self.font.pointSize, NULL);
CFRelease(ctFont);

CGMutablePathRef trackPath = CGPathCreateMutable();
CGPathRelease(trackPath);
```
