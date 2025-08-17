#!/usr/bin/env python3
"""
Commit-AI - Gerador de mensagens de commit usando IA

Este é o ponto de entrada principal da aplicação CLI.
"""

import os
import sys
import subprocess
from .version import VERSION
import click
from dotenv import load_dotenv
from .git_handler import GitHandler
from .ai_service import AIService
from .config_manager import ConfigManager
from .logger import logger

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o gerenciador de configurações
config_manager = ConfigManager()

@click.command()
@click.option('--api', 
              type=click.Choice(['openai', 'gemini'], case_sensitive=False),
              default=lambda: config_manager.get('default_api', 'openai'),
              help='Serviço de IA a ser usado')
@click.option('--model',
              default=lambda: config_manager.get('default_model', None),
              help='Modelo específico a ser usado (ex: gpt-4, gemini-pro)')
@click.option('--max-tokens',
              default=lambda: config_manager.get('max_tokens', 100),
              help='Número máximo de tokens para a resposta')
@click.option('--temperature',
              default=lambda: config_manager.get('temperature', 0.3),
              help='Criatividade da resposta (0.0-1.0)')
@click.option('--preview',
              is_flag=True,
              default=lambda: config_manager.get('preview_mode', False),
              help='Apenas visualizar a mensagem sem fazer o commit')
@click.option('--auto',
              is_flag=True,
              default=lambda: config_manager.get('auto_commit', False),
              help='Fazer commit automaticamente sem confirmação')
@click.option('--verbose', '-v',
              is_flag=True,
              help='Modo verboso - mais informações de debug')
@click.option('--no-cache',
              is_flag=True,
              help='Desabilitar cache - sempre fazer nova consulta à IA')
@click.option('--config',
              help='Definir configuração: --config key=value')
@click.option('--cache-stats',
              is_flag=True,
              help='Mostrar estatísticas do cache')
