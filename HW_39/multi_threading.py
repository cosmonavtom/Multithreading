import threading
from random import randint


def create_list():
    '''Общая(для заданий) функция для ввода списка с клавиатуры'''
    while True:
        str_inp = input('Введите значения списка через пробел: ')
        str_list = str_inp.split()
        try:
            num_list = []
            for symbol in str_list:
                num_list.append(int(symbol))
            return num_list
        except ValueError:
            print('Неверный ввод')


def print_extremums(extremum_num, event_for_wait, event_for_set):
    '''Также общая функция для таргета первых двух заданий'''
    for _ in range(5):
        event_for_wait.wait()
        event_for_wait.clear()
        print(extremum_num, end=' ')
        event_for_set.set()


# Задание 1
print('Задание 1')
lst = create_list()
event_min = threading.Event()
event_max = threading.Event()

thread_min = threading.Thread(target=print_extremums, args=(min(lst), event_min, event_max))
thread_max = threading.Thread(target=print_extremums, args=(max(lst), event_max, event_min))

thread_min.start()
thread_max.start()

event_min.set()

thread_min.join()
thread_max.join()

# Задание 2
print('\n\nЗадание 2')
lst = create_list()
event_sum = threading.Event()
event_average = threading.Event()

thread_sum = threading.Thread(target=print_extremums, args=(sum(lst), event_min, event_max))
thread_average = threading.Thread(target=print_extremums, args=(round((sum(lst) / len(lst)), 1), event_max, event_min))

thread_sum.start()
thread_average.start()

event_sum.set()

thread_sum.join()
thread_average.join()

# Задание 3
print('\n\nЗадание 3')
'''Надеюсь я правильно понял задание. Первый поток полностью отрабатывает заполнение списка
   случайными числами. После его полной отработки одновременно запускаются 2 потока по нахождению
   суммы элементов и среднеарифметического значения. И только потом вывести всё на экран
'''
random_list = []
summ = None
average = None


def create_rnd_list():
    global random_list
    for _ in range(10):
        random_list.append(randint(-10, 10))


def find_sum():
    global random_list, summ
    summ = sum(random_list)


def find_average():
    global random_list, average
    average = round(sum(random_list) / len(random_list), 1)


thread_create_list = threading.Thread(target=create_rnd_list)
thread_find_sum = threading.Thread(target=find_sum)
thread_find_average = threading.Thread(target=find_average)

# Запускаем первый поток для генерации списка
thread_create_list.start()
# Дождались окончания работы потока
thread_create_list.join()


# Запускаем сразу два потока по сумме и среднеарифметическому
thread_find_sum.start()
thread_find_average.start()

# Дожидаемся окончания их работы
thread_find_sum.join()
thread_find_average.join()

# И только теперь выводим результат работы
print(f'Сгенерированный список - {random_list}')
print(f'Сумма элементов = {summ}')
print(f'Среднее арифметическое = {average}')

# Задание 4
print('\n\nЗадание 4')

filename = input('Введите имя файла(без расширения): ')

# Глобальные переменные для статистики. q-primes - считает кол-во простых чисел
# max_fact и min_fact - максимальный и минимальный факториалы
q_primes = 0
max_fact, min_fact = None, None


def create_rnd_file(filename):
    '''Функция создаёт заданный файл с раширением *.txt и заполняет
    его случайными целыми числами от 1 до 100 включительно'''
    with open(f'{filename}.txt', 'w', encoding='utf-8') as f:
        lst = [randint(1, 101) for _ in range(20)]
        for num in lst:
            f.write(str(num) + ' ')


def is_prime(n):
    '''Проверяет, является ли число простым'''
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def find_primes(filename):
    '''Находит все простые числа в файле и записываем в файл primes.txt'''
    primes = []
    global q_primes
    with open(f'{filename}.txt', 'r') as f:
        lst = f.read().split()
        for num in lst:
            if is_prime(int(num)):
                primes.append(num)
    with open('primes.txt', 'w', encoding='utf-8') as f:
        f.write(str(primes))
    q_primes = len(primes)


def factorial(n):
    '''Вычисляет факториал числа n'''
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def calc_factorials(filename):
    '''Вычисляем факториал каждого числа в файле и записываем в файл factorials.txt
    В отличие от простых чисел здесь будем записывать построчно, потому что
    факториалы огромные и плохочитаемые подряд'''
    factorials = []
    global max_fact, min_fact
    with open(f'{filename}.txt', 'r') as f:
        lst = f.read().split()
        for num in lst:
            factorials.append(factorial(int(num)))
    with open('factorials.txt', 'w', encoding='utf-8') as f:
        for fact in factorials:
            f.write(str(fact) + '\n')
    max_fact = max(factorials)
    min_fact = min(factorials)


thread_create_file = threading.Thread(target=create_rnd_file, args=(filename,))
thread_find_primes = threading.Thread(target=find_primes, args=(filename,))
thread_factorials = threading.Thread(target=calc_factorials, args=(filename,))

thread_create_file.start()
thread_create_file.join()

print(f'В файл {filename}.txt записаны 20 случайных целых чисел')
print('Начинаю поиск целых чисел и расчёт факториалов')
print('...')
thread_find_primes.start()
thread_factorials.start()

thread_find_primes.join()
thread_factorials.join()
print(f'В файл primes.txt записаны целые числа')
print(f'В файл factorials.txt записаны факториалы\n')
print(f'Всего найдено {q_primes} простых чисел')
print(f'Максимальный факториал - {max_fact}')
print(f'Минимальный факториал - {min_fact}')

