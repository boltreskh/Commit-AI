#!/usr/bin/env python3
"""
Utilitário de linha de comando para gerenciar o cache do Commit-AI

Fornece comandos para visualizar, limpar e gerenciar o cache.
"""

import click
from pathlib import Path
from commit_ai.cache import CommitCache
from commit_ai.logger import logger


@click.group()
def cache_cli():
    """🗄️  Gerenciador de Cache do Commit-AI"""
    pass


@cache_cli.command()
def stats():
    """📊 Mostrar estatísticas do cache"""
    cache = CommitCache()
    stats_data = cache.stats()
    
    if 'error' in stats_data:
        click.echo(click.style(f"❌ Erro: {stats_data['error']}", fg='red'))
        return
    
    click.echo(click.style("📊 Estatísticas do Cache", fg='cyan', bold=True))
    click.echo(f"📁 Diretório: {stats_data['cache_dir']}")
    click.echo(f"📈 Total de entradas: {stats_data['total_entries']}")
    click.echo(f"⏰ Idade máxima: {stats_data['max_age_hours']:.1f} horas")
    
    provider_stats = stats_data.get('provider_stats', {})
    if provider_stats:
        click.echo("\n🤖 Entradas por provedor:")
        for provider, count in provider_stats.items():
            click.echo(f"  - {provider}: {count}")
    
    if stats_data.get('oldest_entry'):
        click.echo(f"\n📅 Entrada mais antiga: {stats_data['oldest_entry']}")
    
    if stats_data['total_entries'] == 0:
        click.echo(click.style("\n💡 Cache vazio - nenhuma entrada encontrada.", fg='yellow'))


@cache_cli.command()
@click.confirmation_option(prompt='Tem certeza que deseja limpar todo o cache?')
def clear():
    """🧹 Limpar todo o cache"""
    cache = CommitCache()
    
    try:
        old_stats = cache.stats()
        cache.clear_all()
        
        click.echo(click.style(
            f"✅ Cache limpo com sucesso! {old_stats['total_entries']} entradas removidas.", 
            fg='green'
        ))
    except Exception as e:
        click.echo(click.style(f"❌ Erro ao limpar cache: {e}", fg='red'))


@cache_cli.command()
def cleanup():
    """🕒 Remover entradas expiradas do cache"""
    cache = CommitCache()
    
    try:
        old_stats = cache.stats()
        cache.clear_expired()
        new_stats = cache.stats()
        
        removed = old_stats['total_entries'] - new_stats['total_entries']
        
        if removed > 0:
            click.echo(click.style(
                f"✅ Limpeza concluída! {removed} entradas expiradas removidas.",
                fg='green'
            ))
        else:
            click.echo(click.style("✨ Nenhuma entrada expirada encontrada.", fg='blue'))
    except Exception as e:
        click.echo(click.style(f"❌ Erro na limpeza: {e}", fg='red'))


@cache_cli.command()
@click.argument('hours', type=int)
def set_max_age(hours):
    """⏱️  Definir idade máxima do cache (em horas)"""
    if hours <= 0:
        click.echo(click.style("❌ Erro: Horas deve ser um número positivo.", fg='red'))
        return
    
    # Criar novo cache com a idade especificada
    cache = CommitCache(max_age_hours=hours)
    
    click.echo(click.style(
        f"✅ Idade máxima do cache definida para {hours} horas.",
        fg='green'
    ))
    
    # Mostrar estatísticas atualizadas
    stats_data = cache.stats()
    click.echo(f"📊 Total de entradas válidas: {stats_data['total_entries']}")


@cache_cli.command()
def info():
    """ℹ️  Informações detalhadas sobre o cache"""
    cache = CommitCache()
    cache_dir = Path.home() / '.commit-ai' / 'cache'
    
    click.echo(click.style("ℹ️  Informações do Cache", fg='cyan', bold=True))
    click.echo(f"📁 Diretório: {cache_dir}")
    click.echo(f"💾 Arquivo do banco: {cache_dir / 'cache.db'}")
    
    # Verificar se os arquivos existem
    db_file = cache_dir / 'cache.db'
    if db_file.exists():
        file_size = db_file.stat().st_size
        click.echo(f"📏 Tamanho do arquivo: {file_size:,} bytes")
    else:
        click.echo("⚠️  Arquivo de cache não encontrado")
    
    # Mostrar configurações
    click.echo(f"⏰ Idade máxima padrão: 24 horas")
    click.echo(f"🗃️  Formato: SQLite")
    click.echo(f"🔄 Cache automático: Habilitado por padrão")


if __name__ == '__main__':
    cache_cli()