def main(api, model, max_tokens, temperature, preview, auto, verbose, no_cache, config, cache_stats):
    """
    🤖 Commit-AI - Gerador inteligente de mensagens de commit
    
    Gera mensagens de commit profissionais usando IA baseada nas suas alterações de código.
    
    Exemplos de uso:
        commit-ai                           # Usar configurações padrão
        commit-ai --api gemini              # Usar Google Gemini
        commit-ai --preview                 # Apenas visualizar a mensagem
        commit-ai --auto                    # Commit automático
        commit-ai --config api=gemini       # Definir configuração padrão
        commit-ai --verbose                 # Modo debug
        commit-ai --no-cache               # Desabilitar cache
        commit-ai --cache-stats            # Ver estatísticas do cache
    """
    
    try:
        # Configurar nível de logging
        if verbose:
            logger.set_level('DEBUG')
            logger.debug("Modo verbose ativado")
        
        # Mostrar estatísticas do cache se solicitado
        if cache_stats:
            from .cache import CommitCache
            cache = CommitCache()
            stats = cache.stats()
            
            click.echo(click.style("📊 Estatísticas do Cache:", fg='cyan', bold=True))
            click.echo(f"  📁 Diretório: {stats.get('cache_dir')}")
            click.echo(f"  📈 Total de entradas: {stats.get('total_entries', 0)}")
            click.echo(f"  ⏰ Idade máxima: {stats.get('max_age_hours', 24):.1f}h")
            
            provider_stats = stats.get('provider_stats', {})
            if provider_stats:
                click.echo("  🤖 Por provedor:")
                for provider, count in provider_stats.items():
                    click.echo(f"    - {provider}: {count}")
            
            if stats.get('oldest_entry'):
                click.echo(f"  📅 Entrada mais antiga: {stats['oldest_entry']}")
            
            return
        
        # Gerenciar configurações
        if config:
            try:
                key, value = config.split('=', 1)
                # Converter valores para tipos apropriados
                if value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                elif value.replace('.', '').isdigit():
                    value = float(value) if '.' in value else int(value)
                
                config_manager.set(key, value)
                logger.info(f"Configuração atualizada: {key} = {value}")
                click.echo(click.style(f"✅ Configuração salva: {key} = {value}", fg='green'))
                return
            except ValueError:
                logger.error(f"Formato de configuração inválido: {config}")
                click.echo(click.style("❌ Formato inválido. Use: --config chave=valor", fg='red'))
                sys.exit(1)
        
        logger.info(f"Iniciando Commit-AI v{VERSION}")
        logger.debug(f"Configurações: api={api}, model={model}, temperature={temperature}")
        
        # Validação de parâmetros
        try:
            temp_float = float(temperature)
            if not (0.0 <= temp_float <= 1.0):
                logger.error(f"Temperature inválida: {temperature}")
                click.echo(click.style("❌ Erro: Temperature deve estar entre 0.0 e 1.0", fg='red'))
                sys.exit(1)
            temperature = temp_float
        except (ValueError, TypeError):
            logger.error(f"Temperature inválida: {temperature}")
            click.echo(click.style("❌ Erro: Temperature deve ser um número", fg='red'))
            sys.exit(1)
        
        try:
            tokens_int = int(max_tokens)
            if tokens_int <= 0:
                logger.error(f"Max tokens inválido: {max_tokens}")
                click.echo(click.style("❌ Erro: max_tokens deve ser um número positivo", fg='red'))
                sys.exit(1)
            max_tokens = tokens_int
        except (ValueError, TypeError):
            logger.error(f"Max tokens inválido: {max_tokens}")
            click.echo(click.style("❌ Erro: max_tokens deve ser um número", fg='red'))
            sys.exit(1)
        # Verificar se estamos em um repositório Git
        logger.debug("Verificando repositório Git...")
        git_handler = GitHandler()
        if not git_handler.is_git_repo():
            logger.error("Não é um repositório Git")
            click.echo(click.style("❌ Erro: Este diretório não é um repositório Git.", fg='red'))
            sys.exit(1)
        
        logger.debug("Repositório Git detectado")
        
        # Verificar se há alterações para commit
        logger.debug("Verificando alterações staged...")
        diff_text = git_handler.get_staged_diff()
        if not diff_text.strip():
            logger.warning("Nenhuma alteração staged encontrada")
            click.echo(click.style("⚠️  Nenhuma alteração staged encontrada.", fg='yellow'))
            click.echo("Execute 'git add <arquivos>' antes de usar o commit-ai")
            sys.exit(1)
        
        logger.info("Alterações staged encontradas")
        logger.debug(f"Tamanho do diff: {len(diff_text)} caracteres")
        
        # Configurar o serviço de IA
        logger.debug(f"Configurando serviço de IA: {api}")
        use_cache = not no_cache
        logger.debug(f"Cache {'habilitado' if use_cache else 'desabilitado'}")
        
        ai_service = AIService(
            provider=api.lower(),
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            use_cache=use_cache
        )
        
        # Verificar se a API key está configurada
        if not ai_service.is_configured():
            logger.error(f"API key não configurada para {api}")
            click.echo(click.style("❌ Erro: API key não configurada.", fg='red'))
            click.echo("\nConfigurações necessárias:")
            if api.lower() == 'openai':
                click.echo("1. Obtenha sua API key em: https://platform.openai.com/api-keys")
                click.echo("2. Configure a variável de ambiente: OPENAI_API_KEY=sua_api_key")
            elif api.lower() == 'gemini':
                click.echo("1. Obtenha sua API key em: https://makersuite.google.com/app/apikey")
                click.echo("2. Configure a variável de ambiente: GEMINI_API_KEY=sua_api_key")
            click.echo("3. Ou crie um arquivo .env na raiz do projeto com a chave")
            sys.exit(1)
        
        logger.info(f"Serviço de IA configurado: {api} ({ai_service.model})")
        
        # Mostrar informações sobre as alterações
        file_changes = git_handler.get_file_changes()
        click.echo(click.style("📝 Alterações detectadas:", fg='cyan', bold=True))
        for change_type, files in file_changes.items():
            if files:
                click.echo(f"  {change_type}: {', '.join(files)}")
        
        # Gerar mensagem de commit
        logger.info("Iniciando geração de commit com IA...")
        click.echo(click.style("\n🤖 Gerando mensagem de commit com IA...", fg='yellow'))
        
        try:
            commit_message = ai_service.generate_commit_message(diff_text)
            logger.info(f"Mensagem gerada: {commit_message}")
            
            # Exibir a mensagem gerada
            click.echo(click.style("\n✨ Mensagem de commit gerada:", fg='green', bold=True))
            click.echo(click.style(commit_message, fg='white', bold=True))
            
            if preview:
                logger.info("Modo preview - nenhum commit realizado")
                click.echo(click.style("\n👀 Modo preview - nenhum commit foi feito.", fg='blue'))
                return
            
            # Confirmar o commit
            if not auto:
                logger.debug("Aguardando confirmação do usuário...")
                if not click.confirm(click.style("\n🚀 Deseja fazer o commit com esta mensagem?", fg='cyan')):
                    logger.info("Commit cancelado pelo usuário")
                    click.echo(click.style("❌ Commit cancelado.", fg='red'))
                    return
            
            # Fazer o commit
            logger.info("Executando commit...")
            success = git_handler.commit(commit_message)
            if success:
                logger.info("Commit realizado com sucesso")
                click.echo(click.style("✅ Commit realizado com sucesso!", fg='green', bold=True))
            else:
                logger.error("Falha ao realizar commit")
                click.echo(click.style("❌ Erro ao realizar o commit.", fg='red'))
                sys.exit(1)
                
        except Exception as e:
            logger.error(f"Erro ao gerar mensagem: {str(e)}")
            click.echo(click.style(f"❌ Erro ao gerar mensagem: {str(e)}", fg='red'))
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("Operação cancelada pelo usuário (Ctrl+C)")
        click.echo(click.style("\n❌ Operação cancelada pelo usuário.", fg='red'))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        click.echo(click.style(f"❌ Erro inesperado: {str(e)}", fg='red'))
        if verbose:
            click.echo(click.style(f"\n🔍 Para mais detalhes, verifique os logs em: ~/.commit-ai/logs/", fg='yellow'))
        sys.exit(1)


if __name__ == '__main__':
    main()
