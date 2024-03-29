# функция с использованием list comprehension
def process_list(arr):
    if len(arr) < 1 or len(arr) > 10**3:
        print("error")
        return
    return [i**2 if i % 2 == 0 else i**3 for i in arr]

# функция генератор
def process_list_gen(arr):
    if len(arr) < 1 or len(arr) > 10**3:
        print("error")
        return
    for i in arr:
        if i % 2 == 0:
            yield i * 2
        else:
            yield i ** 2
