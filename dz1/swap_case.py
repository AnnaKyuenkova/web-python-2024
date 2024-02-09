while True:
    str = input("Введите строку, содержащую некоторую последовательность символов: ")
    if len(str) > 0 or len(str) <= 1000:
        print(str.swapcase())
    else:
        print("ERROR: нежопустимая длина строки (длина должна быть от 1 до 1000)")