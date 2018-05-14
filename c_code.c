#include<stdio.h>
#include<stdlib.h>
int q = 10,m;
char name[10];
int *n;
int fun1(int a,int x)
{
	int i = 9;
	a = 45;
	static int y = 8;
	y ++ ;
	return a;
}
int fun(int a,int x)
{
	int i = 9;
	q = q + 1;
	fun1(i,x);
	fun1(i,x);
	a = 5;
	return a;
}
int main(void)
{
	int i = 20 , j = 10, k = 2;
	i = q+1;
	q = 11;
	n = &q;
	*n = *n + 1;
	printf("name is :%d",*n);
	scanf("%d",&i);
	printf("i is :%d",i);
	int a[j][i];
	int sum = i + j;
	int z = i *6;
	int *p = &z;
	*p = 8;
	k = fun(i,89);
	i = 10;
	printf("value of p is :%d",*p);
	return 0;
}
