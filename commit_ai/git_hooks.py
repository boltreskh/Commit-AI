#!/usr/bin/env python3
"""
Sistema de Git Hooks para Commit-AI v1.3.0

Implementa hooks automáticos para integração seamless com o fluxo Git:
- pre-commit: Gera sugestões de commit automaticamente
- commit-msg: Valida e melhora mensagens de commit
- post-commit: Analytics e logging avançado
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, List
import click

from .logger import logger
from .git_handler import GitHandler
from .ai_service import AIService
from .config_manager import ConfigManager
from .templates import CommitTemplateManager


class GitHooksManager:
    """Gerenciador de Git Hooks para automação de commits"""
    
    HOOKS = {
        'pre-commit': 'pre_commit_hook.py',
        'commit-msg': 'commit_msg_hook.py',
        'post-commit': 'post_commit_hook.py'
    }
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.git_handler = GitHandler()
        self.hooks_dir = Path(self.git_handler.repo_path) / '.git' / 'hooks'
        
    def install_hooks(self, hooks: List[str] = None) -> bool:
        """
        Instala os Git Hooks especificados
        
        Args:
            hooks: Lista de hooks para instalar. Se None, instala todos.
            
        Returns:
            bool: True se todos os hooks foram instalados com sucesso
        """
        if not self.git_handler.is_git_repo():
            logger.error("Diretório atual não é um repositório Git")
            return False
            
        hooks_to_install = hooks or list(self.HOOKS.keys())
        success_count = 0
        
        for hook_name in hooks_to_install:
            if self._install_single_hook(hook_name):
                success_count += 1
                logger.info(f"Hook {hook_name} instalado com sucesso")
            else:
                logger.error(f"Falha ao instalar hook {hook_name}")
                
        total_hooks = len(hooks_to_install)
        logger.info(f"Instalação concluída: {success_count}/{total_hooks} hooks")
        
        return success_count == total_hooks
    
    def _install_single_hook(self, hook_name: str) -> bool:
        """Instala um hook individual"""
        if hook_name not in self.HOOKS:
            logger.error(f"Hook desconhecido: {hook_name}")
            return False
            
        hook_path = self.hooks_dir / hook_name
        
        # Backup do hook existente se houver
        if hook_path.exists():
            backup_path = hook_path.with_suffix('.backup')
            shutil.move(str(hook_path), str(backup_path))
            logger.info(f"Backup criado: {backup_path}")
        
        # Criar o hook script
        hook_content = self._generate_hook_script(hook_name)
        
        try:
            with open(hook_path, 'w', encoding='utf-8') as f:
                f.write(hook_content)
            
            # Tornar executável no Unix/Linux
            if os.name != 'nt':  # não é Windows
                os.chmod(hook_path, 0o755)
                
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar hook {hook_name}: {e}")
            return False
    
    def _generate_hook_script(self, hook_name: str) -> str:
        """Gera o script do hook"""
        python_path = sys.executable
        commit_ai_path = Path(__file__).parent.parent
        
        if hook_name == 'pre-commit':
            return f"""#!/usr/bin/env python3
# Commit-AI Pre-commit Hook
# Gerado automaticamente - NÃO EDITAR

import sys
import os
sys.path.insert(0, '{commit_ai_path}')

from commit_ai.git_hooks import PreCommitHook

if __name__ == '__main__':
    hook = PreCommitHook()
    sys.exit(hook.run())
"""
        
        elif hook_name == 'commit-msg':
            return f"""#!/usr/bin/env python3
# Commit-AI Commit-msg Hook  
# Gerado automaticamente - NÃO EDITAR

import sys
import os
sys.path.insert(0, '{commit_ai_path}')

from commit_ai.git_hooks import CommitMsgHook

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: commit-msg <arquivo-mensagem>")
        sys.exit(1)
        
    hook = CommitMsgHook()
    sys.exit(hook.run(sys.argv[1]))
"""
        
        elif hook_name == 'post-commit':
            return f"""#!/usr/bin/env python3  
# Commit-AI Post-commit Hook
# Gerado automaticamente - NÃO EDITAR

import sys
import os
sys.path.insert(0, '{commit_ai_path}')

from commit_ai.git_hooks import PostCommitHook

if __name__ == '__main__':
    hook = PostCommitHook()
    sys.exit(hook.run())
