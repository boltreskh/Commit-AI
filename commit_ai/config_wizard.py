#!/usr/bin/env python3
"""
Wizard de Configuração Inicial do Commit-AI v1.4.0

Interface interativa para configuração inicial do sistema,
guiando o usuário através de todas as opções disponíveis.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .config_manager import ConfigManager
from .ai_service import AIService
from .templates import CommitTemplateManager
from .logger import logger


class ConfigurationWizard:
    """Wizard interativo para configuração inicial"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.console = Console() if RICH_AVAILABLE else None
        self.configuration = {}
        
    def run(self) -> bool:
        """Executa o wizard completo"""
        try:
            if not RICH_AVAILABLE:
                return self._run_simple_wizard()
            else:
                return self._run_rich_wizard()
        except KeyboardInterrupt:
            self._print_message("\n[yellow]Configuração cancelada pelo usuário.[/yellow]")
            return False
        except Exception as e:
            self._print_message(f"[red]Erro durante configuração: {e}[/red]")
            logger.error(f"Erro no wizard: {e}", exc_info=True)
            return False
    
    def _run_rich_wizard(self) -> bool:
        """Executa wizard com interface Rich"""
        # Tela de boas-vindas
        self._show_welcome()
        
        # Verificar configuração existente
        if self._check_existing_config():
            return True
        
        # Etapas do wizard
        steps = [
            ("🤖 Provedores de IA", self._configure_ai_providers),
            ("📋 Templates", self._configure_templates),
            ("🔗 Git Hooks", self._configure_hooks),
            ("🔌 Plugins", self._configure_plugins),
            ("⚙️  Configurações Gerais", self._configure_general),
            ("📊 Analytics", self._configure_analytics),
            ("🎨 Interface", self._configure_interface)
        ]
        
        for step_name, step_func in steps:
            self.console.print(f"\n{step_name}", style="bold blue")
            self.console.print("-" * 50)
            
            try:
                if not step_func():
                    self._print_message("[yellow]Etapa cancelada. Continuando...[/yellow]")
            except Exception as e:
                self._print_message(f"[red]Erro na etapa {step_name}: {e}[/red]")
                continue
        
        # Salvar configurações
        return self._save_configuration()
    
    def _run_simple_wizard(self) -> bool:
        """Executa wizard sem Rich (fallback)"""
        print("=" * 60)
        print("🤖 COMMIT-AI - WIZARD DE CONFIGURAÇÃO")
        print("=" * 60)
        print("Rich library não disponível. Usando interface simplificada.")
        print("Execute 'pip install rich' para interface aprimorada.\n")
        
        # Configuração básica
        try:
            # API Key
            print("1. CONFIGURAÇÃO DE API:")
            api_choice = input("Escolha API (1-OpenAI, 2-Gemini, 3-Claude, 4-Ollama): ").strip()
            
            api_map = {'1': 'openai', '2': 'gemini', '3': 'claude', '4': 'ollama'}
            selected_api = api_map.get(api_choice, 'openai')
            
            if selected_api != 'ollama':
                api_key = input(f"API Key para {selected_api}: ").strip()
                if api_key:
                    self.configuration[f'{selected_api}_api_key'] = api_key
            
            self.configuration['default_api'] = selected_api
            
            # Template padrão
            print("\n2. TEMPLATE PADRÃO:")
            template_choice = input("Template (1-conventional, 2-angular, 3-gitmoji): ").strip()
            template_map = {'1': 'conventional', '2': 'angular', '3': 'gitmoji'}
            self.configuration['default_template'] = template_map.get(template_choice, 'conventional')
            
            # Salvar
            for key, value in self.configuration.items():
                self.config_manager.set(key, value)
            
            print("\n✅ Configuração básica salva!")
            return True
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def _show_welcome(self) -> None:
        """Mostra tela de boas-vindas"""
        welcome_text = """[bold blue]🤖 Commit-AI v1.4.0[/bold blue]
[green]Wizard de Configuração Inicial[/green]

Este assistente irá guiá-lo através da configuração inicial do Commit-AI,
incluindo provedores de IA, templates, hooks e outras preferências.

[dim]Pressione Ctrl+C a qualquer momento para cancelar.[/dim]"""
        
        welcome_panel = Panel(
            welcome_text,
            title="[bold]Bem-vindo![/bold]",
            border_style="blue",
            expand=False
        )
        
        self.console.print(welcome_panel)
        
        if not Confirm.ask("\nDeseja continuar com a configuração?", default=True):
            raise KeyboardInterrupt()
    
    def _check_existing_config(self) -> bool:
        """Verifica se já existe configuração"""
        existing_config = self.config_manager.config
        
        if existing_config and len(existing_config) > 2:  # Mais que configurações padrão
            self.console.print(Panel(
                "[yellow]Configuração existente encontrada![/yellow]\n\n"
                "Você já tem o Commit-AI configurado. Suas configurações atuais:\n"
                + self._format_existing_config(existing_config),
                title="[bold]Configuração Existente[/bold]",
                border_style="yellow"
            ))
            
            choice = Prompt.ask(
                "O que deseja fazer?",
                choices=["manter", "reconfigurar", "sair"],
                default="manter"
            )
            
            if choice == "sair":
                return True
            elif choice == "manter":
                self.console.print("[green]Mantendo configuração existente.[/green]")
                return True
            # Se 'reconfigurar', continua com wizard
        
        return False
    
    def _format_existing_config(self, config: Dict[str, Any]) -> str:
        """Formata configuração existente para exibição"""
        important_keys = [
            'default_api', 'default_template', 'default_model',
            'hooks_enabled', 'auto_improve_messages', 'tui_theme'
        ]
        
        lines = []
        for key in important_keys:
            if key in config:
                value = config[key]
                if isinstance(value, bool):
                    value = "✅ Sim" if value else "❌ Não"
                lines.append(f"• {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(lines) if lines else "Configuração básica presente"
    
    def _configure_ai_providers(self) -> bool:
        """Configura provedores de IA"""
        self.console.print("Configuração dos provedores de IA disponíveis:\n")
        
        # Mostrar provedores disponíveis
        providers = AIService.get_supported_providers()
        
        table = Table(title="Provedores Disponíveis")
        table.add_column("Provider", style="cyan")
        table.add_column("Nome", style="white")
        table.add_column("Status", style="green")
        table.add_column("Modelos", style="dim")
        
        for provider, info in providers.items():
            available = AIService.is_provider_available(provider)
            status = "✅ Disponível" if available else "❌ Indisponível"
            models = ", ".join(info['models'][:3]) + "..." if len(info['models']) > 3 else ", ".join(info['models'])
            
            table.add_row(provider.upper(), info['name'], status, models)
        
        self.console.print(table)
        
        # Selecionar provider padrão
        available_providers = [p for p in providers.keys() if AIService.is_provider_available(p)]
        
        if not available_providers:
            self.console.print("[red]❌ Nenhum provider disponível! Configure API keys primeiro.[/red]")
            return False
        
        default_api = Prompt.ask(
            "Provider padrão",
            choices=available_providers,
            default=available_providers[0]
        )
        self.configuration['default_api'] = default_api
        
        # Configurar API key se necessário
        if default_api != 'ollama':
            current_key = os.getenv(f'{default_api.upper()}_API_KEY')
            if not current_key:
                api_key = Prompt.ask(
                    f"API Key para {default_api.upper()} (será salva no .env)",
                    password=True
                )
                if api_key:
                    self._save_api_key(default_api, api_key)
        
        # Configurar modelo padrão
        provider_info = providers[default_api]
        if provider_info['models']:
            default_model = Prompt.ask(
                f"Modelo padrão para {default_api}",
                choices=provider_info['models'],
                default=provider_info['default_model']
            )
            self.configuration[f'{default_api}_model'] = default_model
        
        return True
    
    def _configure_templates(self) -> bool:
        """Configura templates de commit"""
        self.console.print("Configuração de templates de commit:\n")
        
        template_manager = CommitTemplateManager()
        templates = template_manager.list_templates()
        
        # Mostrar templates disponíveis
        table = Table(title="Templates Disponíveis")
        table.add_column("Nome", style="cyan")
        table.add_column("Descrição", style="white")
        table.add_column("Formato", style="dim")
        
        for name, template in templates.items():
            table.add_row(
                name,
                template.get('description', 'N/A'),
                template.get('format', 'N/A')
            )
        
        self.console.print(table)
        
        # Selecionar template padrão
        default_template = Prompt.ask(
            "Template padrão",
            choices=list(templates.keys()),
            default="conventional"
        )
        self.configuration['default_template'] = default_template
        
        # Configurações avançadas de template
        if Confirm.ask("Configurar opções avançadas de templates?", default=False):
            self.configuration['auto_detect_type'] = Confirm.ask(
                "Auto-detectar tipo de commit baseado no diff?", 
                default=True
            )
            self.configuration['template_confidence_threshold'] = FloatPrompt.ask(
                "Limite de confiança para sugestões automáticas (0.0-1.0)",
                default=0.7
            )
        
        return True
    
    def _configure_hooks(self) -> bool:
        """Configura Git Hooks"""
        self.console.print("Configuração de Git Hooks automáticos:\n")
        
        self.console.print(Panel(
            "Os Git Hooks automatizam o workflow de commits:\n\n"
            "• [bold]Pre-commit:[/bold] Analisa alterações e sugere tipos\n"
            "• [bold]Commit-msg:[/bold] Valida e melhora mensagens\n"
            "• [bold]Post-commit:[/bold] Coleta analytics e métricas",
            title="[bold]Sobre Git Hooks[/bold]",
            border_style="green"
        ))
        
        # Habilitar hooks
        enable_hooks = Confirm.ask("Habilitar Git Hooks automáticos?", default=True)
        self.configuration['hooks_enabled'] = enable_hooks
        
        if enable_hooks:
            # Auto-instalação
            auto_install = Confirm.ask(
                "Instalar hooks automaticamente em novos repositórios?", 
                default=True
            )
            self.configuration['auto_install_hooks'] = auto_install
            
            # Auto-melhoria
            auto_improve = Confirm.ask(
                "Permitir melhoria automática de mensagens ruins?", 
                default=False
            )
            self.configuration['auto_improve_messages'] = auto_improve
            
            # Analytics
            collect_analytics = Confirm.ask(
                "Coletar analytics de commits (local)?", 
                default=True
            )
            self.configuration['hook_analytics'] = collect_analytics
        
        return True
    
    def _configure_plugins(self) -> bool:
        """Configura sistema de plugins"""
        self.console.print("Configuração do sistema de plugins:\n")
        
        self.console.print(Panel(
            "Plugins estendem as funcionalidades do Commit-AI:\n\n"
            "• [bold]AI Providers:[/bold] Novos serviços de IA\n"
            "• [bold]Templates:[/bold] Formatos customizados\n"
            "• [bold]Workflows:[/bold] Automações personalizadas\n"
            "• [bold]Integrações:[/bold] Conexões com serviços externos",
            title="[bold]Sistema de Plugins[/bold]",
            border_style="magenta"
        ))
        
        # Habilitar sistema de plugins
        enable_plugins = Confirm.ask("Habilitar sistema de plugins?", default=True)
        self.configuration['plugins_enabled'] = enable_plugins
        
        if enable_plugins:
            # Auto-carregamento
            auto_load = Confirm.ask(
                "Carregar plugins automaticamente na inicialização?", 
                default=True
            )
            self.configuration['auto_load_plugins'] = auto_load
            
            # Plugins confiáveis
            trust_user_plugins = Confirm.ask(
                "Permitir plugins de usuário (diretório ~/.commit-ai/plugins)?", 
                default=True
            )
            self.configuration['trust_user_plugins'] = trust_user_plugins
        
        return True
    
    def _configure_general(self) -> bool:
        """Configura opções gerais"""
        self.console.print("Configurações gerais do sistema:\n")
        
        # Modo padrão
        default_mode = Prompt.ask(
            "Modo padrão de operação",
            choices=["interactive", "preview", "auto"],
            default="interactive"
        )
        self.configuration['default_mode'] = default_mode
        
        # Parâmetros de IA
        temperature = FloatPrompt.ask(
            "Criatividade padrão das respostas (0.0-1.0)",
            default=0.3
        )
        self.configuration['temperature'] = temperature
        
        max_tokens = IntPrompt.ask(
            "Máximo de tokens para respostas",
            default=100
        )
        self.configuration['max_tokens'] = max_tokens
        
        # Cache
        enable_cache = Confirm.ask("Habilitar cache de respostas?", default=True)
        self.configuration['enable_cache'] = enable_cache
        
        if enable_cache:
            cache_hours = IntPrompt.ask(
                "Tempo de expiração do cache (horas)",
                default=24
            )
            self.configuration['cache_expiry_hours'] = cache_hours
        
        # Logs
        log_level = Prompt.ask(
            "Nível de log",
            choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            default="INFO"
        )
        self.configuration['log_level'] = log_level
        
        return True
    
    def _configure_analytics(self) -> bool:
        """Configura sistema de analytics"""
        self.console.print("Configuração de analytics e métricas:\n")
        
        self.console.print(Panel(
            "O sistema de analytics coleta métricas sobre seus commits:\n\n"
            "• Padrões de commits e produtividade\n"
            "• Performance dos diferentes providers\n"
            "• Insights colaborativos da equipe\n"
            "• [dim]Todos os dados permanecem locais[/dim]",
            title="[bold]Analytics[/bold]",
            border_style="yellow"
        ))
        
        # Habilitar analytics
        enable_analytics = Confirm.ask("Habilitar coleta de analytics?", default=True)
        self.configuration['analytics_enabled'] = enable_analytics
        
        if enable_analytics:
            # Retenção de dados
            retention_days = IntPrompt.ask(
                "Dias para manter dados históricos",
                default=90
            )
            self.configuration['analytics_retention_days'] = retention_days
            
            # Relatórios automáticos
            auto_reports = Confirm.ask(
                "Gerar relatórios semanais automáticos?", 
                default=False
            )
            self.configuration['auto_generate_reports'] = auto_reports
            
            # Insights da equipe
            team_insights = Confirm.ask(
                "Coletar insights colaborativos da equipe?", 
                default=True
            )
            self.configuration['collect_team_insights'] = team_insights
        
        return True
    
    def _configure_interface(self) -> bool:
        """Configura opções de interface"""
        self.console.print("Configuração da interface do usuário:\n")
        
        # TUI (se Rich disponível)
        if RICH_AVAILABLE:
            enable_tui = Confirm.ask("Usar interface rica (TUI) quando disponível?", default=True)
            self.configuration['enable_tui'] = enable_tui
            
            if enable_tui:
                # Tema
                theme = Prompt.ask(
                    "Tema da interface",
                    choices=["default", "dark", "light", "colorful"],
                    default="default"
                )
                self.configuration['tui_theme'] = theme
                
                # Preview automático
                auto_preview = Confirm.ask(
                    "Mostrar preview automático de opções?", 
                    default=True
                )
                self.configuration['tui_auto_preview'] = auto_preview
                
                # Mostrar diff
                show_diff = Confirm.ask(
                    "Mostrar diff das alterações na interface?", 
                    default=True
                )
                self.configuration['tui_show_diff'] = show_diff
        
        # Feedback visual
        use_colors = Confirm.ask("Usar cores nos outputs?", default=True)
        self.configuration['use_colors'] = use_colors
        
        # Modo verboso padrão
        default_verbose = Confirm.ask("Habilitar modo verboso por padrão?", default=False)
        self.configuration['default_verbose'] = default_verbose
        
        return True
    
    def _save_api_key(self, provider: str, api_key: str) -> None:
        """Salva API key no arquivo .env"""
        try:
            env_file = Path('.env')
            env_var = f'{provider.upper()}_API_KEY={api_key}\n'
            
            if env_file.exists():
                content = env_file.read_text()
                lines = content.split('\n')
                
                # Atualizar linha existente ou adicionar nova
                key_found = False
                for i, line in enumerate(lines):
                    if line.startswith(f'{provider.upper()}_API_KEY='):
                        lines[i] = env_var.rstrip()
                        key_found = True
                        break
                
                if not key_found:
                    lines.append(env_var.rstrip())
                
                env_file.write_text('\n'.join(lines))
            else:
                env_file.write_text(env_var)
            
            self.console.print(f"[green]API key salva em .env[/green]")
            
        except Exception as e:
            self.console.print(f"[red]Erro ao salvar API key: {e}[/red]")
    
    def _save_configuration(self) -> bool:
        """Salva todas as configurações"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Salvando configurações...", total=None)
                
                # Salvar cada configuração
                for key, value in self.configuration.items():
                    self.config_manager.set(key, value)
                
                progress.update(task, description="Configurações salvas!")
            
            # Resumo final
            self._show_configuration_summary()
            
            self.console.print(Panel(
                "[bold green]✅ Configuração concluída com sucesso![/bold green]\n\n"
                "O Commit-AI está pronto para uso. Execute:\n"
                "[bold cyan]commit-ai[/bold cyan] para gerar seu primeiro commit\n\n"
                "Para ajuda: [bold]commit-ai --help[/bold]",
                title="[bold]Configuração Completa[/bold]",
                border_style="green"
            ))
            
            return True
            
        except Exception as e:
            self.console.print(f"[red]Erro ao salvar configurações: {e}[/red]")
            return False
    
    def _show_configuration_summary(self) -> None:
        """Mostra resumo da configuração"""
        table = Table(title="Resumo da Configuração")
        table.add_column("Configuração", style="cyan")
        table.add_column("Valor", style="white")
        
        important_configs = [
            'default_api', 'default_template', 'hooks_enabled',
            'plugins_enabled', 'analytics_enabled', 'enable_tui'
        ]
        
        for key in important_configs:
            if key in self.configuration:
                value = self.configuration[key]
                if isinstance(value, bool):
                    value = "✅ Habilitado" if value else "❌ Desabilitado"
                table.add_row(key.replace('_', ' ').title(), str(value))
        
        self.console.print("\n")
        self.console.print(table)
    
    def _print_message(self, message: str) -> None:
        """Imprime mensagem (com ou sem Rich)"""
        if self.console:
            self.console.print(message)
        else:
            # Remover markup Rich para terminal simples
            import re
            clean_message = re.sub(r'\[/?\w+\]', '', message)
            print(clean_message)


def run_configuration_wizard() -> bool:
    """Função principal para executar wizard"""
    wizard = ConfigurationWizard()
    return wizard.run()


if __name__ == "__main__":
    success = run_configuration_wizard()
    sys.exit(0 if success else 1)
