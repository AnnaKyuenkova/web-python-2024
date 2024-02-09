while True:
    str = input("Введите строку: ")
    splitStr = str.split()
    splitAndJoin = splitStr[0]
    splitStr.pop(0)
    for i in splitStr:
        splitAndJoin += "-" + i
    print(splitAndJoin)