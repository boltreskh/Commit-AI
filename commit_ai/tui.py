#!/usr/bin/env python3
"""
Sistema de Terminal User Interface (TUI) interativa para o Commit-AI v1.4.0

Proporciona uma interface visual rica no terminal para seleção e configuração
de commits de forma intuitiva e profissional.
"""

try:
    import rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich.layout import Layout
    from rich.live import Live
    from rich.align import Align
    TUI_AVAILABLE = True
except ImportError:
    TUI_AVAILABLE = False

import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

from .git_handler import GitHandler
from .ai_service import AIService
from .config_manager import ConfigManager
from .templates import CommitTemplateManager
from .logger import logger


@dataclass
class CommitOption:
    """Opção de commit na interface"""
    message: str
    type: str
    confidence: float
    provider: str
    template: str
    preview: str


class CommitTUI:
    """Interface de usuário terminal interativa para commits"""
    
    def __init__(self):
        if not TUI_AVAILABLE:
            raise ImportError(
                "Rich library não está instalada. "
                "Execute: pip install rich>=10.0.0"
            )
        
        self.console = Console()
        self.config_manager = ConfigManager()
        self.git_handler = GitHandler()
        self.template_manager = CommitTemplateManager()
        
        # Configurações da TUI
        self.theme = self.config_manager.get('tui_theme', 'default')
        self.show_diff = self.config_manager.get('tui_show_diff', True)
        self.auto_preview = self.config_manager.get('tui_auto_preview', True)
        
        # Estado da aplicação
        self.current_diff = ""
        self.commit_options = []
        self.selected_option = 0
        
    def show_welcome(self) -> None:
        """Exibe tela de boas-vindas"""
        welcome_panel = Panel.fit(
            "[bold blue]🤖 Commit-AI v1.4.0[/bold blue]\n\n"
            "[green]Interface Terminal Interativa[/green]\n"
            "[dim]Geração inteligente de commits com IA[/dim]",
            title="[bold]Bem-vindo![/bold]",
            border_style="blue"
        )
        
        self.console.print(Align.center(welcome_panel))
        time.sleep(1)
    
    def check_repository_status(self) -> bool:
        """Verifica status do repositório"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Verificando repositório Git...", total=None)
            
            try:
                if not self.git_handler.is_git_repo():
                    self.console.print("[red]❌ Não é um repositório Git![/red]")
                    return False
                
                progress.update(task, description="Verificando alterações...")
                
                if not self.git_handler.has_staged_changes():
                    self.console.print("[yellow]⚠️  Nenhuma alteração no staging area![/yellow]")
                    self.console.print("Execute [bold]git add .[/bold] para adicionar arquivos.")
                    return False
                
                progress.update(task, description="Obtendo diff...")
                self.current_diff = self.git_handler.get_staged_diff()
                
                return True
                
            except Exception as e:
                self.console.print(f"[red]❌ Erro: {e}[/red]")
                return False
    
    def show_diff_preview(self) -> None:
        """Mostra preview do diff com syntax highlighting"""
        if not self.show_diff or not self.current_diff:
            return
        
        # Limitar tamanho do diff para exibição
        diff_lines = self.current_diff.split('\n')
        if len(diff_lines) > 20:
            diff_preview = '\n'.join(diff_lines[:20]) + "\n... (truncado)"
        else:
            diff_preview = self.current_diff
        
        syntax = Syntax(
            diff_preview,
            "diff",
            theme="monokai",
            line_numbers=True,
            word_wrap=True
        )
        
        diff_panel = Panel(
            syntax,
            title="[bold]📋 Alterações (git diff --cached)[/bold]",
            border_style="yellow",
            expand=False
        )
        
        self.console.print(diff_panel)
    
    def generate_commit_options(self) -> List[CommitOption]:
        """Gera múltiplas opções de commit usando diferentes providers"""
        options = []
        
        providers = ['openai', 'gemini', 'claude']
        available_providers = [p for p in providers if AIService.is_provider_available(p)]
        
        templates = ['conventional', 'angular', 'gitmoji']
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            total_combinations = len(available_providers) * len(templates)
            task = progress.add_task("Gerando opções de commit...", total=total_combinations)
            
            for provider in available_providers:
                for template_name in templates:
                    try:
                        progress.update(
                            task, 
                            description=f"Gerando com {provider} + {template_name}...",
                            advance=1
                        )
                        
                        # Configurar AI service
                        ai_service = AIService(
                            provider=provider,
                            model=self.config_manager.get(f'{provider}_model')
                        )
                        
                        # Configurar template
                        template = self.template_manager.get_template(template_name)
                        
                        # Gerar mensagem
                        message = ai_service.generate_commit_message(
                            self.current_diff,
                            template=template
                        )
                        
                        # Analisar tipo e confiança
                        commit_type, confidence = self.template_manager.analyze_diff_and_suggest_type(
                            self.current_diff
                        )
                        
                        # Criar preview
                        preview = self._create_commit_preview(message, provider, template_name)
                        
                        option = CommitOption(
                            message=message.strip(),
                            type=commit_type,
                            confidence=confidence,
                            provider=provider,
                            template=template_name,
                            preview=preview
                        )
                        
                        options.append(option)
                        
                    except Exception as e:
                        logger.warning(f"Erro ao gerar opção {provider}+{template_name}: {e}")
                        continue
        
        # Ordenar por confiança
        options.sort(key=lambda x: x.confidence, reverse=True)
        return options[:6]  # Máximo 6 opções
    
    def _create_commit_preview(self, message: str, provider: str, template: str) -> str:
        """Cria preview formatado da opção de commit"""
        lines = message.split('\n')
        title = lines[0] if lines else message
        
        preview = f"[bold]{title}[/bold]\n"
        if len(lines) > 1:
            preview += f"[dim]{lines[1][:60]}...[/dim]\n"
        
        preview += f"[blue]Provider:[/blue] {provider.upper()}\n"
        preview += f"[green]Template:[/green] {template}\n"
        
        return preview
    
    def show_commit_options(self) -> Optional[CommitOption]:
        """Mostra opções de commit para seleção"""
        if not self.commit_options:
            self.console.print("[red]❌ Nenhuma opção de commit gerada![/red]")
            return None
        
        while True:
            # Criar tabela de opções
            table = Table(
                title="[bold]🎯 Opções de Commit Geradas[/bold]",
                show_header=True,
                header_style="bold blue"
            )
            
            table.add_column("Nº", style="dim", width=3)
            table.add_column("Mensagem", style="white", width=50)
            table.add_column("Tipo", style="green", width=12)
            table.add_column("Confiança", style="yellow", width=10)
            table.add_column("Provider", style="blue", width=10)
            table.add_column("Template", style="magenta", width=12)
            
            for i, option in enumerate(self.commit_options):
                style = "bold white" if i == self.selected_option else "dim"
                
                # Truncar mensagem para exibição
                display_msg = option.message[:47] + "..." if len(option.message) > 50 else option.message
                
                table.add_row(
                    str(i + 1),
                    display_msg,
                    option.type,
                    f"{option.confidence:.1%}",
                    option.provider.upper(),
                    option.template,
                    style=style
                )
            
            self.console.print(table)
            
            # Mostrar preview da opção selecionada
            if self.auto_preview:
                self.show_selected_preview()
            
            # Menu de opções
            self.console.print("\n[bold]Opções:[/bold]")
            self.console.print("• [bold]1-6[/bold] - Selecionar opção")
            self.console.print("• [bold]p[/bold] - Preview detalhado")
            self.console.print("• [bold]r[/bold] - Regenerar opções")
            self.console.print("• [bold]c[/bold] - Commit customizado")
            self.console.print("• [bold]q[/bold] - Sair")
            
            choice = Prompt.ask(
                "\n[bold green]Sua escolha[/bold green]",
                choices=["1", "2", "3", "4", "5", "6", "p", "r", "c", "q"],
                default="1"
            )
            
            if choice == "q":
                return None
            elif choice == "r":
                self.console.print("[yellow]🔄 Regenerando opções...[/yellow]")
                self.commit_options = self.generate_commit_options()
                continue
            elif choice == "p":
                self.show_detailed_preview()
                continue
            elif choice == "c":
                return self.custom_commit_flow()
            else:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(self.commit_options):
                        return self.commit_options[index]
                    else:
                        self.console.print("[red]Opção inválida![/red]")
                except ValueError:
                    self.console.print("[red]Entrada inválida![/red]")
    
    def show_selected_preview(self) -> None:
        """Mostra preview da opção atualmente selecionada"""
        if not self.commit_options:
            return
        
        option = self.commit_options[self.selected_option]
        
        preview_panel = Panel(
            option.preview,
            title="[bold]👁️  Preview da Opção Selecionada[/bold]",
            border_style="green",
            expand=False
        )
        
        self.console.print(preview_panel)
    
    def show_detailed_preview(self) -> None:
        """Mostra preview detalhado de uma opção específica"""
        choice = Prompt.ask(
            "Número da opção para preview detalhado",
            choices=[str(i+1) for i in range(len(self.commit_options))],
            default="1"
        )
        
        index = int(choice) - 1
        option = self.commit_options[index]
        
        # Criar preview completo
        preview_content = f"""[bold blue]Provider:[/bold blue] {option.provider.upper()}
