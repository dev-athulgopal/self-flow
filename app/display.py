from typing import Tuple
from .logger import setup_logger

logger = setup_logger(__name__)


def get_primary_display_size() -> Tuple[int, int]:
    """Get the primary display dimensions."""
    logger.info("Detecting primary display size")
    
    try:
        import pyautogui
        w, h = pyautogui.size()
        width, height = int(w), int(h)
        logger.info("Primary display size detected: %sx%s", width, height)
        return width, height
    except ImportError:
        logger.warning("PyAutoGUI not available, using fallback display size")
        fallback_size = (1024, 768)
        logger.info("Using fallback display size: %sx%s", *fallback_size)
        return fallback_size
    except Exception as e:
        logger.error("Failed to detect display size: %s", e)
        fallback_size = (1024, 768)
        logger.info("Using fallback display size: %sx%s", *fallback_size)
        return fallback_size


def take_screenshot() -> str:
    """Take a screenshot of the current screen and save it as screenshot.png in the project root."""
    logger.info("Taking screenshot of current screen")
    
    try:
        import pyautogui
        
        # Save screenshot as screenshot.png in the current working directory
        screenshot_path = "screenshot.png"
        logger.debug("Screenshot will be saved to: %s", screenshot_path)
        
        # Take screenshot
        logger.debug("Capturing screenshot using PyAutoGUI")
        screenshot = pyautogui.screenshot()
        
        # Save the screenshot
        logger.debug("Saving screenshot to disk")
        screenshot.save(screenshot_path)
        
        # Get file size for logging
        import os
        file_size = os.path.getsize(screenshot_path)
        logger.info("Screenshot saved successfully: %s (Size: %s bytes)", screenshot_path, file_size)
        
        return screenshot_path
        
    except ImportError:
        error_msg = "PyAutoGUI not available for screenshot capture"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    except Exception as e:
        error_msg = f"Failed to take screenshot: {e}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


