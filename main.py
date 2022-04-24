# Неевин Кирилл P3213
# Вариант 11

from collections import defaultdict
from functools import reduce
from math import log
from prettytable import PrettyTable
import matplotlib.pyplot as plt


def main():
    input_data = [
        0.92, -1.05, 1.04, 1.55, 0.92,
        -0.49, 1.49, 0.40, -0.61, 0.13,
        0.51, -1.41, -1.03, -0.17, 0.17,
        -0.25, -1.48, 0.64, 0.43, 0.91,
    ]

    print('Исходный ряд:')
    print(input_data)

    print('Вариационный ряд (отсортированные данные):')
    srtd_data = sorted(input_data)
    print(srtd_data)

    print(f'Первая и последняя порядковая статистика (макс. и мин. значения): {srtd_data[0]} и {srtd_data[-1]}')
    print(f'Размах: {srtd_data[-1] - srtd_data[0]:.2f}')

    print()
    print('Статистический ряд (сколько элементов в выборке):')
    count_set = defaultdict(int)
    for x in srtd_data:
        count_set[x] += 1

    static_table = PrettyTable()
    static_table.field_names = ['x(i)', *count_set.keys()]
    static_table.add_row(['n(i)', *count_set.values()])
    print(static_table)

    avg = sum(input_data) / len(input_data)
    print('Выборочное среднее:', avg)
    dispersion = reduce(lambda d, val: d + (val - avg)**2, input_data, 0)
    print('Дисперсия:', dispersion)
    print('СКО:', dispersion ** 0.5)

    print()
    f, axs = plt.subplots(2, 2, figsize=(6, 7))
    print(len(axs))
    plt.subplot(5, 1, 1)
    plt.title('Эмпирическая функции распределения')
    n, keys, y = len(count_set), list(count_set.keys()), 0

    print('Эмпирическая функция:')
    print(f'{y:.2f}, при x <= {keys[0]}')
    for i in range(n - 1):
        y += count_set[keys[i]] / n if i < n else 0
        print(f'{y:.2f}, при {keys[i]} < x <= {keys[i + 1]}')
        plt.plot([keys[i], keys[i + 1]], [y, y], c='orange')
    print(f'{y:.2f}, при {keys[-1]} < x')

    print()
    print('Интервальное статистическое распределение:')
    h = round((srtd_data[-1] - srtd_data[0]) / (1 + round(log(n, 2))), 2)  # ширина столбца гистограммы
    curr_x = round(srtd_data[0] - h / 2, 2)  # начало стоблца гистограммы
    next_x = round(curr_x + h, 2)  # конец стоблца гистограммы
    grouped_data = {curr_x: 0}
    for x in srtd_data:
        if x < next_x:
            grouped_data[curr_x] += 1 / n
        else:
            grouped_data[next_x] = 1 / n
            curr_x = next_x
            next_x = round(next_x + h, 2)
    static_table = PrettyTable()
    static_table.field_names = (f'[{x:.2f}; {x+h:.2f})' for x in grouped_data.keys())
    static_table.add_row(list(round(x, 2) for x in grouped_data.values()))
    print(static_table)

    plt.subplot(5, 1, 3)
    plt.title('Полигон частот')
    plt.plot(list(grouped_data.keys()), list(grouped_data.values()), c='orange')

    plt.subplot(5, 1, 5)
    plt.title('Гистограмма частот')
    plt.bar(list(map(lambda x: x + h / 2, grouped_data.keys())), list(grouped_data.values()), width=h, color='orange')
    xticks = list(grouped_data.keys()) + [round(list(grouped_data.keys())[-1] + h, 2)]
    plt.xticks(xticks, xticks)

    plt.savefig(f'graph.png')
    plt.show()


if __name__ == '__main__':
    main()
