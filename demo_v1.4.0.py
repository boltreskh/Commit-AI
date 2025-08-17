#!/usr/bin/env python3
"""
🎯 DEMONSTRAÇÃO PRÁTICA - Commit-AI v1.4.0
Exemplos de uso das novas funcionalidades avançadas
"""

import os
import sys
import json
from pathlib import Path

# Adicionar o diretório commit_ai ao Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def demo_header(title):
    """Imprime cabeçalho de demonstração"""
    print("\n" + "="*70)
    print(f"🚀 DEMONSTRAÇÃO: {title}")
    print("="*70)

def demo_section(section):
    """Imprime seção de demonstração"""
    print(f"\n📋 {section}")
    print("-" * 50)

# ============================================================================
# DEMONSTRAÇÃO 1: SISTEMA DE PLUGINS
# ============================================================================

demo_header("SISTEMA DE PLUGINS EXTENSÍVEL")

try:
    from commit_ai.plugins_system import PluginManager
    
    demo_section("Inicializando Plugin Manager")
    plugin_manager = PluginManager()
    print("✅ Plugin Manager iniciado com sucesso!")
    
    demo_section("Plugins Disponíveis")
    plugins = plugin_manager.get_available_plugins()
    
    if plugins:
        for plugin_info in plugins:
            status = "🟢 ATIVO" if plugin_info.enabled else "🔴 INATIVO"
            print(f"  • {plugin_info.name} - {status}")
            print(f"    📦 Versão: {plugin_info.version}")
            print(f"    📝 Descrição: {plugin_info.description}")
            print(f"    � Autor: {plugin_info.author}")
            print(f"    🏷️ Categoria: {plugin_info.category}")
            if plugin_info.dependencies:
                print(f"    🔗 Dependências: {', '.join(plugin_info.dependencies)}")
            print()
    else:
        print("📦 Nenhum plugin encontrado. Carregando plugins...")
        plugin_manager.load_plugins()
        print("✅ Plugins carregados!")
    
    demo_section("Plugin de Exemplo: Custom Local AI")
    example_plugin_info = {
        "name": "custom_local_ai",
        "version": "1.0.0",
        "description": "Provider local usando Ollama para geração offline",
        "category": "ai_provider",
        "dependencies": ["ollama"],
        "config": {
            "model": "llama2",
            "endpoint": "http://localhost:11434",
            "timeout": 30
        }
    }
    
    print("📦 Plugin de Exemplo:")
    for key, value in example_plugin_info.items():
        print(f"  • {key.capitalize()}: {value}")

except ImportError as e:
    print(f"⚠️  Plugin system não disponível: {e}")
    print("💡 Execute: pip install -r requirements.txt")

# ============================================================================
# DEMONSTRAÇÃO 2: SISTEMA DE ANALYTICS
# ============================================================================

demo_header("SISTEMA DE ANALYTICS AVANÇADOS")

try:
    from commit_ai.analytics import AnalyticsEngine, ProductivityMetrics
    from datetime import datetime, timedelta
    
    demo_section("Inicializando Analytics Engine")
    
    # Simular dados de exemplo
    analytics = AnalyticsEngine()
    print("✅ Analytics Engine iniciado!")
    
    demo_section("Métricas de Produtividade Simuladas")
    
    # Simular métricas
    fake_metrics = ProductivityMetrics(
        total_commits=150,
        commits_per_day=5.2,
        avg_processing_time=120,  # segundos
        most_used_provider='openai',
        most_used_template='conventional',
        most_common_type='feat',
        avg_confidence=0.92,
        total_lines_changed=2847,
        files_touched=89
    )
    
    # Dados extras para demonstração
    provider_usage = {
        'openai': 45,
        'gemini': 35,
        'claude': 15,
        'ollama': 5
    }
    
    template_usage = {
        'conventional': 60,
        'detailed': 25,
        'simple': 15
    }
    
    most_active_hours = [14, 15, 16, 10]
    most_active_days = ['Monday', 'Tuesday', 'Wednesday']
    
    print("📊 MÉTRICAS DE PRODUTIVIDADE:")
    print(f"  • Total de commits: {fake_metrics.total_commits}")
    print(f"  • Média diária: {fake_metrics.commits_per_day}")
    print(f"  • Horários mais ativos: {most_active_hours}")
    print(f"  • Dias mais ativos: {', '.join(most_active_days)}")
    print(f"  • Tempo médio de processamento: {fake_metrics.avg_processing_time}s")
    print(f"  • Provider mais usado: {fake_metrics.most_used_provider}")
    print(f"  • Template mais usado: {fake_metrics.most_used_template}")
    print(f"  • Tipo mais comum: {fake_metrics.most_common_type}")
    print(f"  • Confiança média: {fake_metrics.avg_confidence:.2f}")
    print(f"  • Total linhas alteradas: {fake_metrics.total_lines_changed}")
    print(f"  • Arquivos tocados: {fake_metrics.files_touched}")
    
    print("\n📈 USO DE PROVIDERS:")
    for provider, count in provider_usage.items():
        percentage = (count / fake_metrics.total_commits) * 100
        bar = "█" * int(percentage / 5)
        print(f"  • {provider.upper():10} {bar:20} {percentage:5.1f}% ({count})")
    
    print("\n📋 USO DE TEMPLATES:")
    for template, count in template_usage.items():
        percentage = (count / fake_metrics.total_commits) * 100
        bar = "█" * int(percentage / 5)
        print(f"  • {template.upper():12} {bar:20} {percentage:5.1f}% ({count})")

