import subprocess
import pytest
import os
import math

from fact import fact_rec
from fact import fact_it
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list
from my_sum import my_sum
from my_sum_argv import my_sum_argv
from email_validation import is_valid_email, fun
from fibonacci import fibonacci
from average_scores import compute_average_scores
from phone_number import sort_phone
from people_sort import sort_people
from circle_square_mk import circle_square_mk


INTERPRETER = 'python'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'fact_rec': [
        (1, 1),
        (7, 5040),
        (100, 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000),
        (0, None)
    ],
    'fact_it': [
        (1, 1),
        (7, 5040),
        (100, 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000),
        (0, None)
    ],
    'show_employee': [
        (["Иванов Иван Иванович", '30000'], ["Иванов Иван Иванович: 30000 ₽"]),
        (["Грибоедов Грибоед Грибоедович", '100000'], ["Грибоедов Грибоед Грибоедович: 100000 ₽"]),
        (["Бибизоро", '50'], ["Бибизоро: 50 ₽"]),
        (["Забор", '0'], ["Забор: 0 ₽"]),
        (["Депутат", '-500000'], ["Депутат: -500000 ₽"]),
    ],
    'sum_and_sub': [
        ([1, 1], [2, 0]),
        ([0, 0], [0, 0]),
        ([5.5, 3.2], [8.7, 2.3]),
        ([100000, 50000], [150000, 50000]),
        ([-10, -5], [-15, -5]),
    ],
    'process_list': [
        ([1, 2, 3, 4, 5], [1, 4, 27, 16, 125]),
        ([4, 2, 34, 23], [16, 4, 1156, 12167]),
        ([3, 6, 9, 10, 56], [27, 36, 729, 100, 3136]),
        ([5, 6, 11, 12, 13], [125, 36, 1331, 144, 2197]),
        ([11, 22, 33, 44], [1331, 484, 35937, 1936])
    ],
    'my_sum': [
        ([1, 2, 3, 4], 10),
        ([-1, -2, -3, -4], -10),
        ([7], 7),
        ([], 0),
        ([1.5, 2.5, 3.5], 7.5)
    ],
    'my_sum_argv': [
        ([1, 2, 3, 4], 10),
        ([-1, -2, -3, -4], -10),
        ([7], 7),
        ([], 0),
        ([1, -2, -3], -4)
    ],
    'fibonacci': [
        (0, []),
        (1, [0]),
        (5, [0, 1, 1, 2, 3]),
        (6, [0, 1, 1, 2, 3, 5]),
        (7, [0, 1, 1, 2, 3, 5, 8])
    ],
    'average_scores': [
        ([(89.0, 90.0, 78.0, 93.0, 80.0), (90.0, 91.0, 85.0, 88.0, 86.0), (91.0, 92.0, 83.0, 89.0, 90.5)], (90.0, 91.0, 82.0, 90.0, 85.5)),
        ([(10, 20, 30), (30, 10, 20), (40, 30, 20), (10, 10, 10), (30, 20, 40)], (24, 18, 24)),
        ([(5, 10), (7, 12)], (6, 11)),
        ([(0, 0, 0), (0, 0, 0)], (0, 0, 0))
    ],
    'sort_phone': [
        (['07895462130', '89875641230', '9195969878'], ['+7 (789) 546-21-30', '+7 (919) 596-98-78', '+7 (987) 564-12-30']),
        (['09258878675', '06734256410'], ['+7 (673) 425-64-10', '+7 (925) 887-86-75']),
        (['9258878675', '6745368907', '87810674537'], ['+7 (674) 536-89-07', '+7 (781) 067-45-37', '+7 (925) 887-86-75'])
    ],
    'sort_people': [
        ([["John", "Doe", '30', "M"]], ["Mr. John Doe"]),
        ([["John", "Doe", '30', "M"], ["Olivia", "Taylor", '38', "F"]], ['Mr. John Doe', 'Ms. Olivia Taylor']),
        ([["Olivia", "Taylor", '38', "F"]], ["Ms. Olivia Taylor"]),
        ([['Mike', 'Thomson', '20', 'M'], ['Robert', 'Bustle', '32', 'M'], ['Andria', 'Bustle', '30', 'F']], ['Mr. Mike Thomson', 'Ms. Andria Bustle', 'Mr. Robert Bustle']),
        ([['Anton', 'Kollaps', '19', 'M'], ['Vlad', 'Shurup', '25', 'M'], ['Maria', 'Jester', '16', 'F']], ['Ms. Maria Jester', 'Mr. Anton Kollaps', 'Mr. Vlad Shurup'])
    ],    
}

@pytest.mark.parametrize("input_data, expected", test_data['fact_rec'])
def test_fact_rec(input_data, expected):
    assert fact_rec(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['fact_it'])
def test_fact_it(input_data, expected):
    assert fact_it(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['show_employee'])
def test_show_employee(input_data, expected):
    assert show_employee(*input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['sum_and_sub'])
def test_sum_and_sub(input_data, expected):
    assert sum_and_sub(*input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['process_list'])
def test_process_list(input_data, expected):
    assert process_list(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['my_sum'])
def test_my_sum(input_data, expected):
    assert my_sum(*input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['my_sum_argv'])
def test_my_sum_argv(input_data, expected):
    assert my_sum_argv(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['fibonacci'])
def test_fibonacci(input_data, expected):
    assert fibonacci(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['average_scores'])
def test_compute_average_scores(input_data, expected):
    assert compute_average_scores(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['sort_phone'])
def test_sort_phone(input_data, expected):
    assert sort_phone(input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['sort_people'])
def test_sort_people(input_data, expected):
    assert sort_people(input_data) == expected

def test_circle_square_mk():
    radius = 5
    n_experiments = 100000
    calculated_square = circle_square_mk(radius, n_experiments)
    actual_square = 3.14159 * radius ** 2  
    error = abs(calculated_square - actual_square)
    assert error < 1  

def test_is_valid_email1():
    assert is_valid_email("lara@mospolytech.ru") == True

def test_is_valid_email2():
    assert is_valid_email("brian-23@mospolytech.ru") == True

def test_is_valid_email3():
    assert is_valid_email("britts_54@mospolytech.ru") == True

def test_is_valid_email4():
    assert is_valid_email("invalid_email") == False

def test_is_valid_email5():
    assert is_valid_email("invalid.com") == False

def test_is_valid_email6():
    assert is_valid_email("username@websitename") == False

def test_fun1():
    emails = ["lara@mospolytech.ru", "brian-23@mospolytech.ru", "britts_54@mospolytech.ru", "invalid_email"]
    valid_emails = fun(len(emails), emails)
    assert valid_emails == ["brian-23@mospolytech.ru", "britts_54@mospolytech.ru", "lara@mospolytech.ru"]

def test_fun2():
    emails = ["lara@mospolytech.ru"]
    valid_emails = fun(len(emails), emails)
    assert valid_emails == ["lara@mospolytech.ru"]

def test_fun3():
    emails = []
    valid_emails = fun(len(emails), emails)
    assert valid_emails == []