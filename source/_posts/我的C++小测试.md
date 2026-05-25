---
title: "我的C++小测试"
date: 2025-01-03 09:52:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "C++"
cnblogs_postid: "18649363"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18649363"
---

1. (单选题, 2.0 分)
复制构造函数的形参是(     )。
A某个对象的引用名  
B某个对象的指针名
C某个对象的成员名
D某个对象名

2. (单选题, 2.0 分)
以下数组定义中，不正确的是(   )。
Aint  a[10 ]={1，2，3，4，5，6};
Bchar a=”hello”;
Cint  a[ ][2]={1，2，3，4，5，6};
Dstring s=”abvfgg@54”;

3. (单选题, 2.0 分)
给出以下定义:
char x[ ]="abcdefg";
char y[ ]={‘a',‘b'，'c',  'd' ,'e' ,'f' ,'g'};
则正确的叙述为（  ）。
A数组Y需要的存储空间大于数组X的存储空间 
B数组x和数组Y需要同样大的存储空间
C数组X需要的存储空间大于数组Y的存储空间
D数组X和数组Y等价

用sizeof（）函数

4. (单选题, 2.0 分)
下列关于C++函数的叙述中，正确的是(    )。
A每个函数都必须返回一个值
B函数不能自己调用自己
C每个函数至少要具有一个参数  
D函数可以嵌套调用，但不能嵌套定义  

5. (单选题, 2.0 分)
在C++中关于类和对象，下列说法错误的是(    )。
A类是对象的抽象，而对象则是类的特例
B类是具有相同特性和相同行为的对象的集合
C一个类只能有一个对象
D面向对象程序设计中，通过创建类（包含属性与方法）实现封装和数据隐藏

6. (单选题, 2.0 分)
下列语句中错误的是(    )。 
Aint n; cin>>n; int *p=new int[n];  
Bdelete []p;
Cint *p=new int (10); 
Dint p=new int[10];   
7. (单选题, 2.0 分)下面的符号中可以用作 C++标识符的是（   ）。
Aelse
Bfcc@other
C3test
Dradius
8. (单选题, 2.0 分)
如果主调函数传递数组给被调函数，对函数形参的说明有错误的是（  ）。
A int a(float x,int n)
B int a(float x[10],int n) 
C void a(float *x,int n)
D int a(float x[ ],int n)  

9. (单选题, 2.0 分)
对于语句x*=y+2；还可以写成（  ）。
```A x=x*y+2;   ```
```B x=2+y*x;   ```
```C x=x*(y+2);　```
```D x=y+2*x;```

10. (单选题, 2.0 分)
下列不是构造函数的特征的是（  ）。
A构造函数可以设置默认参数   
B构造函数可以重载
C构造函数必须指定返回值类型
D构造函数的函数名与类名相同

二、 程序填空题 （共 2题，12.0 分）
11. (程序填空题, 4.0 分)
函数 fun 的功能是判断一个3位整数的个位数和百位数之和是否等于其十位上的数字，是则返回“1”，否则返回“0”，请完善程序。
```
#include <iostream>
using namespace std;
bool  fun(int n)
{int g,s,b;
	g=n%10;
	
	(1)              //获取十位数的值
	
	b=n/100;
	
	(2)                 
	
	return 1;
	
	else return 0;
	
}

int main()

{ int m;
	
	cin>>m;
	
	cout<<fun(m);
	
	return 0;
	
}
```
(1)s=(n%100-g)/10;
(2)if(g+b==s)

12. (程序填空题, 8.0 分)

该程序段实现运算符重载，完善程序。

按成员函数重载运算符“-”以实现两个复数的差运算，再以友元方式重载“*”运算符实现两个复数的积运算。

说明：设z1=a+bi，z2=c+di(a、b、c、d∈R)是任意两个复数，那么它们的积(a+bi)(c+di)=(ac-bd)+(bc+ad)i。


```
#include<iostream> 

using namespace std;

class Complex

{
	
	float real;
	
	float imag;
	
public:
	
	Complex( float r,float i  )
	
	{
		
		real=r; imag=i;}
	
	void display() 
	
	{   
		
		cout<<real<<"+"<<imag<<"i"<<endl;
		
	}
	
	________（1）____________ //函数声明：运算符“-”重载为成员函数
	
	_______（2）_____________ //函数声明：运算符“*”重载为友元员函数
	
	
	
};

__________（3）__________ // 函数类外实现：定义运算符“-”重载函数

__________（4）__________ // 函数类外实现：定义运算符“*”重载函数
```
myanswer:
```
(1)Complex operator+ (Complex& comp2);
(2)friend Complex operator*(Complex& comp1,Complex& comp2);

(3)Complex Complex::operator+ (Complex& comp2) 
{return Complex(real+comp2.real,imag+comp2.imag);}

(4)Complex operator*(Complex& comp1,Complex& comp2)
{return Complex(comp1.real*comp2.real,comp1.imag*comp2.imag);}
```