except ImportError as e:
    print(f"⚠️  Analytics system não disponível: {e}")

# ============================================================================
# DEMONSTRAÇÃO 3: INTERFACE TUI
# ============================================================================

demo_header("TERMINAL USER INTERFACE (TUI)")

try:
    from commit_ai.tui import CommitTUI, CommitOption
    
    demo_section("Simulando Interface TUI")
    
    # Simular opções de commit
    mock_options = [
        CommitOption(
            message="feat: implementar sistema de plugins extensível",
            type="feat",
            confidence=0.95,
            provider="openai",
            template="conventional",
            preview="feat: implementar sistema de plugins extensível\n\n• PluginManager para gerenciamento central\n• Classes base para diferentes tipos de plugin\n• Sistema de categorização automática\n• Verificação de dependências"
        ),
        CommitOption(
            message="docs: atualizar documentação com funcionalidades v1.4.0",
            type="docs",
            confidence=0.88,
            provider="gemini",
            template="detailed",
            preview="docs: atualizar documentação com funcionalidades v1.4.0\n\nDetalhes da atualização:\n- Guia completo do sistema TUI\n- Documentação de analytics\n- Tutorial de criação de plugins"
        ),
        CommitOption(
            message="refactor: otimizar performance do cache SQLite",
            type="refactor",
            confidence=0.91,
            provider="claude",
            template="conventional",
            preview="refactor: otimizar performance do cache SQLite\n\n• Índices compostos para queries frequentes\n• Otimização de joins em relatórios\n• Cache de resultados agregados"
        )
    ]
    
    print("🎨 EXEMPLO DE OPÇÕES TUI:")
    for i, option in enumerate(mock_options, 1):
        print(f"\n[{i}] {option.message}")
        print(f"    🏷️ Tipo: {option.type}")
        print(f"    🤖 Provider: {option.provider} | 📋 Template: {option.template}")
        print(f"    🎯 Confiança: {option.confidence:.0%}")
        
        # Mostrar preview truncado
        preview_lines = option.preview.split('\n')
        print(f"    👀 Preview:")
        for line in preview_lines[:3]:
            print(f"       {line}")
        if len(preview_lines) > 3:
            print(f"       ... (+{len(preview_lines)-3} linhas)")
    
    print("\n💡 Na TUI real você pode:")
    print("  • ↑/↓ para navegar entre opções")
    print("  • ENTER para confirmar seleção")
    print("  • TAB para preview detalhado")
    print("  • ESC para cancelar")
    print("  • r para regenerar opções")

except ImportError as e:
    print(f"⚠️  TUI system não disponível: {e}")
    print("💡 A TUI requer a biblioteca Rich: pip install rich>=13.0.0")

# ============================================================================
# DEMONSTRAÇÃO 4: WIZARD DE CONFIGURAÇÃO
# ============================================================================

demo_header("WIZARD DE CONFIGURAÇÃO INTERATIVO")

demo_section("Fluxo de Configuração Guiada")

