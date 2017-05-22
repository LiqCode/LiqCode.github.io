---
layout: post
title: c、c++、oc混编
date: 2016-04-18 14:11:13.000000000 +08:00
tags: iOS
categories: iOS
---
申明：本文由LiqCode原创，转载请声明出处。

iOS支持c、c++、oc混编，那xcode是如何去区分的。在工程build settings中有一配置项“Compile Sources As”. 其中默认选项“According to File Type”,意思是根据文件类型来区别语言，下面是对应表

| 文件后缀 | 支持语言 |
| --- | --- |
| .m | c、oc |
| .mm | c、c++、oc |
| .cpp | c、c++ |
| .c | c |
