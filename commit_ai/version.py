#!/usr/bin/env python3
"""Sistema de controle de versão do Commit-AI"""

# Versão atual do projeto
VERSION = "1.2.0"
VERSION_DATE = "17/08/2025"
VERSION_NAME = "Providers & Templates" 
VERSION_INFO = "Sistema completo de múltiplos provedores AI e templates personalizados"

# Status das funcionalidades por versão (usando texto simples para compatibilidade)
FEATURES_STATUS = {
    "1.0.0": {
        "basic_ai_commit": "[OK] Completo",
        "openai_integration": "[OK] Completo", 
        "gemini_integration": "[OK] Completo",
        "cli_interface": "[OK] Completo",
        "git_operations": "[OK] Completo",
        "multi_providers": "[OK] Completo"
    },
    "1.1.0": {
        "cache_system": "[OK] Completo",
        "persistent_config": "[OK] Completo", 
        "structured_logging": "[OK] Completo",
        "automated_tests": "[OK] Completo",
        "cache_management": "[OK] Completo",
        "robust_validation": "[OK] Completo"
    },
    "1.2.0": {
        "claude_support": "[OK] Completo",
        "ollama_support": "[OK] Completo", 
        "custom_templates": "[OK] Completo",
        "template_cli": "[OK] Completo",
        "diff_analysis": "[OK] Completo",
        "template_import_export": "[OK] Completo",
        "modular_ai_service": "[OK] Completo",
        "enhanced_prompts": "[OK] Completo",
        "git_hooks": "[PLAN] Planejado"
    },
    "1.3.0": {
        "tui_interface": "[PLAN] Planejado",
        "syntax_highlighting": "[PLAN] Planejado",
        "code_analysis": "[PLAN] Planejado",
        "config_wizard": "[PLAN] Planejado"
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
            "CLI de gerenciamento de templates"
        ]
    },
    "1.3.0": {
        "quarter": "Q1 2026", 
        "theme": "Interface e Automação",
        "features": [
            "Git hooks automáticos",
            "Interface texto melhorada"
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
        "info": VERSION_INFO,
        "features": FEATURES_STATUS,
        "roadmap": ROADMAP
    }

def get_features_status(version=None):
    """Retorna o status das funcionalidades"""
    if version:
        return FEATURES_STATUS.get(version, {})
    return FEATURES_STATUS

def get_version_summary():
    """Retorna um resumo da versão atual"""
    features = FEATURES_STATUS.get(VERSION, {})
    total = len(features)
    completed = len([f for f in features.values() if "[OK]" in f])
    
    return {
        "version": VERSION,
        "name": VERSION_NAME,
        "date": VERSION_DATE,
        "total_features": total,
        "completed_features": completed,
        "completion_rate": f"{(completed/total*100):.1f}%" if total > 0 else "0%"
    }

if __name__ == "__main__":
    print(f"Commit-AI v{VERSION} - {VERSION_NAME}")
    print(f"Data: {VERSION_DATE}")
    
    summary = get_version_summary()
    print(f"Status: {summary['completed_features']}/{summary['total_features']} funcionalidades ({summary['completion_rate']})")
