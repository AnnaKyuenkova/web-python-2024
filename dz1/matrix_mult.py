n = int(input())
if (n >= 2) and (n <= 10):
    a = []
    b = []
    for i in range(n):
        row = list(map(int, input().split()))
        a.append(row)

    for i in range(n):
        row = list(map(int, input().split()))
        b.append(row)
    c = []
    for i in range(n):
        result_row = []
        for j in range(n):
            result_value = 0
            for k in range(n):
                result_value += a[i][k] * b[k][j]
            result_row.append(result_value)
        c.append(result_row)
    for row in c:
        print(" ".join(map(str, row)))
else:
    print('error')