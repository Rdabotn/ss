import logging
import sys
from datetime import datetime
from typing import Dict, Any
import colorlog

class ColoredFormatter(logging.Formatter):
    """Custom colored formatter for better log visibility"""
    
    COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green', 
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
    
    def format(self, record):
        # Add timestamp
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return super().format(record)

class MusicBotLogger:
    """Enhanced logger for Music Bot"""
    
    def __init__(self, name: str = "MusicBot"):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logger with colored output"""
        self.logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Colored formatter
        colored_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow', 
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        console_handler.setFormatter(colored_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        try:
            file_handler = logging.FileHandler('musicbot.log', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            file_formatter = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            self.logger.warning(f"Could not setup file logging: {e}")
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message"""
        self.logger.info(message, extra=extra or {})
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message"""
        self.logger.warning(message, extra=extra or {})
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log error message"""
        self.logger.error(message, extra=extra or {})
    
    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log debug message"""
        self.logger.debug(message, extra=extra or {})
    
    def critical(self, message: str, extra: Dict[str, Any] = None):
        """Log critical message"""
        self.logger.critical(message, extra=extra or {})
    
    def success(self, message: str):
        """Log success message (as info with emoji)"""
        self.info(f"✅ {message}")
    
    def failure(self, message: str):
        """Log failure message (as error with emoji)"""
        self.error(f"❌ {message}")
    
    def startup_info(self, message: str):
        """Log startup information"""
        self.info(f"🚀 {message}")
    
    def shutdown_info(self, message: str):
        """Log shutdown information"""
        self.info(f"🔄 {message}")

# Create main logger instance
LOGS = MusicBotLogger("MusicBot")

# Additional loggers for different components
bot_logs = MusicBotLogger("Bot")
user_logs = MusicBotLogger("UserBot")
calls_logs = MusicBotLogger("PyTgCalls")

# Suppress some noisy loggers
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

# Welcome message
LOGS.info("=" * 50)
LOGS.info("🎵 Music Bot Logger Initialized")
LOGS.info("=" * 50)

# Export everything
__all__ = [
    'LOGS', 
    'bot_logs', 
    'user_logs', 
    'calls_logs',
    'MusicBotLogger'
]
