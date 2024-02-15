while True:
    str = input()
    if len(str) > 0 or len(str) <= 1000:
        print(str.swapcase())
    else:
        print("ERROR: нежопустимая длина строки (длина должна быть от 1 до 1000)")