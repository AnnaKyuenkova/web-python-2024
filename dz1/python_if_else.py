while True:
    n = int(input())
    if (n < 1) or (n > 100):
        print ("ERROR: число выходит за пределы диапазона")
    elif (n % 2 != 0):
        print ("Weird")
    elif (n % 2 == 0) and (n >= 2) and (n <= 5):
        print ("Not Weird")
    elif (n % 2 == 0) and (n >= 6) and (n <= 20):
        print ("Weird")
    elif (n % 2 == 0) and (n >= 20):
        print ("Not Weird")