# LLM-Based Operating System Simulation

## Overview

This project is an experimental exploration of operating system principles applied to Large Language Models (LLMs). It simulates a simple computer system where processes are LLM interactions, managed by a kernel with basic scheduling and interrupt handling capabilities.

**Note:** This is an early-stage, proof-of-concept project and is not intended for production use.

## Key Components

1. **Kernel (kernel.py)**: The core of the system, managing processes and handling interrupts.
2. **CLI (cli.py)**: A command-line interface for interacting with the kernel.
3. **Scheduler (scheduler.py)**: Manages process priorities and execution order.
4. **Process (process.py)**: Defines different types of processes and their properties.
5. **Interrupt Handler (interrupt.py)**: Manages system interrupts.
6. **LLM Utilities (llm_utils.py)**: Interfaces with the LLM for generating responses.

## Features

- Multiple process types (User, System, Housekeeping, etc.)
- Priority-based scheduling
- Interrupt handling (User Input, Timer, System)
- Configurable token allowances for different process types
- CLI for easy interaction with the system

## Getting Started

### Prerequisites

- Python 3.7+
- An LLM server running locally (default: localhost:5001)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/fox4snce/llm-computer.git
   cd llm-os-simulation
   ```

### Running the System

1. Start the kernel:
   ```
   python kernel.py
   ```

2. In a separate terminal, start the CLI:
   ```
   python cli.py
   ```

3. Interact with the system using the CLI. For example:
   ```
   Enter command: query user="What's the weather like today?"
   ```

## Customization

- Modify `llm_utils.py` to use a different LLM or API.
- Adjust process types, priorities, and token allowances in `process.py`.
- Customize interrupt types and handling in `interrupt.py` and `kernel.py`.

## Future Directions

- Implement more complex scheduling algorithms
- Add memory management simulation
- Introduce inter-process communication
- Develop a graphical user interface
- Expand the range of simulated OS features

## Contributing

This project is in its early stages and is primarily for educational and experimental purposes. I'm unlikely to go much further with it, feel free to fork it and play around!

## License

Copyright 2024 fox4snce

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgements

This project draws inspiration from classical operating system design principles and applies them to the emerging field of large language models. It serves as a playground for exploring the intersection of traditional computer science concepts and modern AI capabilities.

This project is based on some ideas from Yohei Nakajima and Andrej Karpathy.
