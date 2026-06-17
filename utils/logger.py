"""
Logging configuration and utilities
"""

import os
import logging
import logging.handlers
from config.settings import get_config

config = get_config()


def setup_logging(log_file=None, log_level=None):
    """
    Setup logging configuration
    
    Args:
        log_file (str): Path to log file
        log_level (str): Logging level
    """
    if log_file is None:
        log_file = config.LOG_FILE
    if log_level is None:
        log_level = config.LOG_LEVEL
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    
    # Formatter
    formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def get_logger(name):
    """
    Get a configured logger instance
    
    Args:
        name (str): Logger name (typically __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        formatter = logging.Formatter(
            config.LOG_FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# Initialize logging on module import
setup_logging()
