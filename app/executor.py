"""Executor for computer automation actions."""

from typing import Any, Dict, List, Optional, Tuple
import time
from .logger import setup_logger

logger = setup_logger(__name__)


def validate_coordinate(coord: Any, display_size: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    """Validate and return coordinate tuple if valid."""
    logger.debug("Validating coordinate: %s (Type: %s)", coord, type(coord).__name__)
    
    if isinstance(coord, list) and len(coord) == 2:
        try:
            x, y = int(coord[0]), int(coord[1])
            width, height = display_size
            
            logger.debug("Parsed coordinates: (%s, %s)", x, y)
            logger.debug("Display bounds: %sx%s", width, height)
            
            if 0 <= x < width and 0 <= y < height:
                logger.debug("Coordinates (%s, %s) are valid", x, y)
                return (x, y)
            else:
                logger.warning("Coordinates (%s, %s) out of bounds (%sx%s)", x, y, width, height)
                if x < 0 or x >= width:
                    logger.debug("X coordinate %s is outside valid range [0, %s)", x, width)
                if y < 0 or y >= height:
                    logger.debug("Y coordinate %s is outside valid range [0, %s)", y, height)
                return None
        except (ValueError, TypeError) as e:
            logger.warning("Invalid coordinate format: %s", e)
            return None
    else:
        logger.warning("Invalid coordinate format: expected list with 2 elements, got %s", coord)
        return None


def validate_action_parameters(action: str, tool_input: Dict[str, Any], display_size: Tuple[int, int]) -> bool:
    """Validate action parameters before execution."""
    logger.debug("Validating action parameters for: %s", action)
    logger.debug("Tool input: %s", tool_input)
    
    if action in ["left_click", "right_click", "double_click", "move"]:
        coord = validate_coordinate(tool_input.get("coordinate"), display_size)
        if not coord:
            logger.error("Action validation failed for %s: Invalid coordinates", action)
            return False
    
    elif action == "drag":
        start_coord = validate_coordinate(tool_input.get("start_coordinate"), display_size)
        end_coord = validate_coordinate(tool_input.get("end_coordinate"), display_size)
        if not start_coord or not end_coord:
            logger.error("Action validation failed for %s: Invalid coordinates", action)
            return False
    
    elif action == "type":
        if not tool_input.get("text"):
            logger.error("No text provided for type action")
            return False
    
    logger.debug("Action validation passed for: %s", action)
    return True


def handle_left_click(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle left click action."""
    logger.info("Executing left_click action")
    coordinate = validate_coordinate(tool_input.get("coordinate"), display_size)
    if not coordinate:
        logger.error("Invalid coordinate for left_click: %s", tool_input.get("coordinate"))
        return False
    
    x, y = coordinate
    logger.debug("Left clicking at coordinates (%s, %s)", x, y)
    
    try:
        logger.debug("Waiting 0.2 seconds before click")
        time.sleep(0.2)
        
        logger.debug("Executing pyautogui.click(%s, %s)", x, y)
        pyautogui.click(x, y)
        
        logger.info("Left clicked successfully at (%s, %s)", x, y)
        return True
    except Exception as e:
        logger.error("Failed to left click at (%s, %s): %s", x, y, e)
        return False


def handle_right_click(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle right click action."""
    logger.info("Executing right_click action")
    coordinate = validate_coordinate(tool_input.get("coordinate"), display_size)
    if not coordinate:
        logger.error("Invalid coordinate for right_click: %s", tool_input.get("coordinate"))
        return False
    
    x, y = coordinate
    logger.debug("Right clicking at coordinates (%s, %s)", x, y)
    
    try:
        logger.debug("Waiting 0.2 seconds before right-click")
        time.sleep(0.2)
        
        logger.debug("Executing pyautogui.rightClick(%s, %s)", x, y)
        pyautogui.rightClick(x, y)
        
        logger.info("Right clicked successfully at (%s, %s)", x, y)
        return True
    except Exception as e:
        logger.error("Failed to right click at (%s, %s): %s", x, y, e)
        return False


def handle_double_click(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle double click action."""
    logger.info("Executing double_click action")
    coordinate = validate_coordinate(tool_input.get("coordinate"), display_size)
    if not coordinate:
        logger.error("Invalid coordinate for double_click: %s", tool_input.get("coordinate"))
        return False
    
    x, y = coordinate
    logger.debug("Double clicking at coordinates (%s, %s)", x, y)
    
    try:
        logger.debug("Waiting 0.2 seconds before double-click")
        time.sleep(0.2)
        
        logger.debug("Executing pyautogui.doubleClick(%s, %s)", x, y)
        pyautogui.doubleClick(x, y)
        
        logger.info("Double clicked successfully at (%s, %s)", x, y)
        return True
    except Exception as e:
        logger.error("Failed to double click at (%s, %s): %s", x, y, e)
        return False


def handle_type(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle type action."""
    logger.info("Executing type action")
    text = tool_input.get("text", "")
    if not text:
        logger.error("No text provided for type action")
        return False
    
    logger.debug("Text to type: '%s' (Length: %s characters)", text, len(text))
    
    coordinate = tool_input.get("coordinate")
    if coordinate:
        logger.debug("Coordinate provided for typing: %s", coordinate)
        coord = validate_coordinate(coordinate, display_size)
        if coord:
            x, y = coord
            logger.debug("Clicking at (%s, %s) before typing", x, y)
            pyautogui.click(x, y)
            time.sleep(0.1)
        else:
            logger.warning("Invalid coordinate provided for typing, proceeding without clicking")
    else:
        logger.debug("No coordinate provided, typing at current cursor position")
    
    try:
        logger.debug("Executing pyautogui.typewrite('%s')", text)
        pyautogui.typewrite(text)
        
        logger.info("Text typed successfully: '%s'", text)
        return True
    except Exception as e:
        logger.error("Failed to type text '%s': %s", text, e)
        return False


def handle_key(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle single key press action."""
    logger.info("Executing key press action")
    key = tool_input.get("key", "")
    if not key:
        logger.error("No key provided for key action")
        return False
    
    logger.debug("Key to press: '%s'", key)
    
    try:
        logger.debug("Executing pyautogui.press('%s')", key)
        pyautogui.press(key)
        
        logger.info("Key pressed successfully: '%s'", key)
        return True
    except Exception as e:
        logger.error("Failed to press key '%s': %s", key, e)
        return False


def handle_key_combination(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle key combination action."""
    logger.info("Executing key combination action")
    keys = tool_input.get("keys", [])
    if not keys or not isinstance(keys, list):
        logger.error("Invalid keys for key_combination: %s", keys)
        return False
    
    logger.debug("Keys to press: %s", keys)
    
    try:
        key_str = '+'.join(keys)
        logger.debug("Executing pyautogui.hotkey(%s)", keys)
        pyautogui.hotkey(*keys)
        
        logger.info("Key combination pressed successfully: %s", key_str)
        return True
    except Exception as e:
        logger.error("Failed to press key combination %s: %s", keys, e)
        return False


def handle_scroll(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle scroll action."""
    logger.info("Executing scroll action")
    coordinate = tool_input.get("coordinate")
    direction = tool_input.get("direction", "down")
    amount = tool_input.get("amount", 3)
    
    logger.debug("Scroll direction: %s, amount: %s", direction, amount)
    
    if coordinate:
        logger.debug("Coordinate provided for scrolling: %s", coordinate)
        coord = validate_coordinate(coordinate, display_size)
        if coord:
            x, y = coord
            logger.debug("Moving to (%s, %s) before scrolling", x, y)
            pyautogui.moveTo(x, y)
            time.sleep(0.1)
        else:
            logger.warning("Invalid coordinate provided for scrolling, proceeding at current position")
    else:
        logger.debug("No coordinate provided, scrolling at current cursor position")
    
    try:
        if direction.lower() == "up":
            logger.debug("Executing pyautogui.scroll(%s)", amount)
            pyautogui.scroll(amount)
        else:
            logger.debug("Executing pyautogui.scroll(-%s)", amount)
            pyautogui.scroll(-amount)
        
        logger.info("Scrolled %s %s units successfully", direction, amount)
        return True
    except Exception as e:
        logger.error("Failed to scroll %s %s units: %s", direction, amount, e)
        return False


def handle_move(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle move action."""
    logger.info("Executing move action")
    coordinate = validate_coordinate(tool_input.get("coordinate"), display_size)
    if not coordinate:
        logger.error("Invalid coordinate for move: %s", tool_input.get("coordinate"))
        return False
    
    x, y = coordinate
    logger.debug("Moving cursor to coordinates (%s, %s)", x, y)
    
    try:
        logger.debug("Executing pyautogui.moveTo(%s, %s, duration=0.25)", x, y)
        pyautogui.moveTo(x, y, duration=0.25)
        
        logger.info("Cursor moved successfully to (%s, %s)", x, y)
        return True
    except Exception as e:
        logger.error("Failed to move cursor to (%s, %s): %s", x, y, e)
        return False


def handle_drag(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle drag action."""
    logger.info("Executing drag action")
    start_coord = validate_coordinate(tool_input.get("start_coordinate"), display_size)
    end_coord = validate_coordinate(tool_input.get("end_coordinate"), display_size)
    
    if not start_coord or not end_coord:
        logger.error("Invalid coordinates for drag: start=%s, end=%s", 
                    tool_input.get("start_coordinate"), tool_input.get("end_coordinate"))
        return False
    
    start_x, start_y = start_coord
    end_x, end_y = end_coord
    
    logger.debug("Dragging from (%s, %s) to (%s, %s)", start_x, start_y, end_x, end_y)
    
    try:
        logger.debug("Moving to start position (%s, %s)", start_x, start_y)
        pyautogui.moveTo(start_x, start_y)
        time.sleep(0.1)
        
        delta_x = end_x - start_x
        delta_y = end_y - start_y
        logger.debug("Executing pyautogui.drag(%s, %s, duration=0.5)", delta_x, delta_y)
        pyautogui.drag(delta_x, delta_y, duration=0.5)
        
        logger.info("Drag executed successfully from (%s, %s) to (%s, %s)", start_x, start_y, end_x, end_y)
        return True
    except Exception as e:
        logger.error("Failed to drag from (%s, %s) to (%s, %s): %s", 
                    start_x, start_y, end_x, end_y, e)
        return False


def handle_wait(tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int]) -> bool:
    """Handle wait action."""
    logger.info("Executing wait action")
    duration = tool_input.get("duration", 1.0)
    
    logger.debug("Duration to wait: %s seconds", duration)
    
    try:
        duration = float(duration)
        logger.debug("Waiting for %s seconds", duration)
        time.sleep(duration)
        
        logger.info("Wait completed successfully: %s seconds", duration)
        return True
    except (ValueError, TypeError):
        logger.error("Invalid duration for wait: %s", tool_input.get("duration"))
        return False
    except Exception as e:
        logger.error("Failed to wait for %s seconds: %s", duration, e)
        return False


# Action handler mapping
ACTION_HANDLERS = {
    "left_click": handle_left_click,
    "right_click": handle_right_click,
    "double_click": handle_double_click,
    "type": handle_type,
    "key": handle_key,
    "key_combination": handle_key_combination,
    "scroll": handle_scroll,
    "move": handle_move,
    "drag": handle_drag,
    "wait": handle_wait,
}


def execute_action_with_retry(action: str, tool_input: Dict[str, Any], pyautogui, display_size: Tuple[int, int], max_retries: int = 2) -> bool:
    """Execute an action with retry logic."""
    logger.debug("Executing action '%s' with max retries: %s", action, max_retries)
    
    for attempt in range(max_retries + 1):
        try:
            if ACTION_HANDLERS[action](tool_input, pyautogui, display_size):
                return True
            elif attempt < max_retries:
                logger.warning("Action %s failed, retrying... (attempt %s/%s)", action, attempt + 1, max_retries)
                time.sleep(0.5)
        except Exception as e:
            if attempt < max_retries:
                logger.warning("Exception during %s, retrying... (attempt %s/%s): %s", action, attempt + 1, max_retries, e)
                time.sleep(0.5)
            else:
                logger.error("Action %s failed after %s attempts: %s", action, max_retries + 1, e)
                return False
    
    return False


def execute_tool_use_actions(message: Any, display_size: Tuple[int, int], max_retries: int = 2) -> int:
    """Execute computer-use tool actions."""
    logger.info("Starting execution of tool use actions")
    logger.debug("Display size: %sx%s", *display_size)
    logger.debug("Max retries per action: %s", max_retries)
    
    try:
        import pyautogui
        pyautogui.FAILSAFE = True
        logger.info("PyAutoGUI loaded successfully")
        logger.debug("PyAutoGUI version: %s", pyautogui.__version__)
        logger.debug("Failsafe enabled: %s", pyautogui.FAILSAFE)
    except Exception as e:
        logger.warning("pyautogui not available; cannot execute actions: %s", e)
        return 0

    content_blocks = getattr(message, "content", []) or []
    tool_use_blocks = []
    
    # Collect all tool_use blocks
    for block in content_blocks:
        if getattr(block, "type", None) == "tool_use" and getattr(block, "name", None) == "computer":
            tool_use_blocks.append(block)
    
    if not tool_use_blocks:
        logger.info("No computer actions found in the response")
        return 0
    
    logger.info("Found %s action(s) to execute", len(tool_use_blocks))
    
    # Log all actions for debugging
    for i, block in enumerate(tool_use_blocks):
        tool_input = getattr(block, "input", {}) or {}
        action = tool_input.get("action", "unknown")
        logger.debug("Action %s: %s with params: %s", i+1, action, tool_input)
    
    executed_actions = 0
    successful_actions = 0
    
    for i, block in enumerate(tool_use_blocks, 1):
        tool_input = getattr(block, "input", {}) or {}
        action = tool_input.get("action")
        
        logger.info("Processing action %s/%s: %s", i, len(tool_use_blocks), action)
        
        if action not in ACTION_HANDLERS:
            logger.warning("Unknown action type: %s", action)
            continue
        
        # Reject screenshot actions
        if action == "screenshot":
            logger.warning("Screenshot action requested but not needed")
            continue
        
        # Validate action parameters before execution
        if not validate_action_parameters(action, tool_input, display_size):
            logger.error("Action validation failed for %s", action)
            continue
        
        # Execute the action
        executed_actions += 1
        logger.info("Executing action: %s with params: %s", action, tool_input)
        
        try:
            if execute_action_with_retry(action, tool_input, pyautogui, display_size, max_retries):
                successful_actions += 1
                logger.info("Action '%s' completed successfully", action)
            else:
                logger.warning("Action '%s' failed", action)
        except Exception as e:
            logger.error("Exception during action %s: %s", action, e)
    
    logger.info("Action execution complete: %s/%s successful (%.1f%%)", 
                successful_actions, executed_actions, 
                (successful_actions/executed_actions*100) if executed_actions > 0 else 0)
    
    return successful_actions
