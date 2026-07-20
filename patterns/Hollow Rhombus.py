#Hollow Rhombus

n=7
for i in range(1, n+1):
    print(" "*(n-i),end="")
    for j in range(1, i + 1):
        if i>2 and (j>=2 and j<i):
            print(" ",end=" ")
        else:
            print(i, end=" ")
    print("")
for i in range(n-1,-1,-1):
    print(" "*(n-i),end="")
    for j in range(0, i):
        if i>2 and (j>=1 and j<i-1):
            print(" ",end=" ")
        else:
            print(i, end=" ")
    print("")