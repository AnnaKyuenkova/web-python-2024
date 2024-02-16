import subprocess
import pytest

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
    'python_if_else': [
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('6','Weird'),
        ('22', 'Not Weird'),
        ('110', 'ERROR: число выходит за пределы диапазона'),
        ('-10', 'ERROR: число выходит за пределы диапазона')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['5', '6'], ['11', '-1', '30']),
        (['10', '5'], ['15', '5', '50']),
        (['-1', '5'], ['ERROR: число выходит за пределы диапазона']),
        (['1', '-5'], ['ERROR: число выходит за пределы диапазона']),
        (['-1', '-5'], ['ERROR: число выходит за пределы диапазона'])
    ],
    'division': [
        (['3', '5'], ['0', '0.6']),
        (['6', '2'], ['3', '3.0']),
        (['14', '5'], ['2', '2.8']),
        (['2', '0'], ['ERROR: деление на ноль'])
    ],
    'loops': [
        (['1'], ['0']),
        (['2'], ['0', '1']),
        (['3'], ['0', '1', '4']),
        (['0'], ['ERROR: число выходит за пределы диапазона']),
        (['100'], ['ERROR: число выходит за пределы диапазона'])
    ], 
    'print_function': [
        (['1'], ['1']),
        (['3'], ['123']),
        (['5'], ['12345']),
        (['21'], ['ERROR: число выходит за пределы диапазона'])
    ],
    'second_score': [
        (['5', '2', '3', '6', '6', '5'], ['5']),
        (['3', '1', '2', '3'], ['2']),
        (['5', '1', '4', '3', '2', '4'], ['3']),
        (['1'], ['ERROR: должно быть введено минимум два числа'])
    ],
    'nested_list': [
        (['5', 'Гарри', '37.21', 'Берри', '37.21', 'Тина', '37.2', 'Акрити', '41', 'Хирш', '39'], ['Берри Гарри']),
        (['3', 'Алиса', '85', 'Боб', '90', 'Чарли', '80'], ['Алиса']),
        (['1', 'Евлампий', '100'], ['ERROR: количество учеников должно быть не меньше 2 и не больше 5']),
    ],
    'lists': [
        (['4', 'append 1', 'append 2', 'insert 1 3', 'print'], ['[1, 3, 2]'])
    ],
    'swap_case': [
        (['Www.MosPolytech.ru'], ['wWW.mOSpOLYTECH.RU']),
        (['ХаХаХа'], ['хАхАхА']),
        (['ooOOoo'], ['OOooOO'])
    ],
    'split_and_join': [
        (['this is a string'], ['this-is-a-string']),
        (['приложение на питоне'], ['приложение-на-питоне']),
        (['пишу текст'], ['пишу-текст'])
    ],
    'anagram': [
        (['кот', 'ток'], ['YES']),
        (['кот', 'пес'], ['NO']),
        (['thing', 'night'], ['YES'])
    ],
    'metro': [
        (['3', '25 32', '26 29', '31 43', '27'], ['2'],),
        (['2', '32 12', '23 34', '25'], ['error', '1'],),
        (['3', '11 21', '22 32', '33 43', '10'], ['0'],)
    ],
    'is_leap': [
        (['1765'], ['error']),
        (['1900'], ['False']),
        (['2024'], ['True'])
    ],
    'minion_game': [
        (['банана'], ['Стюарт 12']),
        (['арка'], ['Ничья']),
        (['пауэр'], ['Кевин 9'])
    ],
    'happiness': [
        (['3 2', '1 5 3', '3 1', '5 7'], ['1']),
        (['0 10'], ['error']),
        (['10 0'], ['error'])
    ],
    'matrix_mult': [
        (['2', '1 2', '2 3', '3 4', '5 6'], ['13 16', '21 26']),
        (['1'], ['error']),
        (['11'], ['error'])
    ]
}

def test_hello_world():
    assert run_script('hello_world.py') == 'Hello, world!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    assert run_script('lists.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join'])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', input_data).split('\n') == expected

def test_max_word():
    assert run_script('max_word.py') == 'сосредоточенности'

def test_price_sum():
    assert run_script('price_sum.py') == '6842.84 5891.06 6810.90'

@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game'])
def test_minion_game(input_data, expected):
    assert run_script('minion_game.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult'])
def test_matrix_mult(input_data, expected):
    assert run_script('matrix_mult.py', input_data).split('\n') == expected