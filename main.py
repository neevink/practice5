# Неевин Кирилл P3213
# Вариант 11
from collections import defaultdict
from math import log
from prettytable import PrettyTable
import matplotlib.pyplot as plt


def main():
    data = [
        0.92, -1.05, 1.04, 1.55, 0.92,
        -0.49, 1.49, 0.40, -0.61, 0.13,
        0.51, -1.41, -1.03, -0.17, 0.17,
        -0.25, -1.48, 0.64, 0.43, 0.91,
    ]

    print('Исходный ряд:')
    print(data)

    print('Вариационный ряд (отсортированные данные):')
    sorted_data = sorted(data)
    print(sorted_data)

    print(f'Первая и последняя порядковая статистика (макс. и мин. значения): {sorted_data[0]} и {sorted_data[-1]}')
    print(f'Размах: {sorted_data[-1] - sorted_data[0]:.2f}')

    print('Статистический ряд (сколько элементов в выборке):')
    count_set = defaultdict(int)
    for x in sorted_data:
        count_set[x] += 1

    table = PrettyTable()
    table.field_names = ['x(i)', *count_set.keys()]
    table.add_row(['n(i)', *count_set.values()])
    print(table)

    avg = sum(data) / len(data)
    print('Выборочное среднее:', avg)

    dispersion = 0
    for x in data:
        dispersion += (x - avg) ** 2
    print('Дисперсия:', dispersion)
    print('СКО:', dispersion ** 0.5)

    print('Эмпирическая функция:')
    plt.subplot(5, 1, 1)
    plt.title('График эмпирической функции распределения')
    n = len(count_set)
    keys = list(count_set.keys())
    y = 0
    print(f'\t\t/ {round(y, 2)}, при x <= {keys[0]}')
    for i in range(n - 1):
        y += count_set[keys[i]] / n if i < n else 0
        left = 'F*(x) = ' if i == n / 2 else '\t\t'
        print(f'{left}| {round(y, 2)}, при {keys[i]} < x <= {keys[i + 1]}')
        plt.plot([keys[i], keys[i + 1]], [y, y], c='black')
    print(f'\t\t\\ {round(y, 2)}, при {keys[-1]} < x')

    print('Интервальное статистическое распределение:')
    h = round((sorted_data[-1] - sorted_data[0]) / (1 + round(log(n, 2))), 2)
    curr_x = round(sorted_data[0] - h / 2, 2)
    next_x = round(curr_x + h, 2)
    grouped_data = {curr_x: 0}
    for x in sorted_data:
        if x < next_x:
            grouped_data[curr_x] += 1 / n
        else:
            grouped_data[next_x] = 1 / n
            curr_x = next_x
            next_x = round(next_x + h, 2)
    table = PrettyTable()
    table.field_names = (f'[{round(x, 2)}; {round(x + h, 2)})' for x in grouped_data.keys())
    table.add_row(list(round(x, 2) for x in grouped_data.values()))
    print(table)

    plt.subplot(5, 1, 3)
    plt.title('Полигон частот')
    plt.plot(list(grouped_data.keys()), list(grouped_data.values()), c='black')

    plt.subplot(5, 1, 5)
    plt.title('Гистограмма частот')
    plt.bar(list(map(lambda x: x + h / 2, grouped_data.keys())), list(grouped_data.values()), width=h)
    xticks = list(grouped_data.keys()) + [round(list(grouped_data.keys())[-1] + h, 2)]
    plt.xticks(xticks, xticks)
    plt.show()


if __name__ == '__main__':
    main()
