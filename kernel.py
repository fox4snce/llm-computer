import socket
import json
import threading
import time
from scheduler import Scheduler
from process import ProcessType
from interrupt import InterruptHandler, InterruptType
from llm_utils import generate_response

class LLMKernel:
    def __init__(self, host='localhost', port=5000):
        self.running = False
        self.scheduler = Scheduler()
        self.interrupt_handler = InterruptHandler()
        self.current_process = None
        self.host = host
        self.port = port
        self.server_socket = None

    def add_process(self, system_prompt, user_prompt, process_type):
        self.scheduler.add_process(system_prompt, user_prompt, process_type)

    def add_interrupt(self, interrupt_type, data=None):
        self.interrupt_handler.add_interrupt(interrupt_type, data)

    def handle_interrupt(self, interrupt):
        if interrupt.type == InterruptType.USER_INPUT:
            print(f"Handling user input: {interrupt.data}")
            self.add_process(
                "You are a helpful assistant responding to user input.",
                interrupt.data,
                ProcessType.USER
            )
        elif interrupt.type == InterruptType.TIMER:
            print("Handling timer interrupt")
            self.add_process(
                "You are a system maintenance bot.",
                "Perform routine system check.",
                ProcessType.HOUSEKEEPING
            )
        elif interrupt.type == InterruptType.SYSTEM:
            print(f"Handling system interrupt: {interrupt.data}")
            self.add_process(
                "You are a system management bot.",
                f"Address the following system event: {interrupt.data}",
                ProcessType.SYSTEM
            )

    def execute_process(self):
        if self.current_process:
            print(f"Executing process of type: {self.current_process.process_type}")
            print(f"Token allowance: {self.current_process.token_allowance}")
            
            response = generate_response(
                system=self.current_process.system_prompt,
                user_message=self.current_process.user_prompt,
                max_tokens=self.current_process.token_allowance
            )
            
            print(f"Response: {response}")
            self.current_process.mark_completed()

    

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Kernel listening on {self.host}:{self.port}")

        while self.running:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while self.running:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                command = json.loads(data)
                response = self.process_command(command)
                if response:
                    client_socket.sendall(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                print("Invalid JSON received")
            except Exception as e:
                print(f"Error handling client: {e}")
        client_socket.close()

    def process_command(self, command):
        action = command.get('action')
        if action == 'add_process':
            return self.execute_process_immediately(
                command['system_prompt'],
                command['user_prompt'],
                ProcessType[command['process_type']]
            )
        elif action == 'add_interrupt':
            self.add_interrupt(
                InterruptType[command['interrupt_type']],
                command.get('data')
            )
            return {"status": "Interrupt added"}
        else:
            return {"error": f"Unknown action: {action}"}

    def execute_process_immediately(self, system_prompt, user_prompt, process_type):
        print(f"Executing process of type: {process_type}")
        response = generate_response(
            system=system_prompt,
            user_message=user_prompt,
            max_tokens=self.get_token_allowance(process_type)
        )
        print(f"Response: {response}")
        return {"response": response}

    def get_token_allowance(self, process_type):
        # This method should return the token allowance based on the process type
        allowances = {
            ProcessType.HOUSEKEEPING: 500,
            ProcessType.LLM_INITIATED: 1000,
            ProcessType.USER_SUBPROCESS: 2000,
            ProcessType.USER: 4000
        }
        return allowances[process_type]

    def main_loop(self):
        self.running = True
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        while self.running:
            # Handle interrupts
            interrupt = self.interrupt_handler.get_next_interrupt()
            while interrupt:
                self.handle_interrupt(interrupt)
                interrupt = self.interrupt_handler.get_next_interrupt()

            # Process scheduling
            self.scheduler.update_priorities()
            self.current_process = self.scheduler.get_next_process()
            if self.current_process:
                self.execute_process()
            else:
                print("No processes to execute. Idling...")
                time.sleep(1)

if __name__ == "__main__":
    kernel = LLMKernel()
    kernel.main_loop()