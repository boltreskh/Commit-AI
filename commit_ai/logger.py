"""
Sistema de logging para o Commit-AI

Fornece logging estruturado e configurável.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


class CommitAILogger:
    """Logger personalizado para o Commit-AI"""
    
    def __init__(self, name: str = 'commit-ai', level: str = 'INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Evita duplicação de handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configura os handlers de logging"""
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formato para console (mais limpo)
        console_format = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_format)
        
        # Handler para arquivo (opcional)
        log_dir = Path.home() / '.commit-ai' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / 'commit-ai.log',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Formato detalhado para arquivo
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        
        # Adiciona handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error"""
        self.logger.error(message, **kwargs)
    
    def set_level(self, level: str):
        """Define o nível de logging"""
        self.logger.setLevel(getattr(logging, level.upper()))


# Instância global do logger
logger = CommitAILogger()
