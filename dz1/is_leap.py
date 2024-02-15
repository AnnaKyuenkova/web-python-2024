def is_leap(year):
    if year <= 10**5 or year >= 1900:
        if year % 400 == 0:
            return True
        elif year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True
        else:
            return False
    else:
        print ("error")

year = int(input())
print(is_leap(year))