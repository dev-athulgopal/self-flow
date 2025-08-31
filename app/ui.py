"""User interface for Self Flow."""
from .logger import setup_logger

logger = setup_logger(__name__)


def get_user_instruction() -> str:
    """Get instruction text from user input."""
    logger.info("Getting user instruction")
    
    print("\n" + "="*50)
    print("SELF FLOW - Desktop Automation")
    print("="*50)
    print("Enter an instruction for what you want to do:")
    print("Examples: 'click on chrome', 'type hello', 'press enter'")
    print("Type 'quit' to exit the program")
    print("="*50)
    
    instruction = input("\nInstruction: ").strip()
    logger.debug("Raw user input: '%s'", instruction)
    
    if not instruction:
        logger.warning("No instruction provided by user")
        print("No instruction provided. Please try again or type 'quit' to exit.")
        return ""
    
    logger.info("User instruction received: '%s' (Length: %s characters)", instruction, len(instruction))
    return instruction


def should_quit(instruction: str) -> bool:
    """Check if the user wants to quit the program."""
    return instruction.lower() in ['quit', 'exit', 'q']


def display_loop_header() -> None:
    """Display the loop header for continuous operation."""
    print("\n" + "="*50)
    print("SELF FLOW - Desktop Automation (Loop Mode)")
    print("="*50)
    print("Enter instructions one by one. Type 'quit' to exit.")
    print("="*50)
