n = 5

# Upper Half
for i in range(n, 0, -1):
    print(" " * (n - i), end="")
    for j in range(1, 2 * i):
        if i < n and i > 1 and (j > 1 and j < 2 * i - 1):
            print(" ", end="")
        else:
            print("*", end="")
    print()

# Lower Half
for i in range(2, n + 1):
    print(" " * (n - i), end="")
    for j in range(1, 2 * i):
        if i < n and i > 1 and (j > 1 and j < 2 * i - 1):
            print(" ", end="")
        else:
            print("*", end="")
    print()