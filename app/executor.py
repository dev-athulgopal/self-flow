from typing import Any
import time
from .logger import setup_logger


logger = setup_logger(__name__)


def execute_tool_use_actions(message: Any) -> None:
    try:
        import pyautogui  # type: ignore
        pyautogui.FAILSAFE = True
    except Exception:
        logger.warning("pyautogui not available; cannot move mouse.")
        return

    content_blocks = getattr(message, "content", []) or []
    for block in content_blocks:
        if getattr(block, "type", None) == "tool_use" and getattr(block, "name", None) == "computer":
            tool_input = getattr(block, "input", {}) or {}
            action = tool_input.get("action")
            if action == "left_click":
                coordinate = tool_input.get("coordinate", [])
                if isinstance(coordinate, list) and len(coordinate) == 2:
                    x, y = coordinate
                    try:
                        time.sleep(0.2)
                        pyautogui.moveTo(int(x), int(y), duration=0.25)
                        logger.info(f"Moved mouse to (%s, %s)", int(x), int(y))
                    except Exception as e:
                        logger.error("Failed to move mouse: %s", e)


