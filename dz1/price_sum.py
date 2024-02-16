import csv
adult_total = 0
pensioner_total = 0
child_total = 0
with open('products.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        adult_total += float(row['Взрослый'])
        pensioner_total += float(row['Пенсионер'])
        child_total += float(row['Ребенок'])
print("{:.2f} {:.2f} {:.2f}".format(adult_total, pensioner_total, child_total))