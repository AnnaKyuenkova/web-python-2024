def is_leap(year):
    if (year <= 10**5) and (year >= 1900):
        if year % 400 == 0:
            return True
        elif year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True
        else:
            return False
    else:
        return "error"

year = int(input())
print(is_leap(year))