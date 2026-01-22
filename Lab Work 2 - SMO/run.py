# Запуск имитации — параметры модели

from simulation import SMOSimulation
from plot_results import print_summary, plot_simulation


def main():
    # Параметры модели
    TOTAL_TICKS = 1_000_000           # ~2.78 часа
    LAMBDA = 0.4                      # Интенсивность потока
    SERVICE_MIN = 100                 # 1 секунда
    SERVICE_MAX = 1600                # 16 секунд
    QUEUE_LENGTH = 30                 # Конечная очередь
    NUM_PROCESSORS = 3                # Многоканальная СМО
    TICKS_PER_SECOND = 100            # 1 сек = 100 тиков

    print("Запуск имитации СМО...")
    sim = SMOSimulation(
        total_ticks=TOTAL_TICKS,
        lambda_rate=LAMBDA,
        service_min=SERVICE_MIN,
        service_max=SERVICE_MAX,
        queue_length=QUEUE_LENGTH,
        num_processors=NUM_PROCESSORS,
        ticks_per_second=TICKS_PER_SECOND
    )

    sim.run()
    stats = sim.get_stats()

    print_summary(stats)      # Консоль
    plot_simulation(stats)    # Графики


if __name__ == "__main__":
    main()