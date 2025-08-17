#!/usr/bin/env python3
"""Sistema de controle de versão do Commit-AI"""

# Versão atual do projeto
VERSION = "1.4.0"
VERSION_DATE = "17/08/2025"
VERSION_NAME = "Interface Avançada e Analytics" 
VERSION_INFO = "TUI interativa, analytics avançados, dashboards e plugins"

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
        "git_hooks_system": "[OK] Sistema completo de Git Hooks",
        "pre_commit_hook": "[OK] Hook de análise pré-commit",
        "commit_msg_hook": "[OK] Hook de validação de mensagens",
        "post_commit_hook": "[OK] Hook de analytics pós-commit",
        "hooks_cli": "[OK] CLI de gerenciamento de hooks",
        "hooks_config": "[OK] Sistema de configuração de hooks",
        "auto_improve": "[OK] Auto-melhoria de mensagens via IA",
        "hooks_testing": "[OK] Suite de testes para hooks",
        "hooks_health": "[OK] Verificação de integridade dos hooks",
        "hooks_documentation": "[OK] Documentação completa dos hooks"
    },
    "1.4.0": {
        "interactive_tui": "[OK] Terminal UI interativa com Rich library",
        "syntax_highlighting": "[OK] Preview com destaque de sintaxe",
        "multiple_options": "[OK] Seleção entre múltiplas opções de commit", 
        "configuration_wizard": "[OK] Wizard de configuração passo-a-passo",
        "advanced_analytics": "[OK] Dashboards de produtividade e métricas SQLite",
        "commit_patterns": "[OK] Análise de padrões temporais de commits",
        "team_insights": "[OK] Insights colaborativos e score de equipe",
        "plugin_system": "[OK] Framework extensível de plugins",
        "custom_providers": "[OK] Plugin de exemplo Custom Local AI",
        "performance_metrics": "[OK] Métricas de performance e tempo de processamento",
        "export_reports": "[OK] Exportação de relatórios JSON/CSV/texto",
        "plugin_management": "[OK] CLI completo de gerenciamento de plugins",
        "theme_system": "[OK] Sistema de temas para interface TUI",
        "fallback_support": "[OK] Fallback gracioso para terminais básicos",
        "hot_loading": "[OK] Carregamento dinâmico de plugins"
    }
}

# Roadmap detalhado
ROADMAP = {
    "1.2.0": {
        "quarter": "Q4 2025",
        "status": "✅ CONCLUÍDO",
        "theme": "Expansão de Providers e Templates",
        "features": [
            "✅ Suporte Anthropic Claude",
            "✅ Suporte Ollama local", 
            "✅ Templates personalizáveis",
            "✅ CLI de gerenciamento de templates"
        ]
    },
    "1.3.0": {
        "quarter": "Q1 2026", 
        "status": "✅ CONCLUÍDO",
        "theme": "Interface e Automação",
        "features": [
            "✅ Git hooks automáticos completos",
            "✅ CLI de gerenciamento de hooks",
            "✅ Sistema de analytics via hooks"
        ]
    },
    "1.4.0": {
        "quarter": "Q2 2026",
        "status": "✅ CONCLUÍDO",
        "theme": "Interface Avançada e Analytics", 
        "features": [
            "✅ Terminal UI (TUI) interativa com Rich",
            "✅ Analytics e dashboards avançados SQLite",
            "✅ Sistema de plugins extensível",
            "✅ Wizard de configuração interativo",
            "✅ Framework completo de métricas"
        ]
    },
    "1.5.0": {
        "quarter": "Q1 2026",
        "status": "🔄 PRÓXIMO",
        "theme": "Interface Gráfica e Colaboração",
        "features": [
            "🖥️ Interface gráfica desktop (GUI)",
            "🔗 Integração com IDEs (VS Code, JetBrains)",
            "☁️ Sincronização em nuvem de configurações",
            "🤝 Recursos colaborativos avançados",
            "📱 Interface web para configuração"
        ]
    },
    "2.0.0": {
        "quarter": "Q2 2026",
        "status": "🎯 PLANEJADO",
        "theme": "Versão Empresarial",
        "features": [
            "🌐 Marketplace de plugins comunitários",
            "🔐 Recursos enterprise e compliance", 
            "🧠 Machine Learning personalizado",
            "📊 Análise preditiva de commits",
            "👥 Gerenciamento de equipes"
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
