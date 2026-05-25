---
title: "几道C++题目"
date: 2024-11-28 20:32:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "C++"
cnblogs_postid: "18575114"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18575114"
---

## 1、初定义一个数组的值，每一行找出最大值放在每一行最后面
```
#include<iostream>
using namespace std;
int main()
{
int a[5][6]={{1,2,3,4,5},{5,6,7,8,9},{9,10,11,12,13},{13,14,15,16,17}};
int max=0;
for(int i=0;i<=3;i++)
{
max=0;
for(int j=0;j<=4;j++)
{
if(a[i][j]>=max)
max=a[i][j];
}
a[i][5]=max;
}
for(int i=0;i<=3;i++)
{for(int j=0;j<=5;j++)
cout<<a[i][j]<<" ";
cout<<endl;}
system("pause");
return 0;
}
```
## 2、重载函数：
```
#include<iostream>
using namespace std;
int min(int a,int b)
{
if(a>b)
return b;
else
return a;
}
double min(double c,double d,double e)
{
double middle=0.0;
if(c>d)
middle=d;
else
middle=c;
if(middle>e)
return e;
else
return middle;
}
int main()
{
int a=1,b=2;
double c=1.14,d=2.25,e=3.39;
cout<<min(a,b)<<endl;
cout<<min(c,d,e)<<endl;
system("pause");
return 0;
}
```
## 3、算一元二次方程（ax^2+bx+c=0）
```
#include<iostream>
#include<cmath>
using namespace std;
int main()
{
double a,b,c,delta;
cin>>a>>b>>c;
delta=b*b-4*a*c;
if(delta<0)
cout<<"No answer!";
else if(delta==0)
cout<<"x="<<-b/2/a;
else if(delta>0)
{cout<<"x1="<<(-b+sqrt(delta))/2/a<<endl;
cout<<"x2="<<(-b-sqrt(delta))/2/a<<endl;}
return 0;
}
```
## 4、有一个分数序列:2/1, 3/2, 5/3, 8/5, 13/8, 21/13, ...编写程序求出这个序列的前20项之和。
```
#include<iostream>
#include<cmath>
using namespace std;
int main()
{
int a=2,b=1,middle=0;
double fenshu=0.0;
for(int i=1;i<=20;i++)
{
fenshu+=a/b;
middle=a;
a=a+b;
b=middle;
}
cout<<fenshu;
system("pause");
return 0;
}
```
## 5、在主函数中键盘输入10个浮点型数据，用一个子函数对它们进行排序(由小到大排序)。然后在主函数中输出排序后的结果。
```
#include<iostream>
using namespace std;
void sort(double a[])
{
double x, temp;
int y;
for (x = 0; x<9; x++)
{
for (y = 9; y > x; y--)
{
if (a[y-1] > a[y])
{
temp = a[y-1];
a[y-1] = a[y];
a[y] = temp;
}
}
}
}
int main()
{
double a[10];
for(int i=0;i<=9;i++)
cin>>a[i];
sort(a);
for(int i=0;i<=9;i++)
cout<<a[i]<<' ';
system("pause");
return 0;
}
```
## 6、在一个程序中，对字符串进行下列操作：
（1）编写一个子函数，它能将数组a中存放的字符串逆序存放。
函数原型：void sstrrev（char a[]）;
如a中原有字符串"Hello"， 调用该函数后a中的字符串变为"olleH"。
（2）编写一个子函数mystrlen，它能统计输入字符串a中非数字字符的个数个
数，
函数原型：int mystrlen（const char a[]）;
如输入字符串"ab5*6cd8_7"，则函数返回值为6。
（3）编写一个子函数将数组b中存放的字符串连接到数组a中的字符串之后（注：
这里不能用strcat_s）。
函数原型： void mystrcat（char a[], const char b[]）;
如a中原有字符串"ab5*6cd8_7"，而b中有字符串"ABCDEF", 则调用该函数后a中
的字符串变为: "ab5*6cd8_7ABCDEF" 。
写出主函数测试以上操作。
```
#include<iostream>
using namespace std;
void sstrrev(char a[])
{
int length = strlen(a);
for (int i = 0; i < length / 2; i++)
{
char temp = a[i];
a[i] = a[length - 1 - i];
a[length - 1 - i] = temp;
}
}
int mystrlen(char a[])
{
int number=0;
for(int i=0;i<strlen(a);i++)
if(!isdigit(a[i]))
number+=1;
return number;
}
void mystrcat(char a[], char b[]) {
int lena=strlen(a);
for (int i = 0; i < strlen(b); i++) {
a[ lena + i] = b[i];
}
}
int main()
{
char str1[] = "Hello";
sstrrev(str1);
cout << str1 << endl;
char str2[] = "ab5*6cd8_7";
cout << mystrlen(str2) << endl;
char str3[40] = "ab5*6cd8_7";
char str4[] = "ABCDEF";
mystrcat(str3, str4);
cout << str3 << endl;
return 0;
}
```
