//测试 #define 宏定义变量与函数

#define p 3
#define add(x,y) (x+y)
int main(){
    int a=1;
    int b=p;
    int c;
    c=add(a,b);
    printf("%d\n",c);
}
