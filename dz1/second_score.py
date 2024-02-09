while True:
    n = int(input("Введите количество учеников: "))
    numbers = []
    for i in range(n):
        num = int(input("Введите число: "))
        numbers.append(num)
    if len(numbers) < 2:
        print("ERROR: должно быть введено минимум два числа")
    else:
        max1 = max(numbers[0], numbers[1])
        max2 = min(numbers[0], numbers[1])
    for i in range(2, len(numbers)):
        if numbers[i] > max1:
            max2 = max1
            max1 = numbers[i]
        elif numbers[i] > max2 and numbers[i] != max1:
            max2 = numbers[i]
    print("Второе место: ", max2)