wizard_steps = [
    {
        "step": 1,
        "title": "Verificação de Dependências",
        "description": "Verifica Git, Python e outras dependências necessárias",
        "status": "✅ Git 2.40.1 encontrado\n✅ Python 3.11.0 encontrado\n✅ Todas as dependências OK"
    },
    {
        "step": 2,
        "title": "Configuração de AI Providers",
        "description": "Configura credenciais e preferências dos provedores",
        "status": "🔑 OpenAI API Key configurada\n🔑 Gemini API Key configurada\n⚙️ Ollama detectado localmente"
    },
    {
        "step": 3,
        "title": "Seleção de Templates",
        "description": "Escolhe templates padrão e configurações de mensagem",
        "status": "📋 Template padrão: conventional\n📝 Idioma: português\n🎯 Nível de detalhes: médio"
    },
    {
        "step": 4,
        "title": "Configuração de Git Hooks",
        "description": "Instala e configura hooks automáticos",
        "status": "🪝 Pre-commit hook instalado\n🔄 Prepare-commit-msg configurado\n✅ Hooks testados e funcionais"
    },
    {
        "step": 5,
        "title": "Sistema de Analytics",
        "description": "Configura coleta e análise de métricas",
        "status": "📊 Banco SQLite inicializado\n📈 Métricas de produtividade ativadas\n🎯 Dashboard configurado"
    },
    {
        "step": 6,
        "title": "Plugins e Extensões",
        "description": "Configura plugins disponíveis e preferências",
        "status": "🔌 Plugin system inicializado\n📦 Custom Local AI habilitado\n🔧 Configurações de plugins salvas"
    },
    {
        "step": 7,
        "title": "Interface e Preferências",
        "description": "Configura interface, tema e preferências pessoais",
        "status": "🎨 TUI habilitada por padrão\n🌙 Tema escuro selecionado\n⚡ Configuração salva"
    }
]

for step_info in wizard_steps:
    print(f"\n🔧 PASSO {step_info['step']}: {step_info['title']}")
    print(f"   📝 {step_info['description']}")
    print(f"   {step_info['status']}")

print(f"\n✨ WIZARD COMPLETO!")
print("🎯 Commit-AI está pronto para uso com todas as funcionalidades!")

# ============================================================================
# DEMONSTRAÇÃO 5: COMANDOS CLI EXPANDIDOS
# ============================================================================

demo_header("COMANDOS CLI EXPANDIDOS v1.4.0")

demo_section("Novos Comandos Disponíveis")

new_commands = [
    {
        "command": "commit-ai setup",
        "description": "Inicia wizard de configuração interativo",
        "example": "commit-ai setup --interactive"
    },
    {
        "command": "commit-ai tui",
        "description": "Inicia interface terminal interativa",
        "example": "commit-ai tui --theme dark"
    },
    {
        "command": "commit-ai analytics",
        "description": "Exibe relatórios de produtividade e métricas",
        "example": "commit-ai analytics --period 30d --export json"
    },
    {
        "command": "commit-ai plugin",
        "description": "Gerencia plugins (listar, instalar, configurar)",
        "example": "commit-ai plugin list --category ai_provider"
    },
    {
        "command": "commit-ai hooks",
        "description": "Gerencia Git hooks (instalar, atualizar, remover)",
        "example": "commit-ai hooks install --auto-commit"
    }
]

for cmd in new_commands:
    print(f"\n🔨 {cmd['command']}")
    print(f"   📝 {cmd['description']}")
    print(f"   💡 Exemplo: {cmd['example']}")

print("\n📚 Comandos existentes mantidos:")
existing_commands = [
    "commit-ai generate",
    "commit-ai configure", 
    "commit-ai templates",
    "commit-ai cache",
    "commit-ai providers"
]

for cmd in existing_commands:
    print(f"  ✅ {cmd}")

# ============================================================================
# DEMONSTRAÇÃO FINAL
# ============================================================================

demo_header("RESUMO DA DEMONSTRAÇÃO")

print("🎊 FUNCIONALIDADES v1.4.0 DEMONSTRADAS:")
print("  ✅ Sistema de Plugins Extensível")
print("  ✅ Analytics Avançados com Métricas Detalhadas") 
print("  ✅ Interface TUI Rica e Interativa")
print("  ✅ Wizard de Configuração Completo")
print("  ✅ Comandos CLI Expandidos")

print("\n🚀 BENEFÍCIOS PRINCIPAIS:")
print("  🎨 Experiência visual rica e profissional")
print("  📊 Insights detalhados de produtividade")  
print("  🔌 Extensibilidade através de plugins")
print("  🔧 Configuração simplificada e guiada")
print("  ⚡ Performance otimizada e UX aprimorada")

print("\n💫 A v1.4.0 transforma o Commit-AI de uma ferramenta CLI simples")
print("   em uma suíte completa de produtividade para desenvolvimento!")

print("\n" + "="*70)
print("✨ DEMONSTRAÇÃO CONCLUÍDA - COMMIT-AI v1.4.0 ✨")
print("="*70)
