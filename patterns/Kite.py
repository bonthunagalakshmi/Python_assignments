#Kite
n=8
for i in range(1, n+1):
    print(" "*(n-i),end="")
    for j in range(1, i + 1):
        print(i, end=" ")
    print("")
for i in range(n-1,0,-1):
    print(" "*(n-i),end="")
    for j in range(0, i):
        print(i, end=" ")
    print("")
for i in range(2, n-2):
    print(" "*(n-i),end="")
    for j in range(1, i + 1):
        print(i, end=" ")
    print("")