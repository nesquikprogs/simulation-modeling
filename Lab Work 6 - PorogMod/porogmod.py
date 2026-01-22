import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Параметры модели
num_nodes = 10
threshold = 0.3  # Порог
initial_active = [0, 3]  # Начально активные вершины
directed = False
edge_prob = 0.3 # Вероятность соединения создания ребра между вершинами

# Создание случайного графа
if directed:
    G = nx.erdos_renyi_graph(num_nodes, edge_prob, directed=True)
else:
    G = nx.erdos_renyi_graph(num_nodes, edge_prob, directed=False)

# Добавление весов ребер от 0 до 1
for u, v in G.edges():
    G.edges[u, v]['weight'] = random.uniform(0, 1)

# Инициализация состояния вершин, где 1 активная(красная) и 0 неактивная(зеленая)
for node in G.nodes():
    G.nodes[node]['active'] = 1 if node in initial_active else 0

# История состояний для анимации
history = []
history.append([G.nodes[n]['active'] for n in G.nodes()])

# Функция одного шага модели
def step_activation(G, threshold):
    new_active = []
    for node in G.nodes():
        if G.nodes[node]['active'] == 0: # Только неактивные могут активироваться
            if directed:
                neighbors = list(G.predecessors(node)) # Входящие соседи
            else:
                neighbors = list(G.neighbors(node)) # Все соседи

            if neighbors: # Если есть соседи
                # Считаем общее влияние: активность * вес ребра
                total_influence = sum(G.nodes[u]['active'] * G[u][node].get('weight', 0) for u in neighbors)

                # Считаем средние влияние
                avg_influence = total_influence / len(neighbors)

                # Если среднее влияние больше порога, то активируем
                if avg_influence > threshold:
                    new_active.append(node)

    # Активируем все вершины, которые прошли порог
    for node in new_active:
        G.nodes[node]['active'] = 1
    history.append([G.nodes[n]['active'] for n in G.nodes()])
    return len(new_active) > 0

# Запуск модели до стабилизации
while step_activation(G, threshold):
    pass

# Визуализация анимации
fig, ax = plt.subplots(figsize=(6,6))
pos = nx.spring_layout(G, seed=42)

def update(num):
    ax.clear()
    colors = ['red' if history[num][i] else 'green' for i in range(num_nodes)]
    nx.draw(G, pos, node_color=colors, with_labels=True, ax=ax, arrows=directed)
    ax.set_title(f"Step {num}")

ani = animation.FuncAnimation(fig, update, frames=len(history), interval=1000, repeat=False)
plt.show()