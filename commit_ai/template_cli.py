#!/usr/bin/env python3
"""
CLI para gerenciar templates de commit personalizados
"""

import click
import json
from pathlib import Path
from .templates import CommitTemplateManager
from .logger import logger


@click.group()
@click.pass_context
def template_cli(ctx):
    """🎨 Gerenciamento de templates de commit"""
    ctx.ensure_object(dict)
    try:
        ctx.obj['manager'] = CommitTemplateManager()
    except Exception as e:
        click.echo(click.style(f"❌ Erro ao inicializar gerenciador de templates: {e}", fg='red'))
        ctx.exit(1)


@template_cli.command('list')
@click.pass_context
def list_templates(ctx):
    """Lista todos os templates disponíveis"""
    manager = ctx.obj['manager']
    templates = manager.get_all_templates()
    
    click.echo(click.style("🎨 Templates de Commit Disponíveis:", fg='cyan', bold=True))
    click.echo()
    
    for commit_type, template in templates.items():
        click.echo(click.style(f"📝 {commit_type.upper()}", fg='green', bold=True))
        click.echo(f"   Descrição: {template['description']}")
        click.echo(f"   Padrão: {template['pattern']}")
        
        if template['examples']:
            click.echo("   Exemplos:")
            for example in template['examples'][:3]:  # Mostrar até 3 exemplos
                click.echo(f"   • {example}")
        
        click.echo()


@template_cli.command('show')
@click.argument('type')
@click.pass_context
def show_template(ctx, type):
    """Mostra detalhes de um template específico"""
    manager = ctx.obj['manager']
    template = manager.get_template(type)
    
    if not template:
        click.echo(click.style(f"❌ Template '{type}' não encontrado", fg='red'))
        return
    
    click.echo(click.style(f"📝 Template: {type.upper()}", fg='cyan', bold=True))
    click.echo(f"Descrição: {template['description']}")
    click.echo(f"Padrão: {click.style(template['pattern'], fg='yellow')}")
    
    if template['examples']:
        click.echo("\nExemplos:")
        for i, example in enumerate(template['examples'], 1):
            click.echo(f"  {i}. {example}")


@template_cli.command('add')
@click.argument('type')
@click.option('--pattern', '-p', required=True, help='Padrão do template (ex: "feat({scope}): {description}")')
@click.option('--description', '-d', required=True, help='Descrição do tipo de commit')
@click.option('--example', '-e', multiple=True, help='Exemplos de uso (pode repetir)')
@click.pass_context
def add_template(ctx, type, pattern, description, example):
    """Adiciona um novo template personalizado"""
    manager = ctx.obj['manager']
    
    examples = list(example) if example else []
    success = manager.add_template(type, pattern, description, examples)
    
    if success:
        click.echo(click.style(f"✅ Template '{type}' adicionado com sucesso!", fg='green'))
        
        # Mostrar o template adicionado
        click.echo("\nTemplate criado:")
        click.echo(f"  Tipo: {type}")
        click.echo(f"  Padrão: {pattern}")
        click.echo(f"  Descrição: {description}")
        if examples:
            click.echo("  Exemplos:")
            for ex in examples:
                click.echo(f"  • {ex}")
    else:
        click.echo(click.style(f"❌ Erro ao adicionar template '{type}'", fg='red'))


@template_cli.command('remove')
@click.argument('type')
@click.confirmation_option(prompt='Tem certeza que deseja remover este template?')
@click.pass_context
def remove_template(ctx, type):
    """Remove um template personalizado"""
    manager = ctx.obj['manager']
    
    success = manager.remove_template(type)
    
    if success:
        click.echo(click.style(f"✅ Template '{type}' removido com sucesso!", fg='green'))
    else:
        click.echo(click.style(f"❌ Erro ao remover template '{type}' (pode ser template padrão)", fg='red'))


@template_cli.command('suggest')
@click.option('--diff-file', type=click.Path(exists=True), help='Arquivo contendo o diff para análise')
@click.pass_context
def suggest_type(ctx, diff_file):
    """Sugere tipo de commit baseado no diff"""
    manager = ctx.obj['manager']
    
    if diff_file:
        try:
            with open(diff_file, 'r', encoding='utf-8') as f:
                diff_text = f.read()
        except Exception as e:
            click.echo(click.style(f"❌ Erro ao ler arquivo: {e}", fg='red'))
            return
    else:
        click.echo("Digite ou cole o diff do Git (Ctrl+C para finalizar):")
        diff_lines = []
        try:
            while True:
                line = input()
                diff_lines.append(line)
        except (EOFError, KeyboardInterrupt):
            pass
        diff_text = '\n'.join(diff_lines)
    
    if not diff_text.strip():
        click.echo(click.style("❌ Diff vazio fornecido", fg='red'))
        return
    
    suggested_type = manager.analyze_diff_and_suggest_type(diff_text)
    template = manager.get_template(suggested_type)
    
    click.echo(click.style(f"💡 Tipo sugerido: {suggested_type.upper()}", fg='cyan', bold=True))
    if template:
        click.echo(f"Descrição: {template['description']}")
        click.echo(f"Padrão: {template['pattern']}")
        
        if template['examples']:
            click.echo("\nExemplos:")
            for example in template['examples'][:2]:
                click.echo(f"  • {example}")


@template_cli.command('export')
@click.argument('output_file', type=click.Path())
@click.pass_context
def export_templates(ctx, output_file):
    """Exporta templates para um arquivo JSON"""
    manager = ctx.obj['manager']
    
    success = manager.export_templates(output_file)
    
    if success:
        click.echo(click.style(f"✅ Templates exportados para: {output_file}", fg='green'))
    else:
        click.echo(click.style(f"❌ Erro ao exportar templates", fg='red'))


@template_cli.command('import')
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--merge/--replace', default=True, help='Mesclar com existentes ou substituir')
@click.pass_context
def import_templates(ctx, input_file, merge):
    """Importa templates de um arquivo JSON"""
    manager = ctx.obj['manager']
    
    success = manager.import_templates(input_file, merge)
    
    if success:
        action = "mesclados" if merge else "substituídos"
        click.echo(click.style(f"✅ Templates {action} com sucesso!", fg='green'))
    else:
        click.echo(click.style(f"❌ Erro ao importar templates", fg='red'))


@template_cli.command('reset')
@click.confirmation_option(prompt='Tem certeza que deseja resetar todos os templates para os padrões?')
@click.pass_context
def reset_templates(ctx):
    """Reseta todos os templates para os padrões originais"""
    manager = ctx.obj['manager']
    
    success = manager.reset_to_defaults()
    
    if success:
        click.echo(click.style("✅ Templates resetados para padrões originais!", fg='green'))
    else:
        click.echo(click.style("❌ Erro ao resetar templates", fg='red'))


@template_cli.command('generate')
@click.argument('type')
@click.argument('description')
@click.option('--scope', '-s', help='Escopo da mudança (opcional)')
@click.pass_context
def generate_message(ctx, type, description, scope):
    """Gera uma mensagem de commit usando um template"""
    manager = ctx.obj['manager']
    
    message = manager.generate_message_with_template(type, description, scope)
    
    click.echo(click.style("📝 Mensagem de commit gerada:", fg='cyan', bold=True))
    click.echo(click.style(message, fg='yellow', bold=True))


if __name__ == '__main__':
    template_cli()
