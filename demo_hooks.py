#!/usr/bin/env python3
"""
Demonstração do sistema de Git Hooks do Commit-AI v1.3.0

Este script demonstra as funcionalidades de automação de hooks implementadas
na versão 1.3.0 "Interface e Automação".
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def print_header(title):
    """Imprime cabeçalho colorido"""
    print(f"\n{'='*60}")
    print(f"🔗 {title}")
    print(f"{'='*60}")

def print_step(step):
    """Imprime passo da demonstração"""
    print(f"\n[PASSO] {step}")

def run_command(cmd, cwd=None, show_output=True):
    """Executa comando e mostra resultado"""
    if show_output:
        print(f"$ {cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            check=False
        )
        
        if show_output and result.stdout:
            print(result.stdout)
        if show_output and result.stderr:
            print(f"[STDERR] {result.stderr}")
            
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        if show_output:
            print(f"[ERROR] {e}")
        return False, "", str(e)

def demo_hooks_installation():
    """Demonstra instalação de hooks"""
    print_header("INSTALAÇÃO DE GIT HOOKS")
    
    print_step("1. Verificando status atual dos hooks")
    run_command("python -m commit_ai hooks status")
    
    print_step("2. Instalando todos os hooks automaticamente")
    run_command("python -m commit_ai hooks install --all")
    
    print_step("3. Verificando hooks instalados")
    run_command("python -m commit_ai hooks status")
    
    print_step("4. Testando saúde dos hooks")
    run_command("python -m commit_ai hooks test pre-commit")

def demo_hooks_configuration():
    """Demonstra configuração de hooks"""
    print_header("CONFIGURAÇÃO DOS HOOKS")
    
    print_step("1. Visualizando configurações atuais")
    run_command("python -m commit_ai hooks config")
    
    print_step("2. Habilitando auto-melhoria de mensagens")
    run_command("python -m commit_ai hooks config --auto-improve")
    
    print_step("3. Configurando templates padrão")
    run_command("python -m commit_ai template set conventional")

def demo_pre_commit_hook():
    """Demonstra funcionamento do pre-commit hook"""
    print_header("DEMO: PRE-COMMIT HOOK")
    
    print_step("1. Criando alterações de exemplo")
    
    # Criar arquivo de exemplo
    test_file = Path("demo_feature.py")
    test_file.write_text('''#!/usr/bin/env python3
"""
Nova funcionalidade de exemplo para demonstração
"""

class ExampleFeature:
    def __init__(self):
        self.name = "Demo Feature"
    
    def process(self):
        """Processa a funcionalidade"""
        return f"Processing {self.name}"

def main():
    feature = ExampleFeature()
    result = feature.process()
    print(result)

if __name__ == "__main__":
    main()
''')
    
    print(f"[INFO] Arquivo criado: {test_file}")
    
    print_step("2. Adicionando ao staging area")
    run_command(f"git add {test_file}")
    
    print_step("3. O pre-commit hook será executado automaticamente")
    print("[INFO] Hook analisa alterações e sugere tipo de commit")
    
    # Simular execução do hook diretamente
    print_step("4. Simulando análise do pre-commit hook")
    print("[HOOK] Analisando diff das alterações...")
    print("[HOOK] Sugestão detectada: feat (confidence: 0.92)")
    print("[HOOK] Tipo: Nova funcionalidade (feature)")

def demo_commit_msg_hook():
    """Demonstra funcionamento do commit-msg hook"""
    print_header("DEMO: COMMIT-MSG HOOK")
    
    print_step("1. Testando mensagem de commit ruim")
    
    # Criar arquivo temporário para mensagem
    msg_file = Path(".git/COMMIT_EDITMSG")
    msg_file.parent.mkdir(exist_ok=True)
    msg_file.write_text("fix bug")
    
    print("[COMMIT] Mensagem original: 'fix bug'")
    
    print_step("2. Hook validará e melhorará a mensagem")
    print("[HOOK] Validando formato da mensagem...")
    print("[HOOK] Mensagem não segue convenções")
    print("[HOOK] Aplicando auto-melhoria...")
    print("[HOOK] Nova mensagem: 'fix: resolve critical bug in user authentication'")
    
    # Atualizar arquivo com mensagem melhorada
    msg_file.write_text("fix: resolve critical bug in user authentication")

def demo_post_commit_hook():
    """Demonstra funcionamento do post-commit hook"""
    print_header("DEMO: POST-COMMIT HOOK")
    
    print_step("1. Simulando commit realizado")
    print("[COMMIT] Commit realizado com sucesso!")
    print("[COMMIT] Hash: a1b2c3d4")
    print("[COMMIT] Mensagem: 'fix: resolve critical bug in user authentication'")
    
    print_step("2. Post-commit hook coletando analytics")
    print("[HOOK] Coletando dados do commit...")
    print("[HOOK] Analisando padrões de commit...")
    print("[HOOK] Atualizando métricas de projeto...")
    print("[HOOK] Analytics salvos em cache")
    
    print_step("3. Sugestões baseadas em histórico")
    print("[ANALYTICS] Commits recentes: 67% fix, 33% feat")
    print("[ANALYTICS] Sugestão: Considere mais commits de feature")
    print("[ANALYTICS] Produtividade: 4.2 commits/dia (média)")

def demo_hooks_management():
    """Demonstra gerenciamento de hooks"""
    print_header("GERENCIAMENTO DE HOOKS")
    
    print_step("1. Listando hooks disponíveis")
    run_command("python -m commit_ai hooks status")
    
    print_step("2. Visualizando logs de hooks")
    run_command("python -m commit_ai hooks logs --lines 5")
    
    print_step("3. Desinstalando hook específico")
    run_command("python -m commit_ai hooks uninstall --hook pre-commit")
    
    print_step("4. Reinstalando todos os hooks")
    run_command("python -m commit_ai hooks install --all")

def demo_integration_workflow():
    """Demonstra workflow completo integrado"""
    print_header("WORKFLOW COMPLETO INTEGRADO")
    
    print_step("1. Desenvolvedor faz alterações")
    print("[DEV] Implementando nova feature...")
    print("[DEV] Alterações prontas para commit")
    
    print_step("2. git add . (ativa pre-commit hook)")
    print("[HOOK] Pre-commit: Analisando alterações...")
    print("[HOOK] Pre-commit: Sugerindo tipo 'feat'")
    
    print_step("3. commit-ai (gera mensagem inteligente)")
    run_command("python -m commit_ai --preview")
    
    print_step("4. git commit (ativa commit-msg hook)")
    print("[HOOK] Commit-msg: Validando mensagem...")
    print("[HOOK] Commit-msg: Mensagem aprovada!")
    
    print_step("5. Post-commit hook (analytics)")
    print("[HOOK] Post-commit: Coletando métricas...")
    print("[HOOK] Post-commit: Workflow completado!")

def cleanup_demo_files():
    """Remove arquivos criados na demonstração"""
    demo_files = [
        "demo_feature.py",
        ".git/COMMIT_EDITMSG"
    ]
    
    for file_path in demo_files:
        try:
            Path(file_path).unlink(missing_ok=True)
        except:
            pass

def main():
    """Função principal da demonstração"""
    print_header("COMMIT-AI v1.3.0 - DEMONSTRAÇÃO DE GIT HOOKS")
    
    print("""
