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
