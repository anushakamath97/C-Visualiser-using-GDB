int q = 10;
int fun1(int a,int x)
{
	int i = 9;
	a = 45;
	return a;
}
int fun(int a,int x)
{
	int i = 9;
	fun1(i,x);
	a = 5;
	return a;
}
int main(void)
{
	int i = 20 , j = 10, k = 2;
	i = q+1;
	q = 11;
	int a[j][k];
	int sum = i + j;
	int z = i *6;
	int *p = &z;
	*p = 8;
	*p = fun(i,89);
	i = 10;
	return 0;
}