编写程序输出200-300之间的所有素数以及素数的个数。
```
#include<iostream> 
using namespace std;
int main()
{
	bool isprime;
	int num=0;
	for(int i=200;i<=300;i++)
	{
		isprime=false;
		for(int j=2;j<i;j++)
		{
			if(i%j==0){isprime=false;break;}
			else{isprime=true;}
		}
		if(isprime){
			cout<<i<<endl;
			num++;
		}
	}
	cout<<num;
	return 0;
}

```
编写程序计算并输出n(包括n)以内能被5或9整除的所有自然数的倒数之和。 例如, 从键盘输入n为20后, 输出为: s=0.583333。
```
#include<iostream> 
using namespace std;
int main()
{
	int n;
	double s;
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		if(i%5==0 || i%9==0)s+=1.0/i;
	}
	cout<<"s="<<s;
	return 0;
}
```
编写一个函数对某犯罪团伙（13人）一段时间内支付宝收入金额(float 类型）进行排序（降序），编写主函数测试该函数，13人支付宝收入金额在主函数中从键盘输入，并将排序后的结果在主函数中输出。(注：不能直接调用系统函数）
```
#include<iostream> 
using namespace std;
void Sort(float* m)
{
	int n=13;
	float temp;
	for(int j=0;j<n-1;j++)
	{
		for(int i=0;i<n-j-1;i++)
		{
			if(m[i]<m[i+1])
			{
				temp=m[i];
				m[i]=m[i+1];
				m[i+1]=temp;
			}
		}
	}
}
int main()
{
	float money[13];
	for(int i=0;i<13;i++)cin>>money[i];
	Sort(money);
	for(int i=0;i<13;i++)cout<<money[i]<<endl;
	return 0;
}
```
编写程序将4*4的二维数组的值按照列的顺序存储到一维数组中，要求从键盘上输入二维数组，转换存储到一维数组中，输出一维数组。
如输入二维数组：
5  7  9  10
4  3  0   1
20  4  19  40
12 45  23  2
输出的一维数组是：
5 4 20 12 7 3 4 45 9 0 19 23 10 1 40 2.
```
#include<iostream> 
using namespace std;
int main()
{
	int a[4][4],b[16],num=0;
	for(int i=0;i<4;i++)
	{
		for(int j=0;j<4;j++)
		{
			cin>>a[i][j];
		}
	}
	for(int i=0;i<4;i++)
	{
		for(int j=0;j<4;j++)
		{
			b[num]=a[j][i];
			num++;
		}
	}
	for(int i=0;i<16;i++)cout<<b[i]<<' ';
	return 0;
}
```
编写程序对字符串进行下列操作：

（1）编写一个子函数，统计字符串c中的非数字字符的个数。

函数原型：int MyStrlen(const char c[]）;

如输入字符串"GQ8&6Kd4_07"，则函数返回值为6。

（2）编写一个子函数，将字符串a中所有的非“*”号字符拷贝到字符串b中。

函数原型：void MyCopy(const char a[]，char b[]）;

如a字符串```"Fb*fk**cg_12***"```,则b字符串应为"Fbfkcg_12"。

（3）编写一个子函数，将一个字符串m加密后存放到字符串n中，加密的规则是：当内容是英文字母时则用该英文字母的后5个字母替换，同时字母变换大小写,如字母a时则替换为F，字母Z则替换为e；当内容是数字时，则把数字加5，如0替换为5，9替换为4。

函数原型： void myEncipher(const char *m, char *n）;

写出主函数测试以上操作。
```
#include<iostream> 
using namespace std;
int MyStrlen(const char c[])
{
	int num=0;
	for(int i=0;c[i]!=0;i++)
	{
		if(c[i]<'0' || c[i]>'9')num++;
	}
	return num;
}
void MyCopy(const char a[],char b[])
{
	int num=0;
	for(int i=0;a[i]!=0;i++)
	{
		if(a[i]!='*')
		{
			b[num]=a[i];
			num++;
		}
	}
	b[num+1]='\0';
}
void myEncipher(const char *m, char *n)
{
	int num=0;
	char ctemp;
	for(int i=0;m[i]!=0;i++)
	{
		if(m[i]>='a' && m[i]<'v'){ctemp=(m[i]+5)-'a'+'A';}
		else if(m[i]>='v' && m[i]<='z'){ctemp=m[i]-53;}
		else if(m[i]>='A' && m[i]<'V'){ctemp=(m[i]+5)-'A'+'a';}
		else if(m[i]>='v' && m[i]<='z'){ctemp=m[i]+11;}
		else if(m[i]>='0' && m[i]<='4'){ctemp=m[i]+5;}
		else if(m[i]>='5' && m[i]<='9'){ctemp=m[i]-5;}
		else{ctemp=m[i];}
		n[num]=ctemp;
		num++;
	}
	n[num+1]='\0';
}
int main()
{
	char c[]="GQ8&6Kd4_07";
	cout<<MyStrlen(c)<<endl;
	
	char a[]="Fb*fk**cg_12***";
	char b[20];
	MyCopy(a,b);
	for(int i=0;b[i]!=0;i++)cout<<b[i];
	cout<<endl;
	
	char m[]="Hello World12345";
	char n[20];
	myEncipher(m,n);
	for(int i=0;n[i]!=0;i++)cout<<n[i];
	return 0;
}
```
某市公安局A派出所统计当月辖区内电信网络诈骗案件相关数据信息，编写一个电诈类（telecom fraud,简写Tel_fraud）, 其中包含案件类型，报案时间，受害人姓名，损失金额等数据成员（都为私有的）。

（1） 添加对数据成员初始化的无参构造函数、带参数构造函数，复制构造函数、析构函数以及显示电诈信息的成员函数（display），也可根据需要添加其他成员函数。

（2） 设计一个普通函数：void amount(Tel_fraud s[])，用于统计所有电诈案件损失金额的总和，并输出统计金额的信息；

（3） 首先在主函数中调用（1）的所有成员函数进行验证，再定义一个 Tel_fraud 的对象数组，可以存放以下电诈案件信息，将数组内容输出，调用 amount()输出损失金额信息。

刷单返利类          2024年12月8日09时00分  张三  12320

冒充电商客服      2024年12月15日11时00分  李四   7301.1

虚假贷款             2024年12月23日09时00分   王五  32253.5

杀猪盘类             2024年12月25日13时00分    小丽  12520

虚假投资理财      2024年12月29日19时00分    李华   53000
```
#include<iostream> 
#include<string>
#include<iomanip>
using namespace std;
class Tel_fraud 
{
public:
	Tel_fraud() {leixing=" ";Time=" ";name=" ";money=0.0;}
	Tel_fraud(string lx,string sj,string mz,double je){leixing=lx;Time=sj;name=mz;money=je;}
	Tel_fraud(Tel_fraud& tel){leixing=tel.leixing;Time=tel.Time;name=tel.name;money=tel.money;}
	~Tel_fraud() {cout<<"调用了析构函数"<<endl;}
	void display()
	{
		cout<<"类型:"<<leixing<<endl<<"时间："<<Time<<endl<<"姓名："<<name<<endl<<"损失金额："<<money<<endl<<endl;
	}
	friend void amount(Tel_fraud s[]);
private:
	string leixing,Time,name;
	double money;
};
void amount(Tel_fraud s[])
{
	double sum=0.0;
	for(int i=0;i<5;i++)
	{
		sum+=s[i].money*1.0;
	}
	cout<<"总损失金额："<<setprecision(7)<<sum<<endl;
}
int main()
{
	Tel_fraud tel;
	Tel_fraud();
	tel=Tel_fraud("test","test","test",1.23);
	tel.display();
	
	Tel_fraud tels[5]=
	{
		Tel_fraud("刷单返利类","2024年12月8日09时00分","张三",12320),
		Tel_fraud("冒充电商客服"," 2024年12月15日11时00分","李四",7301.1),
		Tel_fraud("虚假贷款","2024年12月23日09时00分","王五",32253.5),
		Tel_fraud("杀猪盘类","2024年12月25日13时00分","小丽",12520),
		Tel_fraud("虚假投资理财","2024年12月29日19时00分","李华",53000)
	};
	for(int i=0;i<5;i++)tels[i].display();
	amount(tels);
	return 0;
}
```
