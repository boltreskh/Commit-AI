"""
Sistema de Cache para o Commit-AI

Cache inteligente que armazena respostas da IA baseado no hash do diff.
Economiza chamadas da API e acelera o processo.
"""

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from .logger import logger


class CommitCache:
    """Sistema de cache para respostas da IA"""
    
    def __init__(self, cache_dir: Optional[Path] = None, max_age_hours: int = 24):
        """
        Inicializa o sistema de cache
        
        Args:
            cache_dir: Diretório para o cache (padrão: ~/.commit-ai/cache)
            max_age_hours: Idade máxima do cache em horas (padrão: 24h)
        """
        self.cache_dir = cache_dir or (Path.home() / '.commit-ai' / 'cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.cache_dir / 'cache.db'
        self.max_age = timedelta(hours=max_age_hours)
        
        logger.debug(f"Inicializando cache em: {self.db_path}")
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS commit_cache (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        diff_hash TEXT UNIQUE NOT NULL,
                        provider TEXT NOT NULL,
                        model TEXT NOT NULL,
                        temperature REAL NOT NULL,
                        max_tokens INTEGER NOT NULL,
                        commit_message TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Índice para busca rápida
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_diff_hash 
                    ON commit_cache(diff_hash)
                ''')
                
                conn.commit()
                logger.debug("Banco de dados de cache inicializado")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de cache: {e}")
    
    def _generate_hash(self, diff_text: str, provider: str, model: str, 
                      temperature: float, max_tokens: int) -> str:
        """
        Gera hash único baseado nos parâmetros
        
        Args:
            diff_text: Texto do diff
            provider: Provedor de IA
            model: Modelo usado
            temperature: Parâmetro temperature
            max_tokens: Parâmetro max_tokens
            
        Returns:
            str: Hash SHA-256
        """
        # Combina todos os parâmetros que afetam a resposta
        content = f"{diff_text}|{provider}|{model}|{temperature}|{max_tokens}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def get(self, diff_text: str, provider: str, model: str, 
            temperature: float, max_tokens: int) -> Optional[str]:
        """
        Busca uma resposta no cache
        
        Args:
            diff_text: Texto do diff
            provider: Provedor de IA
            model: Modelo usado
            temperature: Parâmetro temperature
            max_tokens: Parâmetro max_tokens
            
        Returns:
            str: Mensagem de commit em cache ou None se não encontrada
        """
        diff_hash = self._generate_hash(diff_text, provider, model, temperature, max_tokens)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Busca entrada no cache
                cursor.execute('''
                    SELECT commit_message, created_at 
                    FROM commit_cache 
                    WHERE diff_hash = ?
                ''', (diff_hash,))
                
                result = cursor.fetchone()
                
                if result:
                    commit_message, created_at = result
                    
                    # Verifica se o cache ainda é válido
                    created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00').replace('+00:00', ''))
                    if datetime.now() - created_time <= self.max_age:
                        # Atualiza o timestamp de acesso
                        cursor.execute('''
                            UPDATE commit_cache 
                            SET accessed_at = CURRENT_TIMESTAMP 
                            WHERE diff_hash = ?
                        ''', (diff_hash,))
                        conn.commit()
                        
                        logger.info(f"Cache hit para hash: {diff_hash[:12]}...")
                        return commit_message
                    else:
                        # Remove entrada expirada
                        cursor.execute('DELETE FROM commit_cache WHERE diff_hash = ?', (diff_hash,))
                        conn.commit()
                        logger.debug(f"Cache expirado removido: {diff_hash[:12]}...")
                
                logger.debug(f"Cache miss para hash: {diff_hash[:12]}...")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao buscar no cache: {e}")
            return None
    
    def set(self, diff_text: str, provider: str, model: str, 
            temperature: float, max_tokens: int, commit_message: str):
        """
        Armazena uma resposta no cache
        
        Args:
            diff_text: Texto do diff
            provider: Provedor de IA
            model: Modelo usado
            temperature: Parâmetro temperature
            max_tokens: Parâmetro max_tokens
            commit_message: Mensagem de commit para armazenar
        """
        diff_hash = self._generate_hash(diff_text, provider, model, temperature, max_tokens)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insere ou atualiza entrada no cache
                cursor.execute('''
                    INSERT OR REPLACE INTO commit_cache 
                    (diff_hash, provider, model, temperature, max_tokens, commit_message)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (diff_hash, provider, model, temperature, max_tokens, commit_message))
                
                conn.commit()
                logger.debug(f"Cache armazenado para hash: {diff_hash[:12]}...")
                
        except Exception as e:
            logger.error(f"Erro ao armazenar no cache: {e}")
    
    def clear_expired(self):
        """Remove entradas expiradas do cache"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Remove entradas antigas
                cutoff_time = datetime.now() - self.max_age
                cursor.execute('''
                    DELETE FROM commit_cache 
                    WHERE datetime(created_at) < ?
                ''', (cutoff_time.isoformat(),))
                
                removed_count = cursor.rowcount
                conn.commit()
                
                if removed_count > 0:
                    logger.info(f"Removidas {removed_count} entradas expiradas do cache")
                
        except Exception as e:
            logger.error(f"Erro ao limpar cache expirado: {e}")
    
    def clear_all(self):
        """Remove todas as entradas do cache"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM commit_cache')
                removed_count = cursor.rowcount
                conn.commit()
                
                logger.info(f"Cache limpo: {removed_count} entradas removidas")
                
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
    
    def stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total de entradas
                cursor.execute('SELECT COUNT(*) FROM commit_cache')
                total_entries = cursor.fetchone()[0]
                
                # Entradas por provedor
                cursor.execute('''
                    SELECT provider, COUNT(*) 
                    FROM commit_cache 
                    GROUP BY provider
                ''')
                provider_stats = dict(cursor.fetchall())
                
                # Idade da entrada mais antiga
                cursor.execute('''
                    SELECT MIN(created_at) 
                    FROM commit_cache
                ''')
                oldest_entry = cursor.fetchone()[0]
                
                return {
                    'total_entries': total_entries,
                    'provider_stats': provider_stats,
                    'oldest_entry': oldest_entry,
                    'cache_dir': str(self.cache_dir),
                    'max_age_hours': self.max_age.total_seconds() / 3600
                }
                
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas do cache: {e}")
            return {'error': str(e)}
