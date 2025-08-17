#!/usr/bin/env python3
"""
Sistem    "1.2.0": {
        "claude_support": "✅ Completo",
        "ollama_support": "✅ Completo", 
        "custom_templates": "✅ Completo",
        "template_cli": "✅ Completo",
        "diff_analysis": "✅ Completo",
        "template_import_export": "✅ Completo",
        "modular_ai_service": "✅ Completo",
        "git_hooks": "📋 Planejado",controle de versão do Commit-AI
Mantém sincronizadas as versões em todos os arquivos do projeto
"""

VERSION = "1.2.0"
VERSION_DATE = "2025-08-17"
VERSION_NAME = "Providers & Templates"

# Metadata da versão
VERSION_INFO = {
    "major": 1,
    "minor": 2, 
    "patch": 0,
    "pre_release": None,
    "build": None
}

# Status das funcionalidades por versão
FEATURES_STATUS = {
    "1.0.0": {
        "ai_integration": "✅ Completo",
        "cli_basic": "✅ Completo", 
        "git_operations": "✅ Completo",
        "multi_providers": "✅ Completo"
    },
    "1.1.0": {
        "cache_system": "✅ Completo",
        "persistent_config": "✅ Completo", 
        "structured_logging": "✅ Completo",
        "automated_tests": "✅ Completo",
        "cache_management": "✅ Completo",
        "robust_validation": "✅ Completo"
    },
    "1.2.0": {
        "claude_support": "� Em desenvolvimento",
        "ollama_support": "� Em desenvolvimento",
        "custom_templates": "� Em desenvolvimento",
        "git_hooks": "📋 Planejado",
        "enhanced_prompts": "� Em desenvolvimento"
    },
    "1.3.0": {
        "tui_interface": "📋 Planejado",
        "syntax_highlighting": "📋 Planejado",
        "code_analysis": "📋 Planejado",
        "config_wizard": "📋 Planejado"
    }
}

# Roadmap detalhado
ROADMAP = {
    "1.2.0": {
        "quarter": "Q4 2025",
        "theme": "Expansão de Providers e Templates",
        "features": [
            "Suporte Anthropic Claude",
            "Suporte Ollama local", 
            "Templates personalizáveis",
            "Git hooks integration"
        ]
    },
    "1.3.0": {
        "quarter": "Q1 2026", 
        "theme": "UX e Interface Aprimorados",
        "features": [
            "TUI interativa",
            "Preview melhorado",
            "Análise contextual de código"
        ]
    },
    "1.4.0": {
        "quarter": "Q2 2026",
        "theme": "Integrações e Ferramentas",  
        "features": [
            "Plugin VS Code",
            "Extensão JetBrains",
            "GitHub CLI integration"
        ]
    },
    "2.0.0": {
        "quarter": "Q3 2026",
        "theme": "Versão Empresarial",
        "features": [
            "GUI multiplataforma",
            "CI/CD integration", 
            "Analytics avançado",
            "IA personalizada"
        ]
    }
}

def get_version():
    """Retorna a versão atual"""
    return VERSION

def get_version_info():
    """Retorna informações detalhadas da versão"""
    return {
        "version": VERSION,
        "date": VERSION_DATE, 
        "name": VERSION_NAME,
        "info": VERSION_INFO
    }

def get_features_status(version=None):
    """Retorna o status das funcionalidades"""
    if version:
        return FEATURES_STATUS.get(version, {})
    return FEATURES_STATUS

def get_roadmap():
    """Retorna o roadmap completo"""
    return ROADMAP

if __name__ == "__main__":
    print(f"Commit-AI v{VERSION} ({VERSION_NAME})")
    print(f"Lançado em: {VERSION_DATE}")
    print("\n🎯 Funcionalidades desta versão:")
    for feature, status in FEATURES_STATUS.get(VERSION, {}).items():
        print(f"  {status} {feature.replace('_', ' ').title()}")
    
    print(f"\n🚀 Próxima versão: {list(ROADMAP.keys())[0]}")
    next_version = list(ROADMAP.values())[0]
    print(f"  📅 Planejado para: {next_version['quarter']}")
    print(f"  🎨 Tema: {next_version['theme']}")
