while True:   
    a = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))
    if (b != 0):
        print(a // b)
        print(a / b)
    else:
        print ("ERROR: деление на ноль")