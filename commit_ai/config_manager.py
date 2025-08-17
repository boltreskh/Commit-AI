"""
Arquivo de configuração para o Commit-AI

Este módulo gerencia configurações persistentes do usuário.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Gerenciador de configurações do Commit-AI"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.commit-ai'
        self.config_file = self.config_dir / 'config.json'
        self.default_config = {
            'default_api': 'openai',
            'default_model': None,
            'temperature': 0.3,
            'max_tokens': 100,
            'auto_commit': False,
            'preview_mode': False,
            'commit_types': [
                'feat', 'fix', 'docs', 'style', 'refactor',
                'test', 'chore', 'perf', 'ci', 'build'
            ],
            'custom_prompt': None
        }
        self._ensure_config_exists()
    
    def _ensure_config_exists(self):
        """Cria o diretório e arquivo de configuração se não existirem"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.save_config(self.default_config)
    
    def load_config(self) -> Dict[str, Any]:
        """Carrega a configuração do arquivo"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            # Mescla com valores padrão para chaves faltantes
            return {**self.default_config, **config}
        except (FileNotFoundError, json.JSONDecodeError):
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any]):
        """Salva a configuração no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um valor da configuração"""
        config = self.load_config()
        return config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Define um valor na configuração"""
        config = self.load_config()
        config[key] = value
        self.save_config(config)
    
    def reset(self):
        """Reseta a configuração para os valores padrão"""
        self.save_config(self.default_config)
