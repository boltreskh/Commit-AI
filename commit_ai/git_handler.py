"""
GitHandler - Módulo para interagir com o Git

Este módulo gerencia todas as operações relacionadas ao Git,
como obter diffs, verificar alterações e fazer commits.
"""

import os
import subprocess
import sys
from typing import Dict, List, Optional


class GitHandler:
    """Classe para gerenciar operações do Git"""
    
    def __init__(self):
        """Inicializa o GitHandler"""
        self.git_dir = self._find_git_root()
    
    def _find_git_root(self) -> Optional[str]:
        """
        Encontra a raiz do repositório Git
        
        Returns:
            str: Caminho para a raiz do repositório Git ou None se não encontrado
        """
        current_dir = os.getcwd()
        while current_dir != os.path.dirname(current_dir):
            if os.path.exists(os.path.join(current_dir, '.git')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        return None
    
    def is_git_repo(self) -> bool:
        """
        Verifica se o diretório atual é um repositório Git
        
        Returns:
            bool: True se for um repositório Git, False caso contrário
        """
        return self.git_dir is not None
    
    def _run_git_command(self, args: List[str]) -> str:
        """
        Executa um comando git e retorna a saída
        
        Args:
            args: Lista de argumentos para o comando git
            
        Returns:
            str: Saída do comando git
            
        Raises:
            subprocess.CalledProcessError: Se o comando falhar
        """
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.git_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erro ao executar comando git: {e.stderr}")
    
    def get_staged_diff(self) -> str:
        """
        Obtém o diff das alterações staged (prontas para commit)
        
        Returns:
            str: Diff das alterações staged
        """
        try:
            # Primeiro, verifica se há alterações staged
            staged_files = self._run_git_command(['diff', '--cached', '--name-only'])
            if not staged_files:
                return ""
            
            # Obtém o diff completo das alterações staged
            diff = self._run_git_command(['diff', '--cached'])
            return diff
        except Exception:
            return ""
    
    def get_file_changes(self) -> Dict[str, List[str]]:
        """
        Obtém informações sobre arquivos alterados
        
        Returns:
            Dict com tipos de alterações e listas de arquivos
        """
        changes = {
            'Modificados': [],
            'Adicionados': [],
            'Removidos': [],
            'Renomeados': []
        }
        
        try:
            # Obter status dos arquivos staged
            status_output = self._run_git_command(['diff', '--cached', '--name-status'])
            
            for line in status_output.split('\n'):
                if not line.strip():
                    continue
                
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                
                status = parts[0]
                filename = parts[1]
                
                if status == 'M':
                    changes['Modificados'].append(filename)
                elif status == 'A':
                    changes['Adicionados'].append(filename)
                elif status == 'D':
                    changes['Removidos'].append(filename)
                elif status.startswith('R'):
                    if len(parts) >= 3:
                        changes['Renomeados'].append(f"{parts[1]} → {parts[2]}")
                    else:
                        changes['Renomeados'].append(filename)
        
        except Exception:
            pass  # Retorna dicionário vazio em caso de erro
        
        return changes
    
    def commit(self, message: str) -> bool:
        """
        Realiza um commit com a mensagem fornecida
        
        Args:
            message: Mensagem do commit
            
        Returns:
            bool: True se o commit foi bem-sucedido, False caso contrário
        """
        try:
            self._run_git_command(['commit', '-m', message])
            return True
        except Exception as e:
            print(f"Erro ao fazer commit: {str(e)}")
            return False
    
    def has_staged_changes(self) -> bool:
        """
        Verifica se há alterações staged para commit
        
        Returns:
            bool: True se há alterações staged, False caso contrário
        """
        try:
            staged_files = self._run_git_command(['diff', '--cached', '--name-only'])
            return bool(staged_files.strip())
        except Exception:
            return False
