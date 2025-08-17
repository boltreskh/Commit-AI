#!/usr/bin/env python3
"""
Commit-AI - Gerador de mensagens de commit usando IA

Este é o ponto de entrada principal da aplicação CLI.
"""

import os
import sys
import subprocess
import click
from dotenv import load_dotenv
from .git_handler import GitHandler
from .ai_service import AIService

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

@click.command()
@click.option('--api', 
              type=click.Choice(['openai', 'gemini'], case_sensitive=False),
              default='openai',
              help='Serviço de IA a ser usado (padrão: openai)')
@click.option('--model',
              default=None,
              help='Modelo específico a ser usado (ex: gpt-4, gemini-pro)')
@click.option('--max-tokens',
              default=100,
              help='Número máximo de tokens para a resposta (padrão: 100)')
@click.option('--temperature',
              default=0.3,
              help='Criatividade da resposta (0.0-1.0, padrão: 0.3)')
@click.option('--preview',
              is_flag=True,
              help='Apenas visualizar a mensagem sem fazer o commit')
@click.option('--auto',
              is_flag=True,
              help='Fazer commit automaticamente sem confirmação')
def main(api, model, max_tokens, temperature, preview, auto):
    """
    🤖 Commit-AI - Gerador inteligente de mensagens de commit
    
    Gera mensagens de commit profissionais usando IA baseada nas suas alterações de código.
    
    Exemplos de uso:
        commit-ai                    # Usar OpenAI GPT-4 (padrão)
        commit-ai --api gemini       # Usar Google Gemini
        commit-ai --preview          # Apenas visualizar a mensagem
        commit-ai --auto             # Commit automático
    """
    
    try:
        # Verificar se estamos em um repositório Git
        git_handler = GitHandler()
        if not git_handler.is_git_repo():
            click.echo(click.style("❌ Erro: Este diretório não é um repositório Git.", fg='red'))
            sys.exit(1)
        
        # Verificar se há alterações para commit
        diff_text = git_handler.get_staged_diff()
        if not diff_text.strip():
            click.echo(click.style("⚠️  Nenhuma alteração staged encontrada.", fg='yellow'))
            click.echo("Execute 'git add <arquivos>' antes de usar o commit-ai")
            sys.exit(1)
        
        # Configurar o serviço de IA
        ai_service = AIService(
            provider=api.lower(),
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        # Verificar se a API key está configurada
        if not ai_service.is_configured():
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
        
        # Mostrar informações sobre as alterações
        file_changes = git_handler.get_file_changes()
        click.echo(click.style("📝 Alterações detectadas:", fg='cyan', bold=True))
        for change_type, files in file_changes.items():
            if files:
                click.echo(f"  {change_type}: {', '.join(files)}")
        
        # Gerar mensagem de commit
        click.echo(click.style("\n🤖 Gerando mensagem de commit com IA...", fg='yellow'))
        
        try:
            commit_message = ai_service.generate_commit_message(diff_text)
            
            # Exibir a mensagem gerada
            click.echo(click.style("\n✨ Mensagem de commit gerada:", fg='green', bold=True))
            click.echo(click.style(commit_message, fg='white', bold=True))
            
            if preview:
                click.echo(click.style("\n👀 Modo preview - nenhum commit foi feito.", fg='blue'))
                return
            
            # Confirmar o commit
            if not auto:
                if not click.confirm(click.style("\n🚀 Deseja fazer o commit com esta mensagem?", fg='cyan')):
                    click.echo(click.style("❌ Commit cancelado.", fg='red'))
                    return
            
            # Fazer o commit
            success = git_handler.commit(commit_message)
            if success:
                click.echo(click.style("✅ Commit realizado com sucesso!", fg='green', bold=True))
            else:
                click.echo(click.style("❌ Erro ao realizar o commit.", fg='red'))
                sys.exit(1)
                
        except Exception as e:
            click.echo(click.style(f"❌ Erro ao gerar mensagem: {str(e)}", fg='red'))
            sys.exit(1)
    
    except KeyboardInterrupt:
        click.echo(click.style("\n❌ Operação cancelada pelo usuário.", fg='red'))
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"❌ Erro inesperado: {str(e)}", fg='red'))
        sys.exit(1)


if __name__ == '__main__':
    main()
