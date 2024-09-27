from enum import Enum

class ProcessType(Enum):
    HOUSEKEEPING = 1
    LLM_INITIATED = 2
    USER_SUBPROCESS = 3
    USER = 4
    SYSTEM = 5

class Process:
    def __init__(self, system_prompt, user_prompt, process_type):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.process_type = process_type
        self.token_allowance = self.get_token_allowance()
        self.priority = self.get_initial_priority()
        self.age = 0
        self.completed = False

    def get_token_allowance(self):
        allowances = {
            ProcessType.HOUSEKEEPING: 500,
            ProcessType.LLM_INITIATED: 1000,
            ProcessType.USER_SUBPROCESS: 2000,
            ProcessType.USER: 4000,
            ProcessType.SYSTEM: 3000  # Add this line
        }
        return allowances[self.process_type]

    def get_initial_priority(self):
        priorities = {
            ProcessType.HOUSEKEEPING: 1,
            ProcessType.LLM_INITIATED: 2,
            ProcessType.USER_SUBPROCESS: 3,
            ProcessType.USER: 4,
            ProcessType.SYSTEM: 5  # Add this line
        }
        return priorities[self.process_type]

    def increase_age(self):
        self.age += 1
        if self.age % 5 == 0 and self.priority < 4:
            self.priority += 1

    def mark_completed(self):
        self.completed = True