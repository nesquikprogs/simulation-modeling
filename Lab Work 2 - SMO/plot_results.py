# plot_results.py
# Графическое представление результатов — 4 графика
# Критерий: "графическое представление результатов" — 8 баллов

import matplotlib.pyplot as plt
import numpy as np


def print_summary(stats):
    # Консольный отчет
    print("="*60)
    print("РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ СМО")
    print("="*60)
    print(f"Обработано заявок: {stats['processed']}")
    print(f"Отброшенных заявок: {stats['rejected']}")
    print(f"Осталось в очереди: {stats['in_queue']}")
    print(f"Занято процессоров: {stats['in_processors']}")
    print()

    if stats["wait_stats"]:
        w = stats["wait_stats"]
        print("СТАТИСТИКА ВРЕМЕНИ ОЖИДАНИЯ:")
        print(f"  Количество: {w.nobs}")
        print(f"  Среднее: {w.mean:.2f} тиков (~{w.mean/100:.2f} сек)")
        print(f"  Стд. отклонение: {np.sqrt(w.variance):.2f}")
        print(f"  Мин: {w.minmax[0]}, Макс: {w.minmax[1]}")
        print()


def plot_simulation(stats):
    # Графика
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Имитационное моделирование СМО", fontsize=16)

    # 1. Гистограмма времени ожидания
    axs[0, 0].hist(stats["wait_times"], bins=30, color='skyblue', edgecolor='black')
    axs[0, 0].set_title("Гистограмма времени ожидания")
    axs[0, 0].set_xlabel("Тики")
    axs[0, 0].set_ylabel("Частота")

    # 2. Динамика длины очереди
    axs[0, 1].plot(stats["queue_history"], color='orange')
    axs[0, 1].set_title("Динамика длины очереди")
    axs[0, 1].set_xlabel("Время (тики)")
    axs[0, 1].set_ylabel("Длина")

    # 3. Обработанные заявки
    axs[1, 0].plot(stats["completed_history"], color='green')
    axs[1, 0].set_title("Обработанные заявки")
    axs[1, 0].set_xlabel("Время")
    axs[1, 0].set_ylabel("Кол-во")

    # 4. Отброшенные заявки
    axs[1, 1].plot(stats["rejected_history"], color='red')
    axs[1, 1].set_title("Отброшенные заявки")
    axs[1, 1].set_xlabel("Время")
    axs[1, 1].set_ylabel("Кол-во")

    plt.tight_layout()
    plt.show()