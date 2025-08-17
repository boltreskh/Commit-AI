#!/usr/bin/env python3
"""
Testes para o sistema de Git Hooks do Commit-AI
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess

from commit_ai.git_hooks import (
    GitHooksManager, 
    PreCommitHook, 
    CommitMsgHook, 
    PostCommitHook
)


class TestGitHooksManager:
    """Testes para a classe GitHooksManager"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.git_dir = Path(self.temp_dir) / '.git'
        self.hooks_dir = self.git_dir / 'hooks'
        
        # Criar estrutura de diretórios simulando um repo git
        self.git_dir.mkdir()
        self.hooks_dir.mkdir()
        
        # Patch do getcwd para retornar nosso diretório temporário
        self.cwd_patcher = patch('os.getcwd', return_value=self.temp_dir)
        self.cwd_patcher.start()
        
        self.manager = GitHooksManager(repo_path=self.temp_dir)
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        self.cwd_patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init_with_valid_repo(self):
        """Testa inicialização com repositório git válido"""
        assert self.manager.repo_path == Path(self.temp_dir)
        assert self.manager.hooks_dir == self.hooks_dir
    
    @patch('commit_ai.git_hooks.Path.exists')
    def test_init_without_git_repo(self, mock_exists):
        """Testa inicialização sem repositório git"""
        mock_exists.return_value = False
        
        with pytest.raises(Exception, match="Não é um repositório Git"):
            GitHooksManager(repo_path="/invalid/path")
    
    def test_install_hooks_success(self):
        """Testa instalação bem-sucedida de hooks"""
        # Mock dos hooks
        with patch.object(self.manager, '_create_hook_scripts') as mock_create:
            mock_create.return_value = True
            
            result = self.manager.install_hooks()
            
            assert result is True
            mock_create.assert_called_once_with(None)
    
    def test_install_specific_hooks(self):
        """Testa instalação de hooks específicos"""
        hooks_to_install = ['pre-commit', 'commit-msg']
        
        with patch.object(self.manager, '_create_hook_scripts') as mock_create:
            mock_create.return_value = True
            
            result = self.manager.install_hooks(hooks_to_install)
            
            assert result is True
            mock_create.assert_called_once_with(hooks_to_install)
    
    def test_uninstall_hooks(self):
        """Testa remoção de hooks"""
        # Criar alguns arquivos de hook
        pre_commit_file = self.hooks_dir / 'pre-commit'
        commit_msg_file = self.hooks_dir / 'commit-msg'
        
        pre_commit_file.write_text("#!/bin/sh\n# Commit-AI hook")
        commit_msg_file.write_text("#!/bin/sh\n# Commit-AI hook")
        
        result = self.manager.uninstall_hooks(['pre-commit'])
        
        assert result is True
        assert not pre_commit_file.exists()
        assert commit_msg_file.exists()  # Este não foi removido
    
    def test_list_installed_hooks(self):
        """Testa listagem de hooks instalados"""
        # Criar hook com identificador Commit-AI
        pre_commit_file = self.hooks_dir / 'pre-commit'
        pre_commit_file.write_text("#!/bin/sh\n# Commit-AI hook\necho 'test'")
        
        # Criar hook sem identificador (não é nosso)
        post_commit_file = self.hooks_dir / 'post-commit'
        post_commit_file.write_text("#!/bin/sh\necho 'other hook'")
        
        status = self.manager.list_installed_hooks()
        
        assert status['pre-commit'] is True
        assert status['commit-msg'] is False
        assert status['post-commit'] is False
    
    def test_check_hooks_health(self):
        """Testa verificação de saúde dos hooks"""
        # Criar hook executável
        pre_commit_file = self.hooks_dir / 'pre-commit'
        pre_commit_file.write_text("#!/bin/sh\n# Commit-AI hook\necho 'test'")
        pre_commit_file.chmod(0o755)
        
        health = self.manager.check_hooks_health()
        
        assert "Funcionando" in health['pre-commit']
        assert health['commit-msg'] == "Não instalado"


