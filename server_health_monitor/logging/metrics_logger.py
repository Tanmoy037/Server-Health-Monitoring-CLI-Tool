import logging
import json
from logging.handlers import RotatingFileHandler
from typing import Dict, Any
from pathlib import Path

class MetricsLogger:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with rotating file handler."""
        logger = logging.getLogger('server_metrics')
        logger.setLevel(self.config['logging']['level'])
        
        # Create logs directory if it doesn't exist
        log_file = Path(self.config['logging']['file'])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Add rotating file handler
        handler = RotatingFileHandler(
            log_file,
            maxBytes=self.config['logging']['max_size'],
            backupCount=self.config['logging']['backup_count']
        )
        
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def log_metrics(self, metrics: Dict[str, Any]) -> None:
        """Log metrics in JSON format."""
        try:
            self.logger.info(json.dumps(metrics))
        except Exception as e:
            self.logger.error(f"Failed to log metrics: {str(e)}")
    
    def log_alert(self, message: str, level: str = 'WARNING') -> None:
        """Log an alert message."""
        try:
            if level == 'CRITICAL':
                self.logger.critical(message)
            elif level == 'WARNING':
                self.logger.warning(message)
            else:
                self.logger.info(message)
        except Exception as e:
            self.logger.error(f"Failed to log alert: {str(e)}") 