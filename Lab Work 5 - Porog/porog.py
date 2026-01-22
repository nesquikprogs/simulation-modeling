import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Параметры
num_nodes = 10                # Количество вершин
threshold = 1                # Порог активации
initial_active = [0, 3]       # Индексы изначально активированных вершин
directed = False               # True - ориентированный граф, False - неориентированный
edge_prob = 0.3                # Вероятность ребра для генерации графа

# Создание случайного графа
if directed:
    G = nx.erdos_renyi_graph(num_nodes, edge_prob, directed=True)
else:
    G = nx.erdos_renyi_graph(num_nodes, edge_prob, directed=False)

# Инициализация состояния вершин: 0 - неактивна, 1 - активна
for node in G.nodes():
    G.nodes[node]['active'] = 1 if node in initial_active else 0

# История состояний для анимации
history = []
history.append([G.nodes[n]['active'] for n in G.nodes()])

# Функция одного шага активации
def step_activation(G, threshold):
    """Один шаг модели пороговой активации"""
    new_active = []
    for node in G.nodes():
        if G.nodes[node]['active'] == 0:
            # Считаем количество активных соседей
            if directed:
                neighbors = G.predecessors(node)  # для ориентированного графа
            else:
                neighbors = G.neighbors(node)
            active_neighbors = sum(G.nodes[n]['active'] for n in neighbors)
            if active_neighbors >= threshold:
                new_active.append(node)
    # Обновляем состояние вершин
    for node in new_active:
        G.nodes[node]['active'] = 1
    # Сохраняем текущее состояние
    history.append([G.nodes[n]['active'] for n in G.nodes()])
    return len(new_active) > 0  # True, если есть изменения

# Запуск модели до стабилизации
while step_activation(G, threshold):
    pass

# Визуализация анимации
fig, ax = plt.subplots(figsize=(6,6))
pos = nx.spring_layout(G, seed=42)  # Позиции вершин

def update(num):
    ax.clear()
    colors = ['red' if history[num][i]==1 else 'green' for i in range(num_nodes)]
    nx.draw(G, pos, node_color=colors, with_labels=True, ax=ax, arrows=directed)
    ax.set_title(f"Step {num}")

ani = animation.FuncAnimation(fig, update, frames=len(history), interval=1000, repeat=False)
plt.show()
