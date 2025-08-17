#!/usr/bin/env python3
"""
Commit-AI - Script de Demonstração

Autor: boltreskh (lucascanluz@gmail.com)
Este script demonstra as funcionalidades do Commit-AI.
"""

import os
import subprocess
import sys

def run_demo():
    """Executa uma demonstração do Commit-AI"""
    print("🤖 Commit-AI - Demonstração")
    print("=" * 50)
    
    # Verificar se estamos em um repo Git
    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        print("✅ Repositório Git detectado")
    except subprocess.CalledProcessError:
        print("❌ Este diretório não é um repositório Git")
        print("💡 Inicialize um repo com: git init")
        return
    
    # Verificar se há alterações staged
    result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                          capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("⚠️  Nenhuma alteração staged encontrada")
        print("💡 Adicione arquivos com: git add <arquivo>")
        
        # Verificar se há alterações não staged
        result_unstaged = subprocess.run(['git', 'diff', '--name-only'], 
                                       capture_output=True, text=True)
        if result_unstaged.stdout.strip():
            print("\n📁 Arquivos com alterações não staged:")
            for file in result_unstaged.stdout.strip().split('\n'):
                print(f"  - {file}")
        return
    
    print("📝 Alterações staged encontradas:")
    for file in result.stdout.strip().split('\n'):
        print(f"  - {file}")
    
    # Verificar configuração de API
    api_configured = bool(os.getenv('OPENAI_API_KEY')) or bool(os.getenv('GEMINI_API_KEY'))
    
    if not api_configured:
        print("\n⚠️  API key não configurada")
        print("💡 Configure uma das seguintes variáveis:")
        print("   - OPENAI_API_KEY (para OpenAI GPT)")
        print("   - GEMINI_API_KEY (para Google Gemini)")
        print("   - Ou crie um arquivo .env com a chave")
        return
    
    print("\n✅ Configuração válida - pronto para gerar commits!")
    print("\n🚀 Comandos disponíveis:")
    print("   python -m commit_ai.main                    # Uso básico")
    print("   python -m commit_ai.main --preview          # Apenas visualizar")
    print("   python -m commit_ai.main --api gemini       # Usar Gemini")
    print("   python -m commit_ai.main --auto             # Commit automático")


def show_help():
    """Mostra ajuda e informações sobre o projeto"""
    help_text = """
🤖 Commit-AI - Assistente Inteligente de Commits

INSTALAÇÃO:
1. Clone o repositório
2. Crie um ambiente virtual: python -m venv .venv  
3. Ative o ambiente: .venv\\Scripts\\activate (Windows)
4. Instale dependências: pip install -r requirements.txt
5. Configure sua API key no arquivo .env

CONFIGURAÇÃO DA API:
Crie um arquivo .env com:
   OPENAI_API_KEY=sua_key_aqui    # Para OpenAI GPT
   GEMINI_API_KEY=sua_key_aqui    # Para Google Gemini

COMO USAR:
1. Faça suas alterações de código
2. Adicione ao staging: git add .
3. Execute: python -m commit_ai.main

OPÇÕES AVANÇADAS:
   --api [openai|gemini]     # Escolher provedor de IA
   --model MODEL_NAME        # Modelo específico
   --preview                 # Apenas visualizar mensagem
   --auto                    # Commit automático
   --temperature 0.0-1.0     # Criatividade da resposta
   --max-tokens NUMBER       # Tamanho máximo da mensagem

EXEMPLOS:
   python -m commit_ai.main --api gemini --preview
   python -m commit_ai.main --auto --temperature 0.5
   python -m commit_ai.main --model gpt-3.5-turbo
"""
    print(help_text)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
    else:
        run_demo()
