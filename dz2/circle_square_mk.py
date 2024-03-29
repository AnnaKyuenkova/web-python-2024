import random

def circle_square_mk(r, n):
    circle_area = 3.14159 * r**2 
    count_inside = 0
    for _ in range(n):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)
        if x**2 + y**2 <= r**2:
            count_inside += 1
    square_mk = (2 * r)**2 * (count_inside / n)
    return square_mk

if __name__ == '__main__':
    r = float(input())
    n = int(input())

    square_formula = 3.14159 * r**2 
    square_mk = circle_square_mk(r, n)

    print("Площадь окружности по формуле =", square_formula)
    print("Площадь окружности методом Монте-Карло =", square_mk)

# чем больше значение n, тем выше точность вычисления площади окружности методом Монте-Карло и меньше погрешность
