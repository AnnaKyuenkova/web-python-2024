while True:
    n = int(input("Введите число: "))
    if (n >= 1) and (n <= 20):
        for i in range(1, n+1):
            print(i, end="")
        print() 
    else:
        print ("ERROR: число выходит за пределы диапазона")