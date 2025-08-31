from typing import Any, Dict, Tuple
import base64
import anthropic
from .logger import setup_logger

logger = setup_logger(__name__)


def build_client(api_key: str) -> anthropic.Anthropic:
    """Build and return an Anthropic client instance."""
    logger.info("Building Anthropic client")
    logger.debug("API key length: %s characters", len(api_key) if api_key else 0)
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        logger.info("Anthropic client built successfully")
        return client
    except Exception as e:
        logger.error("Failed to build Anthropic client: %s", e)
        raise


def encode_image_to_base64(path: str) -> str:
    """Encode an image file to base64 string."""
    logger.info("Encoding image to base64: %s", path)
    
    try:
        with open(path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode("utf-8")
            logger.info("Image encoded successfully. Size: %s bytes, Base64 length: %s characters", 
                       len(data), len(encoded))
            return encoded
    except FileNotFoundError:
        logger.error("Image file not found: %s", path)
        raise
    except Exception as e:
        logger.error("Failed to encode image %s: %s", path, e)
        raise


def create_computer_use_request(
    client: anthropic.Anthropic,
    model: str,
    instruction_text: str,
    image_b64: str,
    media_type: str,
    display_size: Tuple[int, int],
    system_prompt: str,
    max_tokens: int = 1024,
) -> Any:
    """Create a computer-use request to Claude with enhanced configuration.
    
    Args:
        client: Anthropic client instance
        model: Claude model to use
        instruction_text: User's instruction text
        image_b64: Base64 encoded screenshot
        media_type: Image media type (e.g., "image/png")
        display_size: Tuple of (width, height) for display dimensions
        system_prompt: System prompt for Claude
        max_tokens: Maximum tokens for response
        
    Returns:
        Claude's response message
    """
    width, height = display_size
    
    logger.info("Creating computer-use request to Claude")
    logger.info("Model: %s", model)
    logger.info("Instruction length: %s characters", len(instruction_text))
    logger.info("Image base64 length: %s characters", len(image_b64))
    logger.info("Display size: %sx%s", width, height)
    logger.info("Max tokens: %s", max_tokens)
    logger.debug("System prompt length: %s characters", len(system_prompt))
    
    try:
        response = client.beta.messages.create(
            model=model,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instruction_text},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_b64,
                            },
                        },
                    ],
                }
            ],
            tools=[{
                "type": "computer_20250124",
                "name": "computer",
                "display_width_px": width,
                "display_height_px": height,
                "display_number": 0,
            }],
            betas=["computer-use-2025-01-24"],
            max_tokens=max_tokens,
        )
        
        logger.info("Computer-use request sent successfully")
        logger.debug("Response received from Claude")
        
        # Log response details
        if hasattr(response, 'content'):
            content_blocks = getattr(response, 'content', []) or []
            tool_use_blocks = [b for b in content_blocks 
                              if getattr(b, 'type', None) == 'tool_use' 
                              and getattr(b, 'name', None) == 'computer']
            logger.info("Response contains %s computer action blocks", len(tool_use_blocks))
            
            for i, block in enumerate(tool_use_blocks):
                tool_input = getattr(block, 'input', {}) or {}
                action = tool_input.get('action', 'unknown')
                logger.debug("Action %s: %s with params: %s", i+1, action, tool_input)
        
        return response
        
    except Exception as e:
        logger.error("Failed to create computer-use request: %s", e)
        raise


