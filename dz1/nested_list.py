n = int(input("Введите количество учеников: "))
records = []
if n < 2 or n > 5:
    print("ERROR: количество учеников должно быть не меньше 2 и не больше 5")
else:
    for i in range(n):
        name = input("Введите имя учащегося: ")
        grade = float(input("Введите оценку: "))
        records.append([name, grade])
    # сортировка списка по второму элементу 
    # (1, потому что нумерация с 0, то есть первый элемент под номером 0, второй - 1)
    # reverse=True значит сортировку от большего к меньшему
    records.sort(key=lambda k: k[1], reverse=False)
    secondMinGrade = records[1][1] 
    nameSecondMinGrade = []
    for i in records:
        if i[1] == secondMinGrade:
            nameSecondMinGrade.append(i[0])
    nameSecondMinGrade.sort()
    print (*nameSecondMinGrade)