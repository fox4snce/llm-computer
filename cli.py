import socket
import json
import sys
import shlex

class KernelCLI:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.default_system_prompt = "You are a helpful assistant."

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to kernel at {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("Could not connect to the kernel. Is it running?")
            sys.exit(1)

    def send_command(self, command):
        self.socket.sendall(json.dumps(command).encode('utf-8'))

    def send_command_and_get_response(self, command):
        self.socket.sendall(json.dumps(command).encode('utf-8'))
        response = self.socket.recv(4096).decode('utf-8')
        return json.loads(response)

    def parse_query_command(self, command_string):
        parts = shlex.split(command_string)
        system_prompt = self.default_system_prompt
        user_prompt = None

        for part in parts[1:]:  # Skip the 'query' part
            if part.startswith("system="):
                system_prompt = part[7:].strip('"')
            elif part.startswith("user="):
                user_prompt = part[5:].strip('"')

        if user_prompt is None:
            raise ValueError("User prompt is required")

        return system_prompt, user_prompt

    def run(self):
        self.connect()
        print("LLM Kernel CLI. Type 'exit' to quit.")
        while True:
            try:
                command = input("Enter command: ")
                if command.lower() == 'exit':
                    break
                elif command.lower().startswith('query'):
                    try:
                        system_prompt, user_prompt = self.parse_query_command(command)
                        response = self.send_command_and_get_response({
                            'action': 'add_process',
                            'system_prompt': system_prompt,
                            'user_prompt': user_prompt,
                            'process_type': 'USER'
                        })
                        print("Response from kernel:")
                        print(response.get('response', 'No response received'))
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Unknown command")
            except Exception as e:
                print(f"Error: {e}")
        
        self.socket.close()

if __name__ == "__main__":
    cli = KernelCLI()
    cli.run()