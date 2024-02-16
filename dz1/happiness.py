n, m = map(int, input().split())
i = 1
if (1 <= n <= 10**5) and (1 <= m <= 10**5) and (1 <= i <= 10**9):
    arr = list(map(int, input().split()))
    set_a = set(map(int, input().split()))
    set_b = set(map(int, input().split()))
    mood = 0
    for i in arr:
        if i in set_a:
            mood += 1
        elif i in set_b:
            mood -= 1
    print(mood)
else:
    print('error')