# SIS Model
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Параметры модели
num_nodes = 20  # Количество вершин
edge_prob = 0.1  # Вероятность создание ребра
p = 0.05  # Вероятность заражения от одного инфицированного соседа
q = 0.1  # Вероятность выздоровления
initial_infected = [0, 1]  # Начально инфицированные вершины
max_steps = 50  # Максимальное количество шагов
directed = False  # Неориентированный граф

# Создание случайного графа
G = nx.erdos_renyi_graph(num_nodes, edge_prob, directed=directed)

# Инициализация состояний: 'S' - susceptible, 'I' - infected
for node in G.nodes():
    G.nodes[node]['state'] = 'I' if node in initial_infected else 'S'

# История состояний для анимации
history = []
history.append([G.nodes[n]['state'] for n in G.nodes()])


# Функция одного шага модели SIS
def step_sis(G, p, q):
    new_states = {node: G.nodes[node]['state'] for node in G.nodes()}
    changes = False

    # Проверка для каждой вершины
    for node in G.nodes():
        current_state = new_states[node]

        # Если вершина восприимчивая (S), может заразиться
        if current_state == 'S':
            neighbors = list(G.neighbors(node))
            infected_neighbors = [n for n in neighbors if new_states[n] == 'I']
            if infected_neighbors:

                # Вычисляем вероятность заражения с учётом всех инфицированных соседей
                infection_prob = 1 - (1 - p) ** len(infected_neighbors)
                if random.random() < infection_prob:
                    new_states[node] = 'I' # Вершина заражается
                    changes = True

        # Если вершина инфицированная (I), может выздороветь
        elif current_state == 'I':
            if random.random() < q:
                new_states[node] = 'S' # Выздоровление Е относительно вероятности
                changes = True

    # Применяем новые состояния
    for node, state in new_states.items():
        G.nodes[node]['state'] = state

    history.append([G.nodes[n]['state'] for n in G.nodes()])
    return changes


# Запуск модели на фиксированное количество шагов
for _ in range(max_steps):
    step_sis(G, p, q)

# Визуализация анимации
fig, ax = plt.subplots(figsize=(8, 8))
pos = nx.spring_layout(G, seed=42)


def get_color(state):
    if state == 'S':
        return 'green'
    elif state == 'I':
        return 'red'


def update(num):
    ax.clear()
    colors = [get_color(history[num][i]) for i in range(num_nodes)]
    nx.draw(G, pos, node_color=colors, with_labels=True, ax=ax, arrows=directed)
    ax.set_title(f"SIS Model - Step {num}\nS: green, I: red")


ani = animation.FuncAnimation(fig, update, frames=len(history), interval=500, repeat=False)
plt.show()