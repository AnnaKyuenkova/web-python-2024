import time

def fact_rec(n):
    if n < 1 or n > 10**5:
        print("error")
        return
    if n == 1:
        return 1
    else:
        return n * fact_rec(n-1)

def fact_it(n):
    if n < 1 or n > 10**5:
        print("error")
        return
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

if __name__ == '__main__':
    n = int(input())
    start_time = time.time()
    print(f"Рекурсивная функция: {fact_rec(n)}")
    print(f"Время выполнения рекурсивной функции: {time.time() - start_time} секунд")

    start_time = time.time()
    print(f"Итерационная функция: {fact_it(n)}")
    print(f"Время выполнения итерационной функции: {time.time() - start_time} секунд")

# итерационная выполняется быстрее