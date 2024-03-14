import time
# рекурсивная функция
def fact_rec(n):
    if n == 0:
        return 1
    return n * fact_rec(n-1)
# итерационная функция
def fact_it(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

if __name__ == '__main__':
    n = int(input("Введите целое положительное число n: "))
    start_time = time.time()
    result_rec = fact_rec(n)
    end_time = time.time()
    print(f"Факториал числа {n} (рекурсивно): {result_rec}")
    print(f"Время выполнения (рекурсивно): {end_time - start_time} секунд")
    start_time = time.time()
    result_it = fact_it(n)
    end_time = time.time()
    print(f"Факториал числа {n} (итерационно): {result_it}")
    print(f"Время выполнения (итерационно): {end_time - start_time} секунд")