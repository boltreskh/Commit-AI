#!/usr/bin/env python3
"""
CLI para gerenciamento de Git Hooks do Commit-AI
"""

import click
from pathlib import Path
from .git_hooks import GitHooksManager
from .logger import logger


@click.group()
@click.pass_context
def hooks_cli(ctx):
    """🔗 Gerenciamento de Git Hooks automáticos"""
    ctx.ensure_object(dict)
    try:
        ctx.obj['manager'] = GitHooksManager()
    except Exception as e:
        click.echo(click.style(f"[ERROR] Erro ao inicializar gerenciador de hooks: {e}", fg='red'))
        ctx.exit(1)


@hooks_cli.command('install')
@click.option('--hook', multiple=True, 
              type=click.Choice(['pre-commit', 'commit-msg', 'post-commit']),
              help='Hooks específicos para instalar (pode repetir)')
@click.option('--all', 'install_all', is_flag=True, default=True,
              help='Instalar todos os hooks disponíveis')
@click.pass_context
def install_hooks(ctx, hook, install_all):
    """Instala Git Hooks automáticos"""
    manager = ctx.obj['manager']
    
    hooks_to_install = list(hook) if hook else None
    
    click.echo(click.style("[INFO] Instalando Git Hooks...", fg='yellow'))
    
    if manager.install_hooks(hooks_to_install):
        click.echo(click.style("[OK] Hooks instalados com sucesso!", fg='green'))
        
        # Mostrar status
        status = manager.list_installed_hooks()
        click.echo("\n[INFO] Status dos hooks:")
        for hook_name, installed in status.items():
            icon = "[OK]" if installed else "[--]"
            color = 'green' if installed else 'red'
            click.echo(f"  {click.style(icon, fg=color)} {hook_name}")
            
    else:
        click.echo(click.style("[ERROR] Falha na instalação de alguns hooks", fg='red'))


@hooks_cli.command('uninstall')
@click.option('--hook', multiple=True,
              type=click.Choice(['pre-commit', 'commit-msg', 'post-commit']),
              help='Hooks específicos para remover')
@click.option('--all', 'uninstall_all', is_flag=True,
              help='Remover todos os hooks')
@click.confirmation_option(prompt='Tem certeza que deseja remover os hooks?')
@click.pass_context
def uninstall_hooks(ctx, hook, uninstall_all):
    """Remove Git Hooks instalados"""
    manager = ctx.obj['manager']
    
    hooks_to_remove = list(hook) if hook else (None if uninstall_all else [])
    
    if not hooks_to_remove and not uninstall_all:
        click.echo(click.style("[ERROR] Especifique --hook ou --all", fg='red'))
        return
    
    click.echo(click.style("[INFO] Removendo Git Hooks...", fg='yellow'))
    
    if manager.uninstall_hooks(hooks_to_remove):
        click.echo(click.style("[OK] Hooks removidos com sucesso!", fg='green'))
    else:
        click.echo(click.style("[ERROR] Falha na remoção de alguns hooks", fg='red'))


@hooks_cli.command('status')
@click.pass_context
def show_status(ctx):
    """Mostra status dos Git Hooks"""
    manager = ctx.obj['manager']
    
    click.echo(click.style("[INFO] Status dos Git Hooks:", fg='cyan', bold=True))
    
    # Status de instalação
    status = manager.list_installed_hooks()
    click.echo("\n[INFO] Hooks instalados:")
    for hook_name, installed in status.items():
        if installed:
            click.echo(f"  [OK] {hook_name}")
        else:
            click.echo(f"  [--] {hook_name} (não instalado)")
    
    # Saúde dos hooks
    health = manager.check_hooks_health()
    click.echo("\n[INFO] Saúde dos hooks:")
    for hook_name, health_status in health.items():
        if health_status == "Funcionando":
            click.echo(f"  [OK] {hook_name}: {health_status}")
        elif health_status == "Não instalado":
            click.echo(f"  [--] {hook_name}: {health_status}")
        else:
            click.echo(f"  [WARN] {hook_name}: {health_status}")


