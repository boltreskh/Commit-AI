"""
Testes para o GitHandler

Testa funcionalidades de integração com Git.
"""

import pytest
import tempfile
import os
import subprocess
from pathlib import Path
from commit_ai.git_handler import GitHandler


class TestGitHandler:
    """Classe de testes para GitHandler"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Cria um diretório temporário para testes
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Inicializa repositório Git
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)
        
        self.git_handler = GitHandler()
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        os.chdir(self.original_cwd)
        # Remove diretório temporário
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_is_git_repo_true(self):
        """Testa detecção de repositório Git válido"""
        assert self.git_handler.is_git_repo() is True
    
    def test_is_git_repo_false(self):
        """Testa detecção quando não é repositório Git"""
        # Remove .git
        import shutil
        shutil.rmtree('.git')
        
        git_handler = GitHandler()
        assert git_handler.is_git_repo() is False
    
    def test_has_staged_changes_false(self):
        """Testa quando não há alterações staged"""
        assert self.git_handler.has_staged_changes() is False
    
    def test_has_staged_changes_true(self):
        """Testa quando há alterações staged"""
        # Cria arquivo e adiciona ao staging
        Path('test_file.txt').write_text('Hello World')
        subprocess.run(['git', 'add', 'test_file.txt'], check=True)
        
        assert self.git_handler.has_staged_changes() is True
    
    def test_get_file_changes(self):
        """Testa obtenção de informações sobre arquivos alterados"""
        # Cria e adiciona arquivo
        Path('new_file.txt').write_text('New content')
        subprocess.run(['git', 'add', 'new_file.txt'], check=True)
        
        changes = self.git_handler.get_file_changes()
        
        assert 'new_file.txt' in changes['Adicionados']
        assert len(changes['Modificados']) == 0
        assert len(changes['Removidos']) == 0
    
    def test_get_staged_diff(self):
        """Testa obtenção do diff staged"""
        # Cria arquivo e adiciona ao staging
        Path('test.py').write_text('print("Hello, World!")')
        subprocess.run(['git', 'add', 'test.py'], check=True)
        
        diff = self.git_handler.get_staged_diff()
        
        assert 'test.py' in diff
        assert 'print("Hello, World!")' in diff
        assert '+' in diff  # Linha adicionada


if __name__ == '__main__':
    pytest.main([__file__])
