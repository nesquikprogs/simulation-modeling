import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# параметры
N_STATES = 30           # Количество состояний
ABSORBING_STATE = 29    # Поглощающее состояние
N_TRAJECTORIES = 1000   # Количество траекторий
MAX_STEPS = 200         # Макс. шагов на траекторию

# Генерация распределения вероятностей
def generate_distribution(n):
    vals = [random.random() for _ in range(n)]
    total = sum(vals)
    return [v / total for v in vals]

# Генерация матрицы переходов
def generate_transition_matrix(n, absorbing):
    matrix = []
    for i in range(n):
        if i == absorbing:
            row = [0.0] * n
            row[i] = 1.0  # Поглощающее: остаётся в себе
        else:
            row = generate_distribution(n)
            # row[absorbing] *= 1.5  # Можно усилить притяжение
        matrix.append(row)
    return matrix

# Один шаг по распределению
def next_state(prob_vector):
    r = random.random()
    cumulative = 0.0
    for i, prob in enumerate(prob_vector):
        cumulative += prob
        if r < cumulative:
            return i
    return len(prob_vector) - 1

# Одна траектория с временем до поглощения
def simulate_trajectory(matrix, absorbing, max_steps):
    state = random.randint(0, N_STATES - 1)
    if state == absorbing:
        return [state], 0  # Уже в поглощающем

    trajectory = [state]
    steps = 0

    while state != absorbing and steps < max_steps:
        state = next_state(matrix[state])
        trajectory.append(state)
        steps += 1
        if state == absorbing:
            return trajectory, steps

    return trajectory, max_steps  # Не попал за max_steps

# Основная симуляция
random.seed(42)
transition_matrix = generate_transition_matrix(N_STATES, ABSORBING_STATE)

absorption_times = []
all_final_states = []

print("Запуск 1000 траекторий...")
for _ in range(N_TRAJECTORIES):
    traj, time_to_absorb = simulate_trajectory(transition_matrix, ABSORBING_STATE, MAX_STEPS)
    absorption_times.append(time_to_absorb)
    all_final_states.append(traj[-1])

# Вывод статистики
absorption_times = np.array(absorption_times)
final_counts = np.bincount(all_final_states, minlength=N_STATES)

print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ ЦЕПИ МАРКОВА")
print("="*60)
print(f"Поглощающее состояние: {ABSORBING_STATE}")
print(f"Траекторий: {N_TRAJECTORIES}")
print(f"Попало в поглощающее: {np.sum(np.array(all_final_states) == ABSORBING_STATE)}")
print(f"Среднее время до поглощения: {absorption_times.mean():.2f} шагов")
print(f"Медиана: {np.median(absorption_times):.2f}")
print(f"Мин: {absorption_times.min()}, Макс: {absorption_times.max()}")
print(f"Не попало за {MAX_STEPS} шагов: {np.sum(absorption_times == MAX_STEPS)}")









# Графики


fig = plt.figure(figsize=(15, 10))

# 1. Пример траектории
ax1 = fig.add_subplot(2, 2, 1)
sample_traj, _ = simulate_trajectory(transition_matrix, ABSORBING_STATE, MAX_STEPS)
ax1.plot(sample_traj, 'b-o', markersize=3, linewidth=1)
ax1.axhline(y=ABSORBING_STATE, color='r', linestyle='--', label=f'Поглощающее ({ABSORBING_STATE})')
ax1.set_title("Пример траектории")
ax1.set_xlabel("Шаг")
ax1.set_ylabel("Состояние")
ax1.legend()

# 2. Частоты финальных состояний
ax2 = fig.add_subplot(2, 2, 2)
ax2.bar(range(N_STATES), final_counts, color='skyblue', edgecolor='black')
ax2.bar(ABSORBING_STATE, final_counts[ABSORBING_STATE], color='red')
ax2.set_title("Частоты финальных состояний")
ax2.set_xlabel("Состояние")
ax2.set_ylabel("Количество траекторий")

# 3. Гистограмма времени до поглощения
ax3 = fig.add_subplot(2, 2, 3)
successful_times = absorption_times[absorption_times < MAX_STEPS]
ax3.hist(successful_times, bins=30, color='lightgreen', edgecolor='black')
ax3.set_title("Гистограмма времени до поглощения")
ax3.set_xlabel("Шаги")
ax3.set_ylabel("Частота")

# 4. График переходов (матрица)
ax4 = fig.add_subplot(2, 2, 4)
im = ax4.imshow(transition_matrix, cmap='Blues', aspect='auto')
ax4.set_title("Матрица переходных вероятностей")
ax4.set_xlabel("След. состояние")
ax4.set_ylabel("Тек. состояние")
plt.colorbar(im, ax=ax4, label="Вероятность")

plt.tight_layout()
plt.show()

# === scipy.stats.describe ===
if len(successful_times) > 0:
    desc = stats.describe(successful_times)
    print("\nСТАТИСТИКА (scipy.stats.describe):")
    print(f"  N: {desc.nobs}")
    print(f"  Среднее: {desc.mean:.2f}")
    print(f"  Дисперсия: {desc.variance:.2f}")
    print(f"  Асимметрия: {desc.skewness:.2f}")
    print(f"  Эксцесс: {desc.kurtosis:.2f}")