@hooks_cli.command('test')
@click.argument('hook_name', type=click.Choice(['pre-commit', 'commit-msg', 'post-commit']))
@click.pass_context
def test_hook(ctx, hook_name):
    """Testa um hook específico"""
    manager = ctx.obj['manager']
    
    # Verificar se hook está instalado
    status = manager.list_installed_hooks()
    if not status.get(hook_name, False):
        click.echo(click.style(f"[ERROR] Hook {hook_name} não está instalado", fg='red'))
        return
    
    click.echo(click.style(f"[INFO] Testando hook {hook_name}...", fg='yellow'))
    
    try:
        from .git_hooks import PreCommitHook, CommitMsgHook, PostCommitHook
        
        if hook_name == 'pre-commit':
            hook = PreCommitHook()
            result = hook.run()
        elif hook_name == 'commit-msg':
            # Criar arquivo temporário para teste
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                f.write("feat: test commit message")
                temp_file = f.name
            
            hook = CommitMsgHook()
            result = hook.run(temp_file)
            
            # Limpar arquivo temporário
            Path(temp_file).unlink()
            
        elif hook_name == 'post-commit':
            hook = PostCommitHook()
            result = hook.run()
        
        if result == 0:
            click.echo(click.style(f"[OK] Hook {hook_name} funcionou corretamente", fg='green'))
        else:
            click.echo(click.style(f"[ERROR] Hook {hook_name} retornou código {result}", fg='red'))
            
    except Exception as e:
        click.echo(click.style(f"[ERROR] Erro ao testar hook: {e}", fg='red'))


@hooks_cli.command('config')
@click.option('--enable/--disable', default=None, help='Habilitar/desabilitar hooks')
@click.option('--auto-improve/--no-auto-improve', default=None, 
              help='Auto-melhoria de mensagens')
@click.pass_context
def configure_hooks(ctx, enable, auto_improve):
    """Configura comportamento dos hooks"""
    from .config_manager import ConfigManager
    config_manager = ConfigManager()
    
    changes_made = False
    
    if enable is not None:
        config_manager.set('hooks_enabled', enable)
        status = "habilitados" if enable else "desabilitados"
        click.echo(click.style(f"[OK] Hooks {status}", fg='green'))
        changes_made = True
    
    if auto_improve is not None:
        config_manager.set('auto_improve_messages', auto_improve)
        status = "habilitada" if auto_improve else "desabilitada"
        click.echo(click.style(f"[OK] Auto-melhoria {status}", fg='green'))
        changes_made = True
    
    if not changes_made:
        # Mostrar configurações atuais
        hooks_enabled = config_manager.get('hooks_enabled', True)
        auto_improve_enabled = config_manager.get('auto_improve_messages', False)
        
        click.echo(click.style("[INFO] Configurações atuais:", fg='cyan', bold=True))
        click.echo(f"  Hooks habilitados: {hooks_enabled}")
        click.echo(f"  Auto-melhoria: {auto_improve_enabled}")


@hooks_cli.command('logs')
@click.option('--lines', '-n', default=10, help='Número de linhas do log')
@click.pass_context
def show_logs(ctx, lines):
    """Mostra logs dos hooks"""
    import subprocess
    
    try:
        # Filtrar logs relacionados aos hooks
        result = subprocess.run(
            ['tail', '-n', str(lines * 5)],  # Pegar mais linhas para filtrar
            input=open(Path.home() / '.commit-ai' / 'logs' / 'commit-ai.log').read(),
            text=True, capture_output=True
        )
        
        log_lines = result.stdout.split('\n')
        hook_logs = [line for line in log_lines if 'hook' in line.lower()][-lines:]
        
        if hook_logs:
            click.echo(click.style("[INFO] Logs recentes dos hooks:", fg='cyan', bold=True))
            for line in hook_logs:
                if '[ERROR]' in line:
                    click.echo(click.style(line, fg='red'))
                elif '[WARN]' in line:
                    click.echo(click.style(line, fg='yellow'))
                else:
                    click.echo(line)
        else:
            click.echo(click.style("[INFO] Nenhum log de hook encontrado", fg='yellow'))
            
    except Exception as e:
        click.echo(click.style(f"[ERROR] Erro ao ler logs: {e}", fg='red'))


if __name__ == '__main__':
    hooks_cli()
