from enum import Enum, auto
from collections import deque

class InterruptType(Enum):
    USER_INPUT = auto()
    TIMER = auto()
    SYSTEM = auto()

class Interrupt:
    def __init__(self, type, data=None):
        self.type = type
        self.data = data

class InterruptHandler:
    def __init__(self):
        self.interrupt_queue = deque()

    def add_interrupt(self, interrupt_type, data=None):
        self.interrupt_queue.append(Interrupt(interrupt_type, data))

    def get_next_interrupt(self):
        return self.interrupt_queue.popleft() if self.interrupt_queue else None