[bold green]Template:[/bold green] {option.template}
[bold yellow]Tipo:[/bold yellow] {option.type}
[bold red]Confiança:[/bold red] {option.confidence:.1%}

[bold white]Mensagem completa:[/bold white]
{option.message}

[bold cyan]Comando que será executado:[/bold cyan]
git commit -m "{option.message}" """
        
        detailed_panel = Panel(
            preview_content,
            title=f"[bold]📋 Preview Detalhado - Opção {choice}[/bold]",
            border_style="cyan",
            expand=False
        )
        
        self.console.print(detailed_panel)
        
        # Confirmar se deseja usar esta opção
        if Confirm.ask("Usar esta opção para commit?"):
            self.execute_commit(option)
    
    def custom_commit_flow(self) -> Optional[CommitOption]:
        """Fluxo para criar commit customizado"""
        self.console.print("\n[bold]✏️  Commit Customizado[/bold]")
        
        # Selecionar provider
        providers = [p for p in ['openai', 'gemini', 'claude'] if AIService.is_provider_available(p)]
        if not providers:
            self.console.print("[red]Nenhum provider disponível![/red]")
            return None
        
        provider = Prompt.ask(
            "Provider de IA",
            choices=providers,
            default=providers[0]
        )
        
        # Selecionar template
        templates = list(self.template_manager.list_templates().keys())
        template_name = Prompt.ask(
            "Template",
            choices=templates,
            default="conventional"
        )
        
        # Configurações avançadas
        temperature = Prompt.ask(
            "Criatividade (0.0-1.0)",
            default="0.3"
        )
        
        try:
            # Gerar commit customizado
            ai_service = AIService(provider=provider)
            template = self.template_manager.get_template(template_name)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("Gerando commit customizado..."),
                console=self.console
            ) as progress:
                progress.add_task("Processando...", total=None)
                
                message = ai_service.generate_commit_message(
                    self.current_diff,
                    template=template,
                    temperature=float(temperature)
                )
            
            # Analisar resultado
            commit_type, confidence = self.template_manager.analyze_diff_and_suggest_type(
                self.current_diff
            )
            
            preview = self._create_commit_preview(message, provider, template_name)
            
            return CommitOption(
                message=message.strip(),
                type=commit_type,
                confidence=confidence,
                provider=provider,
                template=template_name,
                preview=preview
            )
            
        except Exception as e:
            self.console.print(f"[red]Erro ao gerar commit customizado: {e}[/red]")
            return None
    
    def execute_commit(self, option: CommitOption) -> bool:
        """Executa o commit com a opção selecionada"""
        # Confirmação final
        commit_panel = Panel(
            f"[bold white]Mensagem:[/bold white]\n{option.message}\n\n"
            f"[bold blue]Provider:[/bold blue] {option.provider}\n"
            f"[bold green]Template:[/bold green] {option.template}\n"
            f"[bold yellow]Confiança:[/bold yellow] {option.confidence:.1%}",
            title="[bold red]⚠️  Confirmação de Commit[/bold red]",
            border_style="red"
        )
        
        self.console.print(commit_panel)
        
        if not Confirm.ask("[bold]Confirma o commit?[/bold]", default=True):
            self.console.print("[yellow]Commit cancelado.[/yellow]")
            return False
        
        # Executar commit
        with Progress(
            SpinnerColumn(),
            TextColumn("Executando commit..."),
            console=self.console
        ) as progress:
            progress.add_task("Processando...", total=None)
            
            try:
                success = self.git_handler.commit(option.message)
                
                if success:
                    self.console.print("[bold green]✅ Commit realizado com sucesso![/bold green]")
                    
                    # Mostrar informações do commit
                    commit_info = self.git_handler.get_last_commit_info()
                    if commit_info:
                        info_panel = Panel(
                            f"[bold]Hash:[/bold] {commit_info.get('hash', 'N/A')}\n"
                            f"[bold]Author:[/bold] {commit_info.get('author', 'N/A')}\n"
                            f"[bold]Date:[/bold] {commit_info.get('date', 'N/A')}",
                            title="[bold]📊 Informações do Commit[/bold]",
                            border_style="green"
                        )
                        self.console.print(info_panel)
                    
                    return True
                else:
                    self.console.print("[bold red]❌ Falha ao realizar commit![/bold red]")
                    return False
                    
            except Exception as e:
                self.console.print(f"[bold red]❌ Erro: {e}[/bold red]")
                return False
    
    def run_interactive_mode(self) -> bool:
        """Executa o modo interativo completo"""
        try:
            # Tela de boas-vindas
            self.show_welcome()
            
            # Verificar repositório
            if not self.check_repository_status():
                return False
            
            # Mostrar diff
            self.show_diff_preview()
            
            # Gerar opções de commit
            self.console.print("\n[bold yellow]🔄 Gerando opções de commit...[/bold yellow]")
            self.commit_options = self.generate_commit_options()
            
            if not self.commit_options:
                self.console.print("[red]❌ Não foi possível gerar opções de commit![/red]")
                return False
            
            # Seleção interativa
            selected_option = self.show_commit_options()
            if not selected_option:
                self.console.print("[yellow]Operação cancelada.[/yellow]")
                return False
            
            # Executar commit
            return self.execute_commit(selected_option)
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operação cancelada pelo usuário.[/yellow]")
            return False
        except Exception as e:
            self.console.print(f"\n[red]Erro inesperado: {e}[/red]")
            logger.error(f"Erro na TUI: {e}", exc_info=True)
            return False


def run_tui_mode() -> bool:
    """Função principal para executar modo TUI"""
    if not TUI_AVAILABLE:
        print("❌ Rich library não está instalada.")
        print("Execute: pip install rich>=10.0.0")
        return False
    
    try:
        tui = CommitTUI()
        return tui.run_interactive_mode()
    except Exception as e:
        print(f"❌ Erro ao inicializar TUI: {e}")
        return False


if __name__ == "__main__":
    run_tui_mode()
