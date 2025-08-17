#!/usr/bin/env python3
"""Script de teste para verificar se todas as dependências estão funcionando"""

def test_dependencies():
    """Testa todas as dependências principais"""
    print("🔍 Testando dependências do Commit-AI v1.4.0...")
    
    # Teste 1: Módulos básicos
    try:
        import requests
        import click
        import git
        from dotenv import load_dotenv
        print("✅ Módulos básicos OK")
    except ImportError as e:
        print(f"❌ Erro nos módulos básicos: {e}")
        return False
    
    # Teste 2: APIs de IA
    try:
        import openai
        import anthropic
        import ollama
        import google.generativeai as genai
        print("✅ APIs de IA OK")
    except ImportError as e:
        print(f"❌ Erro nas APIs de IA: {e}")
        return False
    
    # Teste 3: Rich (TUI)
    try:
        from rich.console import Console
        from rich.progress import Progress
        from rich.table import Table
        console = Console()
        print("✅ Rich (TUI) OK")
    except ImportError as e:
        print(f"❌ Erro no Rich: {e}")
        return False
    
    # Teste 4: Ferramentas de desenvolvimento
    try:
        import pytest
        import black
        import mypy
        print("✅ Ferramentas de desenvolvimento OK")
    except ImportError as e:
        print(f"❌ Erro nas ferramentas de desenvolvimento: {e}")
        return False
    
    # Teste 5: Módulos do Commit-AI
    try:
        from commit_ai.version import VERSION
        import commit_ai.main
        import commit_ai.ai_service
        import commit_ai.cache
        import commit_ai.git_handler
        print(f"✅ Módulos do Commit-AI v{VERSION} OK")
    except ImportError as e:
        print(f"❌ Erro nos módulos do Commit-AI: {e}")
        return False
    
    print("\n🎉 Todos os testes passaram! Commit-AI está pronto para usar.")
    print(f"📋 Versão instalada: {VERSION}")
    return True

if __name__ == "__main__":
    success = test_dependencies()
    exit(0 if success else 1)
