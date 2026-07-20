n=int(input())
num = 1
for i in range(n):
    if i % 2 == 0:
        for j in range(n):
            print(num, end=" ")
            num += 1
    else:
        temp = num + n - 1
        for j in range(n):
            print(temp, end=" ")
            temp -= 1
        num += n
    print()