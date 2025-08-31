import logging
import sys
from typing import Optional


def setup_logger(name: str = "self_flow", level: Optional[str] = None) -> logging.Logger:
    """Setup and configure a logger with enhanced formatting.
    
    Args:
        name: Logger name
        level: Logging level (INFO, DEBUG, WARNING, ERROR)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    
    # Set log level from parameter or default to INFO
    log_level = getattr(logging, level.upper()) if level else logging.INFO
    logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    
    # Enhanced formatter with more context
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    return logger


def setup_automation_logger(name: str = "automation", level: str = "INFO") -> logging.Logger:
    """Setup a specialized logger for automation operations with enhanced context."""
    logger = setup_logger(name, level)
    
    # Add automation-specific context
    logger.info("Automation session started")
    
    return logger


def setup_debug_logger(name: str = "debug", level: str = "DEBUG") -> logging.Logger:
    """Setup a debug logger with maximum verbosity for troubleshooting."""
    logger = setup_logger(name, level)
    
    # Add debug-specific context
    logger.debug("Debug logging enabled with maximum verbosity")
    
    return logger


def get_log_level_from_env() -> str:
    """Get log level from environment variable LOG_LEVEL."""
    import os
    return os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logger_with_env(name: str = "self_flow") -> logging.Logger:
    """Setup logger with level from environment variable."""
    level = get_log_level_from_env()
    return setup_logger(name, level)


