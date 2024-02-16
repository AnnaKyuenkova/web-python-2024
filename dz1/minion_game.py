string = input()
string = string.lower()
kevin_score = 0
stewart_score = 0
vowel_letters = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я']
consonant_letters = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
if (len(string) > 0) and (len(string) <= 10**6):
        for i in range(len(string)):
                if string[i].lower() in consonant_letters:
                        stewart_score += len(string) - i
                else:
                        kevin_score += len(string) - i
        if stewart_score > kevin_score:
                print("Стюарт", stewart_score)
        elif stewart_score < kevin_score:
                print("Кевин", kevin_score)
        else:
                print("Ничья")
else:
        print('error')
