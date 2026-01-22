
import random
import math
from collections import deque
from dataclasses import dataclass
from typing import List, Optional
import numpy as np


# Заявка
@dataclass
class Request:
    id: int                          # Номер заявки (для отладки)
    arrival_time: int                # Тик прибытия в систему
    service_time: int                # Время обработки (тики, 100–1600)
    wait_start: Optional[int] = None # Когда попала в очередь
    processing_start: Optional[int] = None  # Когда начала обслуживаться
    finish_time: Optional[int] = None       # Когда завершена


# Генератор заявок
class ExponentialGenerator:
    def __init__(self, lambda_rate: float, ticks_per_second: int):
        self.lambda_rate = lambda_rate           # λ = 0.4 → средний интервал = 2.5 сек
        self.ticks_per_second = ticks_per_second # 1 сек = 100 тиков
        self.time_to_next = 0                    # Сколько тиков до следующей заявки

    def tick(self):
        # Каждый тик уменьшаем счётчик
        if self.time_to_next > 0:
            self.time_to_next -= 1
            return None
        else:
            # Генерируем экспоненциальный интервал
            interarrival = -math.log(1 - random.random()) / self.lambda_rate
            self.time_to_next = round(interarrival * self.ticks_per_second)
            return self.time_to_next  # Возвращаем, что пора генерировать заявку


# Очередь
class Queue:
    def __init__(self, max_length: int):
        self.max_length = max_length  # Максимум 30 заявок
        self.requests = deque()       # FIFO: первый пришёл — первый обслужен

    def add(self, request: Request) -> bool:
        if len(self.requests) < self.max_length:
            self.requests.append(request)
            return True
        return False  # Очередь полная → заявка отброшена

    def pop(self) -> Optional[Request]:
        return self.requests.popleft() if self.requests else None

    def __len__(self):
        return len(self.requests)


# Процессор(3 паралельных канала)
class Processor:
    def __init__(self):
        self.current_request: Optional[Request] = None
        self.remaining_time: int = 0  # Сколько тиков осталось

    def is_busy(self) -> bool:
        return self.current_request is not None

    def start_processing(self, request: Request, current_tick: int):
        self.current_request = request
        self.remaining_time = request.service_time
        request.processing_start = current_tick  # Запоминаем начало

    def tick(self, current_tick) -> Optional[Request]:
        if not self.is_busy():
            return None
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            finished = self.current_request
            finished.finish_time = current_tick
            self.current_request = None
            self.remaining_time = 0
            return finished  # Заявка завершена
        return None


# Главный класс
class SMOSimulation:
    def __init__(
        self,
        total_ticks: int,
        lambda_rate: float,
        service_min: int,
        service_max: int,
        queue_length: int,
        num_processors: int,
        ticks_per_second: int = 100
    ):
        # Параметры модели
        self.total_ticks = total_ticks
        self.lambda_rate = lambda_rate
        self.service_min = service_min
        self.service_max = service_max
        self.queue_length = queue_length
        self.num_processors = num_processors
        self.ticks_per_second = ticks_per_second

        # Компоненты СМО
        self.generator = ExponentialGenerator(lambda_rate, ticks_per_second)
        self.queue = Queue(queue_length)
        self.processors = [Processor() for _ in range(num_processors)]  # 3 канала
        self.rejected = []    # Не попали в очередь
        self.completed = []   # Обслужены

        # Статистика (для графиков и анализа)
        self.queue_history = []
        self.completed_history = []
        self.rejected_history = []
        self.wait_times = []
        self.service_times = []

        self.request_counter = 0
        self.current_tick = 0

    def run(self):
        # Основной цикл имитации
        for tick in range(self.total_ticks):
            self.current_tick = tick
            self._step()              # Один тик системы
            self._collect_stats()     # Сохраняем данные

        self._finalize_stats()

    def _step(self):
        # 1: Завершить обработку
        for processor in self.processors:
            finished = processor.tick(self.current_tick)
            if finished:
                self.completed.append(finished)
                # Время ожидания = начало обработки - начало ожидания
                wait = (finished.processing_start - finished.wait_start)
                self.wait_times.append(wait)
                self.service_times.append(finished.service_time)

        # 2: Переместить из очереди в свободный процессор
        for processor in self.processors:
            if not processor.is_busy() and len(self.queue) > 0:
                req = self.queue.pop()
                if req.wait_start is None:
                    req.wait_start = self.current_tick  # Начало ожидания
                processor.start_processing(req, self.current_tick)

        # 3: Увеличить время ожидания в очереди
        for req in self.queue.requests:
            if req.wait_start is None:
                req.wait_start = self.current_tick

        # 4: Генерация новой заявки
        next_in = self.generator.tick()
        if next_in is not None:
            self.request_counter += 1
            service_time = random.randint(self.service_min, self.service_max)
            new_req = Request(
                id=self.request_counter,
                arrival_time=self.current_tick,
                service_time=service_time
            )
            if not self.queue.add(new_req):
                self.rejected.append(new_req)  # Очередь полная

    def _collect_stats(self):
        # Сохраняем состояние каждый тик — для графиков
        self.queue_history.append(len(self.queue))
        self.completed_history.append(len(self.completed))
        self.rejected_history.append(len(self.rejected))

    def _finalize_stats(self):
        pass  # Всё уже собрано

    def get_stats(self):
        # Анализ
        from scipy import stats
        wait_arr = np.array(self.wait_times)
        service_arr = np.array(self.service_times)
        return {
            "processed": len(self.completed),
            "rejected": len(self.rejected),
            "in_queue": len(self.queue),
            "in_processors": sum(1 for p in self.processors if p.is_busy()),
            "wait_stats": stats.describe(wait_arr) if len(wait_arr) > 0 else None,
            "service_stats": stats.describe(service_arr) if len(service_arr) > 0 else None,
            "queue_history": self.queue_history,
            "completed_history": self.completed_history,
            "rejected_history": self.rejected_history,
            "wait_times": self.wait_times
        }