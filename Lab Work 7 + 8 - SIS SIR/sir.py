# SIR Model
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Параметры модели
num_nodes = 20  # Количество вершин
edge_prob = 0.1  # Вероятность ребра (для разреженного графа; для плотного - 0.5)
p = 0.5  # Вероятность заражения от одного инфицированного соседа
q = 0.1  # Вероятность выздоровления
initial_infected = [0, 1]  # Начально инфицированные вершины
max_steps = 50  # Максимальное количество шагов
directed = False  # Неориентированный граф

# Создание графа
G = nx.erdos_renyi_graph(num_nodes, edge_prob, directed=directed)

# Инициализация состояний: 'S' - susceptible, 'I' - infected, 'R' - recovered
for node in G.nodes():
    G.nodes[node]['state'] = 'I' if node in initial_infected else 'S'

# История состояний для анимации
history = []
history.append([G.nodes[n]['state'] for n in G.nodes()])


# Функция одного шага модели SIR
def step_sir(G, p, q):
    new_states = {node: G.nodes[node]['state'] for node in G.nodes()}
    changes = False# Флаг, есть ли изменения на этом шаге

    # Проверка каждой вершины
    for node in G.nodes():
        current_state = new_states[node] # Текущее состояние вершины

        # Восприимчивые вершины могут заразиться
        if current_state == 'S':
            neighbors = list(G.neighbors(node))  # Получаем список соседей вершины
            infected_neighbors = [n for n in neighbors if new_states[n] == 'I'] # Выбираем только инфицированных соседей

            # Если есть инфицированные соседи
            if infected_neighbors:
                infection_prob = 1 - (1 - p) ** len(infected_neighbors)

                # Случайное событие: заразилась ли вершина на этом шаге
                if random.random() < infection_prob:
                    new_states[node] = 'I'
                    changes = True

        # Вершина инфицированная ('I')
        # Может выздороветь с вероятностью q
        elif current_state == 'I':
            if random.random() < q:
                new_states[node] = 'R'
                changes = True
        # 'R' остается 'R'

    # Применяем новые состояния
    for node, state in new_states.items():
        G.nodes[node]['state'] = state

    history.append([G.nodes[n]['state'] for n in G.nodes()])
    return changes


# Запуск модели на фиксированное количество шагов
for _ in range(max_steps):
    step_sir(G, p, q)

# Визуализация анимации
fig, ax = plt.subplots(figsize=(8, 8))
pos = nx.spring_layout(G, seed=42)


def get_color(state):
    if state == 'S':
        return 'green'
    elif state == 'I':
        return 'red'
    elif state == 'R':
        return 'blue'


def update(num):
    ax.clear()
    colors = [get_color(history[num][i]) for i in range(num_nodes)]
    nx.draw(G, pos, node_color=colors, with_labels=True, ax=ax, arrows=directed)
    ax.set_title(f"SIR Model - Step {num}\nS: green, I: red, R: blue")


ani = animation.FuncAnimation(fig, update, frames=len(history), interval=500, repeat=False)
plt.show()