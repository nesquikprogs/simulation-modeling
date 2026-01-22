import tkinter as tk
import random

# Параментры модели

ROWS = 30
COLS = 30
CELL_SIZE = 20
DELAY = 300

INFECTION_PROB = 0.3     # вероятность заражения
RECOVERY_TIME = 10       # шагов до выздоровления

# Состояния
SUSCEPTIBLE = 0  # здоров
INFECTED = 1     # заражён
RECOVERED = 2    # выздоровел


# Клеточный автомат

class EpidemicModel:
    """
    Клеточный автомат распространения эпидемии
    """

    # Начальное состояние
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        # Основное поле состояний
        self.grid = [[SUSCEPTIBLE for _ in range(cols)]
                     for _ in range(rows)]

        # Время заражения для каждой клетки
        self.infection_time = [[0 for _ in range(cols)]
                               for _ in range(rows)]

        # Инициализация: несколько заражённых
        for _ in range(10):
            i = random.randint(0, rows - 1)
            j = random.randint(0, cols - 1)
            self.grid[i][j] = INFECTED

    # Подсчет количества заболевших соседей в окрестности Мура
    def count_infected_neighbors(self, row: int, col: int) -> int:
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                if 0 <= i < self.rows and 0 <= j < self.cols:
                    if self.grid[i][j] == INFECTED:
                        count += 1
        return count

    # Один шаг моделирования
    def next_step(self):
        new_grid = [row[:] for row in self.grid]

        for i in range(self.rows):
            for j in range(self.cols):

                # Здоровья может заразиться
                if self.grid[i][j] == SUSCEPTIBLE:
                    infected_neighbors = self.count_infected_neighbors(i, j)
                    if infected_neighbors > 0:
                        if random.random() < INFECTION_PROB:
                            new_grid[i][j] = INFECTED
                            self.infection_time[i][j] = 0

                # Зараженная выздоравливает и больше не заражается
                elif self.grid[i][j] == INFECTED:
                    self.infection_time[i][j] += 1
                    if self.infection_time[i][j] >= RECOVERY_TIME:
                        new_grid[i][j] = RECOVERED

        self.grid = new_grid


# Визуализация

class EpidemicGUI:

    def __init__(self, root: tk.Tk, model: EpidemicModel):
        self.root = root
        self.model = model

        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="white"
        )
        self.canvas.pack()

        self.update()

    def draw(self):
        self.canvas.delete("all")

        for i in range(self.model.rows):
            for j in range(self.model.cols):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                state = self.model.grid[i][j]

                if state == SUSCEPTIBLE:
                    color = "white"
                elif state == INFECTED:
                    color = "red"
                else:
                    color = "green"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="gray"
                )

    def update(self):
        self.draw()
        self.model.next_step()
        self.root.after(DELAY, self.update)


# Точка входа

def main():
    root = tk.Tk()
    root.title("Клеточный автомат: распространение эпидемии")

    model = EpidemicModel(ROWS, COLS)
    EpidemicGUI(root, model)

    root.mainloop()


if __name__ == "__main__":
    main()
