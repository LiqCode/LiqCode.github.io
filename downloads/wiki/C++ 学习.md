# C++ 学习

这里记录一下，C++特有的东西，至少是c、Java、oc、js中没有的

### 重载 - 多态

### 引用
按引用传递使用的内存和时间都比按值传递少。如果使用引用作为形参，不要改变它的值，最好传入的引用参数加上const关键字。


```
int & pr = pr;

getPerson(p);
void getPerson(Person &p)
{
 ····
}

```

```
Time operator+(const int & t1, const Time & t2)
{
    Time sum;
    sum.minutes = t2.minutes + t1;
    sum.hours = t2.hours ;
    return sum; //局部变量，如果用引用，会在函数执行完后释放掉，所以这里不能用引用，将返回对象拷贝一份回传。
}
```

### new布局
new通常负责堆中找到一个足以能够满足要求的内存块。但它还有一种变体，被称作布局new操作符，它你指定要使用的位置。程序员可能使用这种特性来设置其内存管理或处理需要通过特定地址进行访问的硬件。

```
#include <new> //引用头文件
struct chaff
{
    char dross[20];
    int slag;
}

char buffer1[50];
char buffer2[200];

int main()
{
    chaff *p1, *p2;
    int *p3, *p4;
    
    p1 = new chaff; //堆中分配空间
    p3 = new int[20]; //堆中分配空间
    
    p2 = new (buffer1) chaff; //布局到buffer1中
    p4 = new (buffer2) int[20]; //布局到buffer2中
}
```

内存管理，对于使用布局加入偏移量的，不建议，内存释放会有问题。

### 名称空间

```
namespace Jack {
    double pail;
    void fetch();
    int pal;
    struct Well{...};
}
```

名字空间可以是全局的（全局名称空间），也可以位于另一个名称空间中，但不能位于代码块中。
```
Jack::pail = 12.34; //变量
Jack::Well model; //结构体

//using编译指令,
using namespace jack; //使用该命名空间的名称在下来的下面的作用域全局可用。

//下面会导致二义性  using声明，如果某个名称已经在函数中声明了，则不能用using声明导入相同的名称。
using jack::pal; 
using jill::pal;
pal = 4 ; //是指的那个，这样会有冲突。
```

* 未命名的命名空间
```
//匿名命名空间
//作用域：从声明点到改声明区域末尾，与全局变量相似。可以替代内部静态变量
namespace
{
    int ice;
    int bandycoot;
}
```

### class
* private/public
* 构造函数和析构函数
* 操作符重载 operator
    Time operator+(const Time & t) const;
    Time operator+(const int & t) const;

### 友元
* 友元函数：友元函数是非成员函数，其访问权限与成员函数相同。与oc中的类方法大致相同
* 友元类
* 友元成员函数
```
    friend std::ostream & operator<<(std::ostream & os, const Time & t);
    
    std::ostream &  operator<<(std::ostream & os, const Time & t)
    {
        os << t.hours << "hours, " << t.minutes << " minutes";
        return os;
    }
```
### 类的自动转换和强制类型转换

```
    explicit Time(int h);
```

