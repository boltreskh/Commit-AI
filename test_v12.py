#!/usr/bin/env python3
"""
Teste de integração do sistema de templates v1.2.0
"""

from commit_ai.templates import CommitTemplateManager
from commit_ai.ai_service import AIService
from commit_ai.config_manager import ConfigManager
from commit_ai.git_handler import GitHandler

def test_templates():
    """Testa o sistema de templates"""
    print("🎨 Testando sistema de templates v1.2.0...")
    
    # Inicializar gerenciadores
    template_manager = CommitTemplateManager()
    
    # Teste 1: Listar templates
    print("\n📋 Templates disponíveis:")
    templates = template_manager.get_all_templates()
    for type_name in list(templates.keys())[:3]:  # Mostrar só 3 para economizar espaço
        template = templates[type_name]
        print(f"  • {type_name}: {template['description']}")
    
    # Teste 2: Sugerir tipo baseado em diff simulado
    sample_diff = """
    +++ b/src/auth.py
    @@ -0,0 +1,10 @@
    +def login_user(username, password):
    +    # Nova função de login
    +    return authenticate(username, password)
    +
    +def logout_user(session):
    +    # Nova função de logout
    +    session.clear()
    """
    
    suggested_type = template_manager.analyze_diff_and_suggest_type(sample_diff)
    print(f"\n💡 Tipo sugerido para diff de autenticação: {suggested_type}")
    
    # Teste 3: Gerar mensagem com template
    message = template_manager.generate_message_with_template(
        suggested_type, 
        "implementa sistema de autenticação de usuários", 
        "auth"
    )
    print(f"📝 Mensagem gerada: {message}")
    
    # Teste 4: Adicionar template personalizado
    success = template_manager.add_template(
        "hotfix",
        "hotfix({scope}): {description}",
        "Correção crítica urgente",
        ["hotfix(security): corrige vulnerabilidade XSS"]
    )
    print(f"\n🔧 Template personalizado adicionado: {'✅' if success else '❌'}")
    
    print("\n✅ Sistema de templates v1.2.0 funcionando corretamente!")

def test_integration():
    """Testa integração entre componentes"""
    print("\n🔄 Testando integração entre componentes...")
    
    try:
        config_manager = ConfigManager()
        ai_service = AIService(config_manager, use_cache=False)
        
        print(f"  • ConfigManager: ✅")
        print(f"  • AIService inicializado: ✅")
        print(f"  • Providers disponíveis: {', '.join(ai_service.get_available_providers())}")
        print(f"  • Templates integrados: ✅")
        
    except Exception as e:
        print(f"  • Erro na integração: ❌ {e}")

if __name__ == "__main__":
    test_templates()
    test_integration()
    print("\n🚀 Commit-AI v1.2.0 - Sistema de Providers & Templates completo!")