"""
        
        return ""
    
    def uninstall_hooks(self, hooks: List[str] = None) -> bool:
        """Remove os Git Hooks especificados"""
        hooks_to_remove = hooks or list(self.HOOKS.keys())
        success_count = 0
        
        for hook_name in hooks_to_remove:
            hook_path = self.hooks_dir / hook_name
            backup_path = hook_path.with_suffix('.backup')
            
            try:
                if hook_path.exists():
                    hook_path.unlink()
                    logger.info(f"Hook {hook_name} removido")
                
                # Restaurar backup se existir
                if backup_path.exists():
                    shutil.move(str(backup_path), str(hook_path))
                    logger.info(f"Backup {hook_name} restaurado")
                
                success_count += 1
                
            except Exception as e:
                logger.error(f"Erro ao remover hook {hook_name}: {e}")
                
        return success_count == len(hooks_to_remove)
    
    def list_installed_hooks(self) -> Dict[str, bool]:
        """Lista o status de instalação dos hooks"""
        status = {}
        
        for hook_name in self.HOOKS:
            hook_path = self.hooks_dir / hook_name
            status[hook_name] = hook_path.exists()
            
        return status
    
    def check_hooks_health(self) -> Dict[str, str]:
        """Verifica a saúde dos hooks instalados"""
        health = {}
        
        for hook_name in self.HOOKS:
            hook_path = self.hooks_dir / hook_name
            
            if not hook_path.exists():
                health[hook_name] = "Não instalado"
            elif not os.access(hook_path, os.X_OK) and os.name != 'nt':
                health[hook_name] = "Não executável"
            else:
                try:
                    with open(hook_path, 'r') as f:
                        content = f.read()
                    if 'Commit-AI' in content:
                        health[hook_name] = "Funcionando"
                    else:
                        health[hook_name] = "Hook externo"
                except Exception:
                    health[hook_name] = "Erro de leitura"
                    
        return health


class PreCommitHook:
    """Hook executado antes do commit"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.template_manager = CommitTemplateManager()
        
    def run(self) -> int:
        """Executa o pre-commit hook"""
        try:
            # Verificar se deve executar automação
            if not self.config_manager.get('hooks_enabled', True):
                return 0
                
            # Analisar mudanças staged
            git_handler = GitHandler()
            if not git_handler.has_staged_changes():
                return 0
            
            diff = git_handler.get_staged_diff()
            
            # Sugerir tipo de commit baseado no diff
            suggested_type = self.template_manager.analyze_diff_and_suggest_type(diff)
            
            # Log da sugestão
            logger.info(f"Pre-commit: Tipo sugerido '{suggested_type}' baseado no diff")
            
            # Salvar sugestão para uso posterior
            suggestion_file = Path.home() / '.commit-ai' / 'last_suggestion.txt'
            suggestion_file.parent.mkdir(exist_ok=True)
            
            with open(suggestion_file, 'w') as f:
                f.write(f"type={suggested_type}\n")
                f.write(f"timestamp={logger.logger.handlers[0].formatter.formatTime(logger.logger.makeRecord('', 0, '', 0, '', (), None))}\n")
            
            return 0
            
        except Exception as e:
            logger.error(f"Erro no pre-commit hook: {e}")
            return 0  # Não bloquear o commit em caso de erro


class CommitMsgHook:
    """Hook para validação e melhoria de mensagens de commit"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.template_manager = CommitTemplateManager()
        
    def run(self, commit_msg_file: str) -> int:
        """Executa o commit-msg hook"""
        try:
            if not self.config_manager.get('hooks_enabled', True):
                return 0
                
            with open(commit_msg_file, 'r', encoding='utf-8') as f:
                original_msg = f.read().strip()
            
            # Pular se mensagem vazia ou é um merge/revert
            if not original_msg or original_msg.startswith(('Merge', 'Revert')):
                return 0
            
            # Validar formato da mensagem
            validation_result = self._validate_message(original_msg)
            
            if validation_result['valid']:
                logger.info("Mensagem de commit válida")
                return 0
            else:
                # Tentar melhorar a mensagem se configurado
                if self.config_manager.get('auto_improve_messages', False):
                    improved_msg = self._improve_message(original_msg)
                    
                    if improved_msg and improved_msg != original_msg:
                        with open(commit_msg_file, 'w', encoding='utf-8') as f:
                            f.write(improved_msg)
                        logger.info("Mensagem de commit melhorada automaticamente")
                        
                return 0  # Não bloquear mesmo com problemas
                
        except Exception as e:
            logger.error(f"Erro no commit-msg hook: {e}")
            return 0
    
    def _validate_message(self, message: str) -> Dict[str, any]:
        """Valida formato da mensagem de commit"""
        lines = message.strip().split('\n')
        first_line = lines[0] if lines else ""
        
        # Verificações básicas
        checks = {
            'length_ok': len(first_line) <= 72,
            'has_type': any(first_line.startswith(t + ':') or first_line.startswith(t + '(') 
                          for t in self.template_manager.get_template_types()),
            'capitalized': first_line and first_line[0].isupper(),
            'no_period': not first_line.endswith('.')
        }
        
        return {
            'valid': all(checks.values()),
            'checks': checks,
            'message': first_line
        }
    
    def _improve_message(self, message: str) -> Optional[str]:
        """Tenta melhorar a mensagem de commit"""
        lines = message.strip().split('\n')
        first_line = lines[0] if lines else ""
        
        # Melhorias simples
        improved = first_line
        
        # Remover ponto final se houver
        if improved.endswith('.'):
            improved = improved[:-1]
            
        # Capitalizar primeira letra
        if improved and improved[0].islower():
            improved = improved[0].upper() + improved[1:]
        
        # Se não tem tipo, tentar adicionar baseado em palavras-chave
        if not any(improved.startswith(t + ':') or improved.startswith(t + '(') 
                  for t in self.template_manager.get_template_types()):
            
            # Análise básica de palavras-chave
            lower_msg = improved.lower()
            if any(word in lower_msg for word in ['fix', 'corrige', 'resolve']):
                improved = f"fix: {improved.lower()}"
            elif any(word in lower_msg for word in ['add', 'adiciona', 'nova', 'novo']):
                improved = f"feat: {improved.lower()}"
            elif any(word in lower_msg for word in ['update', 'atualiza', 'melhora']):
                improved = f"chore: {improved.lower()}"
                
        return improved if improved != first_line else None


class PostCommitHook:
    """Hook executado após o commit"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        
    def run(self) -> int:
        """Executa o post-commit hook"""
        try:
            if not self.config_manager.get('hooks_enabled', True):
                return 0
            
            # Analytics básico
            git_handler = GitHandler()
            last_commit = git_handler.get_last_commit_message()
            
            if last_commit:
                # Log para analytics
                logger.info(f"Post-commit: {last_commit[:50]}...")
                
                # Limpar arquivo de sugestão
                suggestion_file = Path.home() / '.commit-ai' / 'last_suggestion.txt'
                if suggestion_file.exists():
                    suggestion_file.unlink()
            
            return 0
            
        except Exception as e:
            logger.error(f"Erro no post-commit hook: {e}")
            return 0
