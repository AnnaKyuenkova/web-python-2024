n = int(input())
passengers = []
for i in range(n):
    entry, exit = map(int, input().split())
    if (entry < exit):
        passengers.append((entry, exit))
    else:
        print('error')
t = int(input())
count = 0
for entry, exit in passengers:
    if (entry <= t) and (t <= exit):
        count += 1
print(count)
