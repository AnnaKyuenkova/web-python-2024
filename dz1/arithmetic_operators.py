while True:   
    a = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))
    if (a >= 1) and (a <= 10**10) and (b >= 1) and (b <= 10**10):
        print (a + b)
        print (a - b)
        print (a * b)
    else:
        print ("ERROR: число выходит за пределы диапазона")