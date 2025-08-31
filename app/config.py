import os
from dataclasses import dataclass
from dotenv import load_dotenv
from .logger import setup_logger

logger = setup_logger(__name__)

# Minimal system prompt for debugging
DEFAULT_SYSTEM_PROMPT = """You are a desktop automation assistant that can control a computer using specific actions.

IMPORTANT: You already have a screenshot of the current screen. DO NOT request or use screenshot actions.

AVAILABLE ACTIONS:
- left_click: Click at coordinates. Use: {"action": "left_click", "coordinate": [x, y]}
- right_click: Right-click at coordinates. Use: {"action": "right_click", "coordinate": [x, y]}
- double_click: Double-click at coordinates. Use: {"action": "double_click", "coordinate": [x, y]}
- move: Move cursor without clicking. Use: {"action": "move", "coordinate": [x, y]}
- type: Type text. Use: {"action": "type", "text": "your text"}
- key: Press a single key. Use: {"action": "key", "key": "enter"}
- key_combination: Press multiple keys. Use: {"action": "key_combination", "keys": ["cmd", "c"]}
- scroll: Scroll up/down. Use: {"action": "scroll", "direction": "down", "amount": 3}
- drag: Drag from start to end. Use: {"action": "drag", "start_coordinate": [x1, y1], "end_coordinate": [x2, y2]}
- wait: Wait for duration. Use: {"action": "wait", "duration": 1.0}

INSTRUCTIONS:
1. Analyze the current screenshot you already have to understand what the user wants
2. Execute the action needed to complete the instruction
3. Use precise coordinates - aim for the center of interactive elements
4. Provide coordinates as [x, y] arrays with integer values
5. NEVER use screenshot action - you already have the current screen state"""


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    max_tokens: int = 1024


def load_settings() -> Settings:
    """Load application settings from environment variables."""
    logger.info("Loading application settings")
    
    # Load environment variables
    logger.debug("Loading environment variables from .env file")
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        error_msg = "ANTHROPIC_API_KEY is not set in environment"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    logger.info("ANTHROPIC_API_KEY loaded successfully")
    logger.debug("API key length: %s characters", len(api_key))
    
    # Create settings object
    settings = Settings(
        anthropic_api_key=api_key,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        max_tokens=1024
    )
    
    logger.info("Settings loaded successfully")
    logger.info("Max tokens: %s", settings.max_tokens)
    logger.debug("System prompt length: %s characters", len(settings.system_prompt))
    
    return settings


