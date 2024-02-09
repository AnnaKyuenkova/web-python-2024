while True:
    n = int(input("Введите число: "))
    if (n >= 1) and (n <= 20):
        for i in range(n):
            print(i ** 2)
    else: 
        print ("ERROR: число выходит за пределы диапазона")        