🚀 Esta demonstração mostra as funcionalidades de automação de Git Hooks
   implementadas na versão 1.3.0 "Interface e Automação".

📋 Funcionalidades demonstradas:
   • Instalação e configuração de hooks
   • Pre-commit hook (análise automática)
   • Commit-msg hook (validação e melhoria)
   • Post-commit hook (analytics)
   • Gerenciamento completo via CLI
   • Workflow integrado

⚠️  Nota: Esta é uma demonstração simulada para mostrar funcionalidades.
    Em um ambiente real, os hooks seriam executados automaticamente pelo Git.
    """)
    
    input("\nPressione Enter para iniciar a demonstração...")
    
    try:
        # Verificar se estamos em um repositório git
        success, _, _ = run_command("git status", show_output=False)
        if not success:
            print_step("Inicializando repositório Git para demo")
            run_command("git init")
            run_command("git config user.name 'Demo User'")
            run_command("git config user.email 'demo@commit-ai.com'")
        
        # Executar demonstrações
        demo_hooks_installation()
        
        input("\nPressione Enter para continuar...")
        demo_hooks_configuration()
        
        input("\nPressione Enter para continuar...")
        demo_pre_commit_hook()
        
        input("\nPressione Enter para continuar...")
        demo_commit_msg_hook()
        
        input("\nPressione Enter para continuar...")
        demo_post_commit_hook()
        
        input("\nPressione Enter para continuar...")
        demo_hooks_management()
        
        input("\nPressione Enter para continuar...")
        demo_integration_workflow()
        
        print_header("DEMONSTRAÇÃO CONCLUÍDA")
        print("""
✅ Demonstração completa das funcionalidades de Git Hooks!

🎯 Próximos passos:
   1. Execute: commit-ai hooks install --all
   2. Configure: commit-ai hooks config --auto-improve
   3. Use normalmente: git add . && commit-ai && git commit
   
📚 Mais informações:
   • commit-ai hooks --help
   • commit-ai --help
   • GitHub: https://github.com/boltreskh/commit-ai
        """)
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Demonstração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n[ERROR] Erro durante demonstração: {e}")
    finally:
        cleanup_demo_files()

if __name__ == "__main__":
    main()
