"""
Testes para o sistema de cache

Testa funcionalidades do CommitCache.
"""

import pytest
import tempfile
import os
from pathlib import Path
from commit_ai.cache import CommitCache


class TestCommitCache:
    """Classe de testes para CommitCache"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Usar diretório temporário para testes
        self.temp_dir = Path(tempfile.mkdtemp())
        self.cache = CommitCache(cache_dir=self.temp_dir, max_age_hours=1)
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        # Fechar conexão SQLite se existir
        if hasattr(self, 'cache') and hasattr(self.cache, 'conn'):
            try:
                self.cache.conn.close()
            except:
                pass
        # Limpar diretório temporário
        import shutil
        import time
        try:
            # Aguardar um pouco para o SQLite liberar o arquivo
            time.sleep(0.1)
            shutil.rmtree(self.temp_dir)
        except PermissionError:
            # Tentar novamente após mais uma pausa
            time.sleep(0.5)
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass  # Ignora se não conseguir limpar
    
    def test_cache_miss_initial(self):
        """Testa cache miss inicial"""
        result = self.cache.get(
            diff_text="test diff",
            provider="openai",
            model="gpt-4",
            temperature=0.3,
            max_tokens=100
        )
        assert result is None
    
    def test_cache_hit_after_set(self):
        """Testa cache hit após armazenar"""
        diff_text = "test diff content"
        commit_msg = "feat: add test feature"
        
        # Armazenar no cache
        self.cache.set(
            diff_text=diff_text,
            provider="openai", 
            model="gpt-4",
            temperature=0.3,
            max_tokens=100,
            commit_message=commit_msg
        )
        
        # Buscar no cache
        result = self.cache.get(
            diff_text=diff_text,
            provider="openai",
            model="gpt-4", 
            temperature=0.3,
            max_tokens=100
        )
        
        assert result == commit_msg
    
    def test_cache_miss_different_params(self):
        """Testa cache miss com parâmetros diferentes"""
        diff_text = "test diff content"
        commit_msg = "feat: add test feature"
        
        # Armazenar com parâmetros específicos
        self.cache.set(
            diff_text=diff_text,
            provider="openai",
            model="gpt-4", 
            temperature=0.3,
            max_tokens=100,
            commit_message=commit_msg
        )
        
        # Buscar com parâmetros diferentes (temperature)
        result = self.cache.get(
            diff_text=diff_text,
            provider="openai",
            model="gpt-4",
            temperature=0.5,  # Diferente!
            max_tokens=100
        )
        
        assert result is None
    
    def test_cache_stats_empty(self):
        """Testa estatísticas com cache vazio"""
        stats = self.cache.stats()
        
        assert stats['total_entries'] == 0
        assert stats['provider_stats'] == {}
        assert stats['cache_dir'] == str(self.temp_dir)
    
    def test_cache_stats_with_data(self):
        """Testa estatísticas com dados"""
        # Adicionar algumas entradas
        self.cache.set("diff1", "openai", "gpt-4", 0.3, 100, "commit1")
        self.cache.set("diff2", "gemini", "gemini-pro", 0.3, 100, "commit2")
        self.cache.set("diff3", "openai", "gpt-3.5", 0.5, 50, "commit3")
        
        stats = self.cache.stats()
        
        assert stats['total_entries'] == 3
        assert stats['provider_stats']['openai'] == 2
        assert stats['provider_stats']['gemini'] == 1
    
    def test_clear_all(self):
        """Testa limpeza completa do cache"""
        # Adicionar entrada
        self.cache.set("diff", "openai", "gpt-4", 0.3, 100, "commit")
        
        # Verificar que existe
        assert self.cache.stats()['total_entries'] == 1
        
        # Limpar tudo
        self.cache.clear_all()
        
        # Verificar que foi limpo
        assert self.cache.stats()['total_entries'] == 0
    
    def test_hash_consistency(self):
        """Testa que o mesmo input gera o mesmo hash"""
        diff_text = "same diff content"
        
        # Primeira armazenagem
        self.cache.set(diff_text, "openai", "gpt-4", 0.3, 100, "first commit")
        
        # Segunda armazenagem com mesmo input (deve substituir)
        self.cache.set(diff_text, "openai", "gpt-4", 0.3, 100, "second commit")
        
        # Deve ter apenas uma entrada
        assert self.cache.stats()['total_entries'] == 1
        
        # Deve retornar a segunda mensagem
        result = self.cache.get(diff_text, "openai", "gpt-4", 0.3, 100)
        assert result == "second commit"


if __name__ == '__main__':
    pytest.main([__file__])
