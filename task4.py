def fibonacci():
    n=int (input("enter a number:"))
    a=0
    b=1
    sum=0
    count=1
    print(fibonacci,end=" ")
    while(count<=n):
        print(sum,end=" ")
        count=count+1
        a=b
        b=sum
        sum=a+b
fibonacci()