from kernel import LLMKernel
from process import ProcessType
from interrupt import InterruptType

def main():
    kernel = LLMKernel()
    
    # Add initial processes
    kernel.add_process(
        "You are a helpful assistant.",
        "Calculate the fibonacci sequence up to 10 terms",
        ProcessType.USER
    )
    
    kernel.add_process(
        "You are a system maintenance bot.",
        "Update system logs with the current timestamp",
        ProcessType.HOUSEKEEPING
    )
    
    # Simulate interrupts
    kernel.add_interrupt(InterruptType.USER_INPUT, "What's the weather like today?")
    kernel.add_interrupt(InterruptType.TIMER)
    kernel.add_interrupt(InterruptType.SYSTEM, "Low disk space warning")
    
    # Start the main loop
    kernel.main_loop()

if __name__ == "__main__":
    main()