class TestPreCommitHook:
    """Testes para PreCommitHook"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.hook = PreCommitHook()
    
    @patch('commit_ai.git_hooks.GitHandler')
    @patch('commit_ai.git_hooks.CommitTemplateManager')
    def test_run_with_changes(self, mock_template_manager, mock_git_handler):
        """Testa execução do hook com alterações"""
        # Mock do GitHandler
        mock_git = Mock()
        mock_git.has_staged_changes.return_value = True
        mock_git.get_staged_diff.return_value = "diff content"
        mock_git_handler.return_value = mock_git
        
        # Mock do TemplateManager
        mock_template = Mock()
        mock_template.analyze_diff_and_suggest_type.return_value = ("feat", 0.9)
        mock_template_manager.return_value = mock_template
        
        result = self.hook.run()
        
        assert result == 0
        mock_template.analyze_diff_and_suggest_type.assert_called_once()
    
    @patch('commit_ai.git_hooks.GitHandler')
    def test_run_without_changes(self, mock_git_handler):
        """Testa execução do hook sem alterações"""
        # Mock do GitHandler
        mock_git = Mock()
        mock_git.has_staged_changes.return_value = False
        mock_git_handler.return_value = mock_git
        
        result = self.hook.run()
        
        assert result == 0


class TestCommitMsgHook:
    """Testes para CommitMsgHook"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.hook = CommitMsgHook()
    
    def test_run_with_valid_message(self):
        """Testa execução com mensagem válida"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("feat: add new feature")
            msg_file = f.name
        
        try:
            result = self.hook.run(msg_file)
            assert result == 0
        finally:
            Path(msg_file).unlink()
    
    def test_run_with_invalid_message(self):
        """Testa execução com mensagem inválida"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("bad commit message")
            msg_file = f.name
        
        try:
            result = self.hook.run(msg_file)
            # Hook não falha, apenas sugere melhorias
            assert result == 0
        finally:
            Path(msg_file).unlink()
    
    @patch('commit_ai.git_hooks.ConfigManager')
    @patch('commit_ai.git_hooks.AIService')
    @patch('commit_ai.git_hooks.GitHandler')
    def test_auto_improve_message(self, mock_git_handler, mock_ai_service, mock_config):
        """Testa melhoria automática de mensagem"""
        # Mock da configuração
        mock_config_instance = Mock()
        mock_config_instance.get.return_value = True  # auto_improve_messages habilitado
        mock_config.return_value = mock_config_instance
        
        # Mock do AI Service
        mock_ai = Mock()
        mock_ai.generate_commit_message.return_value = "feat: improved commit message"
        mock_ai_service.return_value = mock_ai
        
        # Mock do GitHandler
        mock_git = Mock()
        mock_git.get_staged_diff.return_value = "diff content"
        mock_git_handler.return_value = mock_git
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("bad message")
            msg_file = f.name
        
        try:
            result = self.hook.run(msg_file)
            assert result == 0
            
            # Verificar se mensagem foi melhorada
            with open(msg_file, 'r') as f:
                improved_content = f.read().strip()
            
            assert "feat: improved commit message" in improved_content
            
        finally:
            Path(msg_file).unlink()


class TestPostCommitHook:
    """Testes para PostCommitHook"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.hook = PostCommitHook()
    
    @patch('commit_ai.git_hooks.GitHandler')
    def test_run_analytics(self, mock_git_handler):
        """Testa execução de analytics pós-commit"""
        # Mock do GitHandler
        mock_git = Mock()
        mock_git.get_last_commit_info.return_value = {
            'hash': 'abc123',
            'message': 'feat: add new feature',
            'author': 'Test User',
            'date': '2024-01-01'
        }
        mock_git_handler.return_value = mock_git
        
        result = self.hook.run()
        
        assert result == 0
        mock_git.get_last_commit_info.assert_called_once()


class TestHooksIntegration:
    """Testes de integração dos hooks"""
    
    def setup_method(self):
        """Setup para testes de integração"""
        self.temp_dir = tempfile.mkdtemp()
        self.git_dir = Path(self.temp_dir) / '.git'
        self.hooks_dir = self.git_dir / 'hooks'
        
        # Criar estrutura de diretórios
        self.git_dir.mkdir()
        self.hooks_dir.mkdir()
    
    def teardown_method(self):
        """Cleanup após testes"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_full_workflow(self):
        """Testa workflow completo de instalação e execução"""
        with patch('os.getcwd', return_value=self.temp_dir):
            manager = GitHooksManager(repo_path=self.temp_dir)
            
            # Instalar hooks
            with patch.object(manager, '_create_hook_scripts') as mock_create:
                mock_create.return_value = True
                result = manager.install_hooks()
                assert result is True
            
            # Verificar status
            status = manager.list_installed_hooks()
            assert isinstance(status, dict)
            
            # Verificar saúde
            health = manager.check_hooks_health()
            assert isinstance(health, dict)


if __name__ == '__main__':
    pytest.main([__file__])
