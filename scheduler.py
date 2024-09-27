from collections import deque
from process import Process, ProcessType

class Scheduler:
    def __init__(self):
        self.queues = {
            5: deque(),  # Add this line
            4: deque(),
            3: deque(),
            2: deque(),
            1: deque()
        }

    def add_process(self, system_prompt, user_prompt, process_type):
        process = Process(system_prompt, user_prompt, process_type)
        self.queues[process.priority].append(process)

    def get_next_process(self):
        for priority in range(4, 0, -1):
            if self.queues[priority]:
                return self.queues[priority].popleft()
        return None

    def update_priorities(self):
        for priority in range(1, 5):  # Change this line from 4 to 5
            for process in self.queues[priority]:
                process.increase_age()
                if process.priority > priority:
                    self.queues[priority].remove(process)
                    self.queues[process.priority].append(process)