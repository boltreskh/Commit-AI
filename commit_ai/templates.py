"""
Template System - Sistema de templates personalizáveis para mensagens de commit

Este módulo permite criar e gerenciar templates de commit personalizados
baseados no tipo de alteração, linguagem de programação, etc.
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from .logger import logger
from .config_manager import ConfigManager


class CommitTemplateManager:
    """Gerenciador de templates de commit personalizáveis"""
    
    DEFAULT_TEMPLATES = {
        "feat": {
            "pattern": "feat({scope}): {description}",
            "description": "Nova funcionalidade",
            "examples": [
                "feat(auth): adiciona autenticação por JWT",
                "feat(ui): implementa componente de botão",
                "feat(api): adiciona endpoint de usuários"
            ]
        },
        "fix": {
            "pattern": "fix({scope}): {description}",
            "description": "Correção de bug",
            "examples": [
                "fix(login): corrige validação de senha",
                "fix(db): resolve problema de conexão",
                "fix(ui): corrige layout responsivo"
            ]
        },
        "docs": {
            "pattern": "docs({scope}): {description}",
            "description": "Documentação",
            "examples": [
                "docs(readme): atualiza guia de instalação",
                "docs(api): adiciona documentação dos endpoints",
                "docs(changelog): adiciona release v1.2.0"
            ]
        },
        "style": {
            "pattern": "style({scope}): {description}",
            "description": "Formatação de código",
            "examples": [
                "style(eslint): corrige warnings de lint",
                "style(format): ajusta indentação do código",
                "style(imports): reorganiza imports"
            ]
        },
        "refactor": {
            "pattern": "refactor({scope}): {description}",
            "description": "Refatoração de código",
            "examples": [
                "refactor(auth): simplifica lógica de login",
                "refactor(utils): extrai funções auxiliares",
                "refactor(api): melhora estrutura de rotas"
            ]
        },
        "test": {
            "pattern": "test({scope}): {description}",
            "description": "Testes",
            "examples": [
                "test(auth): adiciona testes de login",
                "test(api): implementa testes de integração",
                "test(utils): adiciona testes unitários"
            ]
        },
        "chore": {
            "pattern": "chore({scope}): {description}",
            "description": "Manutenção",
            "examples": [
                "chore(deps): atualiza dependências",
                "chore(config): ajusta configuração do build",
                "chore(ci): melhora pipeline de deploy"
            ]
        },
        "perf": {
            "pattern": "perf({scope}): {description}",
            "description": "Performance",
            "examples": [
                "perf(db): otimiza consultas SQL",
                "perf(cache): implementa cache Redis",
                "perf(api): reduz tempo de resposta"
            ]
        }
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Inicializa o gerenciador de templates
        
        Args:
            config_dir: Diretório de configuração personalizado
        """
        self.config_manager = ConfigManager()
        
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / '.commit-ai'
        
        self.templates_file = self.config_dir / 'templates.json'
        self.config_dir.mkdir(exist_ok=True)
        
        # Carregar templates
        self.templates = self._load_templates()
        logger.debug(f"Templates carregados: {list(self.templates.keys())}")
    
    def _load_templates(self) -> Dict[str, Any]:
        """Carrega templates do arquivo de configuração"""
        if self.templates_file.exists():
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    custom_templates = json.load(f)
                    
                # Mesclar templates padrão com personalizados
                templates = self.DEFAULT_TEMPLATES.copy()
                templates.update(custom_templates)
                
                logger.info(f"Templates personalizados carregados: {len(custom_templates)} customizados")
                return templates
                
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Erro ao carregar templates personalizados: {e}")
                logger.info("Usando templates padrão")
        
        # Criar arquivo de templates padrão
        self._save_templates(self.DEFAULT_TEMPLATES)
        return self.DEFAULT_TEMPLATES.copy()
    
    def _save_templates(self, templates: Dict[str, Any]):
        """Salva templates no arquivo de configuração"""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(templates, f, indent=2, ensure_ascii=False)
            logger.debug("Templates salvos com sucesso")
        except IOError as e:
            logger.error(f"Erro ao salvar templates: {e}")
    
    def get_template(self, commit_type: str) -> Optional[Dict[str, Any]]:
        """
        Obtém um template por tipo
        
        Args:
            commit_type: Tipo do commit (feat, fix, docs, etc.)
            
        Returns:
            Dict com dados do template ou None se não encontrado
        """
        return self.templates.get(commit_type.lower())
    
    def get_all_templates(self) -> Dict[str, Any]:
        """Retorna todos os templates disponíveis"""
        return self.templates.copy()
    
    def get_template_types(self) -> List[str]:
        """Retorna lista de tipos de template disponíveis"""
        return list(self.templates.keys())
    
    def add_template(self, commit_type: str, pattern: str, description: str, 
                    examples: List[str] = None) -> bool:
        """
        Adiciona um novo template personalizado
        
        Args:
            commit_type: Tipo do commit
            pattern: Padrão do template (ex: "feat({scope}): {description}")
            description: Descrição do tipo de commit
            examples: Lista de exemplos
            
        Returns:
            bool: True se adicionado com sucesso
        """
        try:
            self.templates[commit_type.lower()] = {
                "pattern": pattern,
                "description": description,
                "examples": examples or []
            }
            
            self._save_templates(self.templates)
            logger.info(f"Template '{commit_type}' adicionado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao adicionar template: {e}")
            return False
    
    def remove_template(self, commit_type: str) -> bool:
        """
        Remove um template personalizado
        
        Args:
            commit_type: Tipo do template a remover
            
        Returns:
            bool: True se removido com sucesso
        """
        if commit_type.lower() in self.DEFAULT_TEMPLATES:
            logger.warning(f"Não é possível remover template padrão: {commit_type}")
            return False
        
        if commit_type.lower() in self.templates:
            try:
                del self.templates[commit_type.lower()]
                self._save_templates(self.templates)
                logger.info(f"Template '{commit_type}' removido com sucesso")
                return True
            except Exception as e:
                logger.error(f"Erro ao remover template: {e}")
        
        return False
    
    def analyze_diff_and_suggest_type(self, diff_text: str) -> str:
        """
        Analisa o diff e sugere o tipo de commit mais apropriado
        
        Args:
            diff_text: Texto do diff do Git
            
        Returns:
            str: Tipo de commit sugerido
        """
        diff_lower = diff_text.lower()
        
        # Palavras-chave para cada tipo de commit
        keywords = {
            "test": ["test", "spec", "unittest", "pytest", "jest", ".test.", "_test", "testing"],
            "docs": ["readme", "doc", "documentation", "changelog", "md", ".md", "comment"],
            "style": ["format", "lint", "eslint", "prettier", "style", "indent", "whitespace"],
            "fix": ["fix", "bug", "error", "issue", "problem", "resolve", "patch"],
            "perf": ["performance", "perf", "speed", "fast", "optimize", "cache", "memory"],
            "refactor": ["refactor", "cleanup", "simplify", "restructure", "reorganize"],
            "chore": ["dependency", "deps", "package.json", "requirements", "config", "build"],
            "feat": ["add", "new", "feature", "implement", "create", "introduce"]
        }
        
        # Contar matches para cada tipo
        scores = {}
        for commit_type, words in keywords.items():
            score = sum(diff_lower.count(word) for word in words)
            if score > 0:
                scores[commit_type] = score
        
        if scores:
            suggested_type = max(scores.items(), key=lambda x: x[1])[0]
            logger.debug(f"Tipo sugerido baseado no diff: {suggested_type} (score: {scores[suggested_type]})")
            return suggested_type
        
        # Fallback para feat se não encontrar matches
        logger.debug("Nenhum tipo específico detectado, usando 'feat' como padrão")
        return "feat"
    
    def generate_message_with_template(self, commit_type: str, description: str, 
                                     scope: Optional[str] = None) -> str:
        """
        Gera uma mensagem de commit usando um template
        
        Args:
            commit_type: Tipo do commit
            description: Descrição da mudança
            scope: Escopo da mudança (opcional)
            
        Returns:
            str: Mensagem de commit formatada
        """
        template = self.get_template(commit_type)
        if not template:
            logger.warning(f"Template '{commit_type}' não encontrado, usando formato básico")
            return f"{commit_type}: {description}"
        
        pattern = template["pattern"]
        
        # Substituir variáveis no template
        if scope:
            message = pattern.replace("{scope}", scope)
        else:
            # Remove o scope se não fornecido
            message = pattern.replace("({scope})", "").replace("{scope}", "")
        
        message = message.replace("{description}", description)
        
        logger.debug(f"Mensagem gerada com template: {message}")
        return message
    
    def export_templates(self, export_path: str) -> bool:
        """
        Exporta templates para um arquivo JSON
        
        Args:
            export_path: Caminho para salvar o arquivo
            
        Returns:
            bool: True se exportado com sucesso
        """
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Templates exportados para: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar templates: {e}")
            return False
    
    def import_templates(self, import_path: str, merge: bool = True) -> bool:
        """
        Importa templates de um arquivo JSON
        
        Args:
            import_path: Caminho do arquivo para importar
            merge: Se True, mescla com existentes. Se False, substitui todos
            
        Returns:
            bool: True se importado com sucesso
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_templates = json.load(f)
            
            if merge:
                self.templates.update(imported_templates)
            else:
                self.templates = imported_templates
            
            self._save_templates(self.templates)
            
            action = "mesclados" if merge else "substituídos"
            logger.info(f"Templates {action} com sucesso de: {import_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao importar templates: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """
        Reseta todos os templates para os padrões originais
        
        Returns:
            bool: True se resetado com sucesso
        """
    def export_templates(self, export_path: str) -> bool:
        """
        Exporta templates para um arquivo JSON
        
        Args:
            export_path: Caminho para salvar o arquivo
            
        Returns:
            bool: True se exportado com sucesso
        """
        try:
            export_file = Path(export_path)
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Templates exportados para: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar templates: {e}")
            return False
    
    def import_templates(self, import_path: str, merge: bool = True) -> bool:
        """
        Importa templates de um arquivo JSON
        
        Args:
            import_path: Caminho do arquivo para importar
            merge: Se True, mescla com templates existentes; se False, substitui
            
        Returns:
            bool: True se importado com sucesso
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                logger.error(f"Arquivo não encontrado: {import_path}")
                return False
            
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_templates = json.load(f)
            
            if merge:
                self.templates.update(imported_templates)
            else:
                self.templates = imported_templates
            
            self._save_templates(self.templates)
            logger.info(f"Templates importados de: {import_path}")
            return True
            
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Erro ao importar templates: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """
        Reseta templates para os padrões originais
        
        Returns:
            bool: True se resetado com sucesso
        """
        try:
            self.templates = self.DEFAULT_TEMPLATES.copy()
            self._save_templates(self.templates)
            logger.info("Templates resetados para padrões originais")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao resetar templates: {e}")
            return False
            return False
