#!/usr/bin/env python3
"""
Sistema de Plugins Extensível para Commit-AI v1.4.0

Permite extensão das funcionalidades através de plugins customizados
que podem adicionar novos providers de IA, templates ou funcionalidades.
"""

import importlib
import importlib.util
import inspect
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, Type, Callable
from dataclasses import dataclass

from .config_manager import ConfigManager
from .logger import logger


@dataclass
class PluginInfo:
    """Informações de um plugin"""
    name: str
    version: str
    description: str
    author: str
    category: str
    dependencies: List[str]
    enabled: bool
    file_path: Path


class PluginBase(ABC):
    """Classe base para todos os plugins"""
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações do plugin"""
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """Inicializa o plugin"""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """Limpa recursos do plugin"""
        pass


class AIProviderPlugin(PluginBase):
    """Plugin para provedores de IA customizados"""
    
    @abstractmethod
    def generate_commit_message(self, 
                               diff: str, 
                               template: str = "conventional",
                               **kwargs) -> str:
        """Gera mensagem de commit usando IA customizada"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o provider está disponível"""
        pass
    
    @abstractmethod
    def get_supported_models(self) -> List[str]:
        """Retorna modelos suportados pelo provider"""
        pass


class TemplatePlugin(PluginBase):
    """Plugin para templates customizados"""
    
    @abstractmethod
    def get_template(self) -> Dict[str, Any]:
        """Retorna definição do template"""
        pass
    
    @abstractmethod
    def format_message(self, commit_type: str, description: str, **kwargs) -> str:
        """Formata mensagem usando o template"""
        pass


class WorkflowPlugin(PluginBase):
    """Plugin para workflows customizados"""
    
    @abstractmethod
    def pre_commit_hook(self, diff: str) -> Optional[Dict[str, Any]]:
        """Hook executado antes do commit"""
        pass
    
    @abstractmethod
    def post_commit_hook(self, commit_info: Dict[str, Any]) -> None:
        """Hook executado após o commit"""
        pass


class IntegrationPlugin(PluginBase):
    """Plugin para integrações externas"""
    
    @abstractmethod
    def connect(self, config: Dict[str, Any]) -> bool:
        """Conecta com serviço externo"""
        pass
    
    @abstractmethod
    def send_data(self, data: Dict[str, Any]) -> bool:
        """Envia dados para serviço externo"""
        pass


