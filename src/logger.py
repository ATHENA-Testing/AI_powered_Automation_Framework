"""
Logging Configuration for Python Automation Framework
Provides centralized logging setup and utilities
"""

import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from loguru import logger
import sys

class FrameworkLogger:
    """Centralized logging configuration for the automation framework"""
    
    def __init__(self, log_level: str = "INFO", log_file: Optional[str] = None):
        """
        Initialize the logger
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file. If None, uses default path.
        """
        self.log_level = log_level.upper()
        
        if log_file is None:
            # Default to logs directory in project root
            project_root = Path(__file__).parent.parent
            logs_dir = project_root / "logs"
            logs_dir.mkdir(exist_ok=True)
            
            # Create timestamped log file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = logs_dir / f"framework_{timestamp}.log"
        
        self.log_file = Path(log_file)
        self.setup_logging()
    
    def setup_logging(self) -> None:
        """Configure logging with both file and console output"""
        # Remove default loguru handler
        logger.remove()
        
        # Add console handler with colors
        logger.add(
            sys.stdout,
            level=self.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True
        )
        
        # Add file handler
        logger.add(
            str(self.log_file),
            level=self.log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="10 MB",
            retention="30 days",
            compression="zip"
        )
        
        # Configure standard logging to use loguru
        class InterceptHandler(logging.Handler):
            def emit(self, record):
                # Get corresponding Loguru level if it exists
                try:
                    level = logger.level(record.levelname).name
                except ValueError:
                    level = record.levelno

                # Find caller from where originated the logged message
                frame, depth = logging.currentframe(), 2
                while frame.f_code.co_filename == logging.__file__:
                    frame = frame.f_back
                    depth += 1

                logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
        
        # Replace standard logging
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
        
        logger.info(f"Logging initialized - Level: {self.log_level}, File: {self.log_file}")
    
    def get_logger(self, name: str = None):
        """
        Get a logger instance
        
        Args:
            name: Logger name. If None, returns the main logger.
            
        Returns:
            Logger instance
        """
        if name:
            return logger.bind(name=name)
        return logger

class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self):
        """Get logger for this class"""
        return logger.bind(name=self.__class__.__name__)

# Global logger instance
framework_logger = FrameworkLogger()
log = framework_logger.get_logger("Framework")