class PluginManager:
    """Gerenciador de plugins do Commit-AI"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        
        # Diretórios de plugins
        self.system_plugins_dir = Path(__file__).parent / 'plugins'
        self.user_plugins_dir = Path.home() / '.commit-ai' / 'plugins'
        
        # Criar diretórios se não existem
        self.user_plugins_dir.mkdir(parents=True, exist_ok=True)
        self.system_plugins_dir.mkdir(exist_ok=True)
        
        # Hooks para diferentes categorias
        self.ai_providers: Dict[str, AIProviderPlugin] = {}
        self.templates: Dict[str, TemplatePlugin] = {}
        self.workflows: Dict[str, WorkflowPlugin] = {}
        self.integrations: Dict[str, IntegrationPlugin] = {}
    
    def load_plugins(self) -> None:
        """Carrega todos os plugins disponíveis"""
        try:
            # Carregar plugins do sistema
            self._load_plugins_from_directory(self.system_plugins_dir, is_system=True)
            
            # Carregar plugins do usuário
            self._load_plugins_from_directory(self.user_plugins_dir, is_system=False)
            
            # Inicializar plugins habilitados
            self._initialize_enabled_plugins()
            
            logger.info(f"Plugins carregados: {len(self.plugins)}")
            
        except Exception as e:
            logger.error(f"Erro ao carregar plugins: {e}")
    
    def _load_plugins_from_directory(self, directory: Path, is_system: bool) -> None:
        """Carrega plugins de um diretório específico"""
        if not directory.exists():
            return
        
        for plugin_file in directory.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue  # Ignorar arquivos privados
            
            try:
                self._load_plugin_file(plugin_file, is_system)
            except Exception as e:
                logger.warning(f"Erro ao carregar plugin {plugin_file.name}: {e}")
    
    def _load_plugin_file(self, plugin_file: Path, is_system: bool) -> None:
        """Carrega um arquivo de plugin específico"""
        module_name = f"commit_ai_plugin_{plugin_file.stem}"
        
        # Carregar módulo
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        if not spec or not spec.loader:
            logger.warning(f"Não foi possível criar spec para {plugin_file}")
            return
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Encontrar classes de plugin no módulo
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if (issubclass(obj, PluginBase) and 
                obj != PluginBase and 
                not name.endswith('Plugin')):  # Evitar classes base
                
                try:
                    plugin_instance = obj()
                    plugin_info = plugin_instance.get_info()
                    
                    # Criar objeto PluginInfo
                    info = PluginInfo(
                        name=plugin_info.get('name', name),
                        version=plugin_info.get('version', '1.0.0'),
                        description=plugin_info.get('description', ''),
                        author=plugin_info.get('author', 'Unknown'),
                        category=plugin_info.get('category', 'general'),
                        dependencies=plugin_info.get('dependencies', []),
                        enabled=self._is_plugin_enabled(plugin_info.get('name', name)),
                        file_path=plugin_file
                    )
                    
                    # Registrar plugin
                    self.plugins[info.name] = plugin_instance
                    self.plugin_info[info.name] = info
                    
                    logger.debug(f"Plugin carregado: {info.name} v{info.version}")
                    
                except Exception as e:
                    logger.error(f"Erro ao instanciar plugin {name}: {e}")
    
    def _is_plugin_enabled(self, plugin_name: str) -> bool:
        """Verifica se um plugin está habilitado na configuração"""
        enabled_plugins = self.config_manager.get('enabled_plugins', [])
        disabled_plugins = self.config_manager.get('disabled_plugins', [])
        
        # Por padrão, plugins estão habilitados unless explicitamente desabilitados
        if plugin_name in disabled_plugins:
            return False
        
        return True
    
    def _initialize_enabled_plugins(self) -> None:
        """Inicializa plugins habilitados"""
        for plugin_name, plugin in self.plugins.items():
            info = self.plugin_info[plugin_name]
            
            if not info.enabled:
                continue
            
            try:
                # Verificar dependências
                if not self._check_dependencies(info.dependencies):
                    logger.warning(f"Plugin {plugin_name}: dependências não satisfeitas")
                    continue
                
                # Inicializar plugin
                if plugin.initialize():
                    self._categorize_plugin(plugin_name, plugin, info)
                    logger.info(f"Plugin inicializado: {plugin_name}")
                else:
                    logger.warning(f"Plugin {plugin_name}: falha na inicialização")
                    
            except Exception as e:
                logger.error(f"Erro ao inicializar plugin {plugin_name}: {e}")
    
    def _check_dependencies(self, dependencies: List[str]) -> bool:
        """Verifica se as dependências estão disponíveis"""
        for dep in dependencies:
            try:
                importlib.import_module(dep)
            except ImportError:
                return False
        return True
    
    def _categorize_plugin(self, name: str, plugin: PluginBase, info: PluginInfo) -> None:
        """Categoriza plugin baseado no tipo"""
        if isinstance(plugin, AIProviderPlugin):
            self.ai_providers[name] = plugin
        elif isinstance(plugin, TemplatePlugin):
            self.templates[name] = plugin
        elif isinstance(plugin, WorkflowPlugin):
            self.workflows[name] = plugin
        elif isinstance(plugin, IntegrationPlugin):
            self.integrations[name] = plugin
    
    def get_available_plugins(self, category: Optional[str] = None) -> List[PluginInfo]:
        """Retorna lista de plugins disponíveis"""
        plugins = list(self.plugin_info.values())
        
        if category:
            plugins = [p for p in plugins if p.category == category]
        
        return plugins
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Habilita um plugin específico"""
        if plugin_name not in self.plugins:
            logger.error(f"Plugin não encontrado: {plugin_name}")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            info = self.plugin_info[plugin_name]
            
            # Verificar dependências
            if not self._check_dependencies(info.dependencies):
                logger.error(f"Plugin {plugin_name}: dependências não satisfeitas")
                return False
            
            # Inicializar plugin
            if plugin.initialize():
                info.enabled = True
                self._categorize_plugin(plugin_name, plugin, info)
                
                # Atualizar configuração
                enabled_plugins = self.config_manager.get('enabled_plugins', [])
                if plugin_name not in enabled_plugins:
                    enabled_plugins.append(plugin_name)
                    self.config_manager.set('enabled_plugins', enabled_plugins)
                
                # Remover da lista de desabilitados
                disabled_plugins = self.config_manager.get('disabled_plugins', [])
                if plugin_name in disabled_plugins:
                    disabled_plugins.remove(plugin_name)
                    self.config_manager.set('disabled_plugins', disabled_plugins)
                
                logger.info(f"Plugin habilitado: {plugin_name}")
                return True
            else:
                logger.error(f"Falha ao inicializar plugin: {plugin_name}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao habilitar plugin {plugin_name}: {e}")
            return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Desabilita um plugin específico"""
        if plugin_name not in self.plugins:
            logger.error(f"Plugin não encontrado: {plugin_name}")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            info = self.plugin_info[plugin_name]
            
            # Limpar recursos do plugin
            plugin.cleanup()
            info.enabled = False
            
            # Remover das categorias
            self.ai_providers.pop(plugin_name, None)
            self.templates.pop(plugin_name, None)
            self.workflows.pop(plugin_name, None)
            self.integrations.pop(plugin_name, None)
            
            # Atualizar configuração
            disabled_plugins = self.config_manager.get('disabled_plugins', [])
            if plugin_name not in disabled_plugins:
                disabled_plugins.append(plugin_name)
                self.config_manager.set('disabled_plugins', disabled_plugins)
            
            # Remover da lista de habilitados
            enabled_plugins = self.config_manager.get('enabled_plugins', [])
            if plugin_name in enabled_plugins:
                enabled_plugins.remove(plugin_name)
                self.config_manager.set('enabled_plugins', enabled_plugins)
            
            logger.info(f"Plugin desabilitado: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao desabilitar plugin {plugin_name}: {e}")
            return False
    
    def install_plugin(self, plugin_path: Path) -> bool:
        """Instala plugin a partir de arquivo"""
        try:
            if not plugin_path.exists():
                logger.error(f"Arquivo de plugin não encontrado: {plugin_path}")
                return False
            
            # Copiar plugin para diretório do usuário
            destination = self.user_plugins_dir / plugin_path.name
            
            if destination.exists():
                logger.error(f"Plugin já existe: {plugin_path.name}")
                return False
            
            destination.write_text(plugin_path.read_text(), encoding='utf-8')
            
            # Carregar o novo plugin
            self._load_plugin_file(destination, is_system=False)
            
            logger.info(f"Plugin instalado: {plugin_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao instalar plugin: {e}")
            return False
    
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Desinstala plugin do usuário"""
        if plugin_name not in self.plugin_info:
            logger.error(f"Plugin não encontrado: {plugin_name}")
            return False
        
        try:
            info = self.plugin_info[plugin_name]
            
            # Apenas plugins do usuário podem ser desinstalados
            if not str(info.file_path).startswith(str(self.user_plugins_dir)):
                logger.error(f"Não é possível desinstalar plugin do sistema: {plugin_name}")
                return False
            
            # Desabilitar plugin primeiro
            self.disable_plugin(plugin_name)
            
            # Remover arquivo
            if info.file_path.exists():
                info.file_path.unlink()
            
            # Remover das estruturas internas
            self.plugins.pop(plugin_name, None)
            self.plugin_info.pop(plugin_name, None)
            
            logger.info(f"Plugin desinstalado: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao desinstalar plugin: {e}")
            return False
    
    def get_ai_providers(self) -> Dict[str, AIProviderPlugin]:
        """Retorna providers de IA disponíveis via plugins"""
        return self.ai_providers.copy()
    
    def get_templates(self) -> Dict[str, TemplatePlugin]:
        """Retorna templates disponíveis via plugins"""
        return self.templates.copy()
    
    def execute_workflow_hooks(self, 
                              hook_type: str, 
                              data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa hooks de workflow de todos os plugins"""
        results = {}
        
        for name, workflow_plugin in self.workflows.items():
            try:
                if hook_type == 'pre_commit':
                    result = workflow_plugin.pre_commit_hook(data.get('diff', ''))
                    if result:
                        results[name] = result
                        
                elif hook_type == 'post_commit':
                    workflow_plugin.post_commit_hook(data)
                    results[name] = True
                    
            except Exception as e:
                logger.error(f"Erro ao executar hook {hook_type} do plugin {name}: {e}")
                results[name] = False
        
        return results
    
    def cleanup_all_plugins(self) -> None:
        """Limpa recursos de todos os plugins"""
        for plugin_name, plugin in self.plugins.items():
            try:
                plugin.cleanup()
            except Exception as e:
                logger.error(f"Erro ao limpar plugin {plugin_name}: {e}")


# Instância global do gerenciador de plugins
plugin_manager = PluginManager()


if __name__ == "__main__":
    # Teste do sistema de plugins
    manager = PluginManager()
    manager.load_plugins()
    
    print("Plugins disponíveis:")
    for plugin_info in manager.get_available_plugins():
        status = "✅" if plugin_info.enabled else "❌"
        print(f"  {status} {plugin_info.name} v{plugin_info.version} ({plugin_info.category})")
        print(f"    {plugin_info.description}")
        print(f"    Autor: {plugin_info.author}")
        if plugin_info.dependencies:
            print(f"    Dependências: {', '.join(plugin_info.dependencies)}")
        print()
    
    print(f"AI Providers: {len(manager.ai_providers)}")
    print(f"Templates: {len(manager.templates)}")
    print(f"Workflows: {len(manager.workflows)}")
    print(f"Integrações: {len(manager.integrations)}")
