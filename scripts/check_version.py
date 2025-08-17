#!/usr/bin/env python3
"""
Script para verificar e sincronizar versões em todos os arquivos do projeto
"""

import json
import re
import sys
from pathlib import Path

# Importar a versão centralizada
sys.path.append(str(Path(__file__).parent))
from commit_ai.version import VERSION, VERSION_DATE

def check_pyproject_version():
    """Verifica versão no pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        return False, "pyproject.toml não encontrado"
    
    content = pyproject_path.read_text(encoding='utf-8')
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        return False, "Versão não encontrada no pyproject.toml"
    
    current_version = match.group(1)
    if current_version == VERSION:
        return True, f"✅ pyproject.toml: {current_version}"
    else:
        return False, f"❌ pyproject.toml: {current_version} ≠ {VERSION}"

def check_changelog_version():
    """Verifica se a versão está no CHANGELOG"""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        return False, "CHANGELOG.md não encontrado"
    
    content = changelog_path.read_text(encoding='utf-8')
    version_pattern = f"## \\[{re.escape(VERSION)}\\]"
    if re.search(version_pattern, content):
        return True, f"✅ CHANGELOG.md: {VERSION} encontrada"
    else:
        return False, f"❌ CHANGELOG.md: {VERSION} não encontrada"

def check_init_version():
    """Verifica versão no __init__.py"""
    init_path = Path("commit_ai/__init__.py")
    if not init_path.exists():
        return False, "__init__.py não encontrado"
    
    try:
        # Importar a versão
        from commit_ai import __version__
        if __version__ == VERSION:
            return True, f"✅ __init__.py: {__version__}"
        else:
            return False, f"❌ __init__.py: {__version__} ≠ {VERSION}"
    except ImportError:
        return False, "Erro ao importar versão do __init__.py"

def check_tag_exists():
    """Verifica se a tag da versão existe"""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "tag", "-l", f"v{VERSION}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return True, f"✅ Git tag: v{VERSION} existe"
        else:
            return False, f"❌ Git tag: v{VERSION} não existe"
    except FileNotFoundError:
        return False, "Git não encontrado"

def update_pyproject_version():
    """Atualiza versão no pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text(encoding='utf-8')
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{VERSION}"',
        content
    )
    pyproject_path.write_text(updated_content, encoding='utf-8')
    return True

def main():
    print(f"🔍 Verificando consistência da versão {VERSION}")
    print("=" * 50)
    
    checks = [
        ("PyProject.toml", check_pyproject_version),
        ("CHANGELOG.md", check_changelog_version), 
        ("__init__.py", check_init_version),
        ("Git Tag", check_tag_exists)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            success, message = check_func()
            results.append((success, message))
            print(message)
        except Exception as e:
            results.append((False, f"❌ {name}: Erro - {e}"))
            print(f"❌ {name}: Erro - {e}")
    
    print("=" * 50)
    
    # Resumo
    successful = sum(1 for success, _ in results if success)
    total = len(results)
    
    if successful == total:
        print(f"🎉 Todas as verificações passaram! ({successful}/{total})")
        print(f"✅ Versão {VERSION} está consistente em todo o projeto")
        return True
    else:
        print(f"⚠️ {successful}/{total} verificações passaram")
        
        # Oferecer correção automática
        if input("\n🔧 Deseja tentar corrigir automaticamente? (y/N): ").lower() == 'y':
            try:
                update_pyproject_version()
                print("✅ pyproject.toml atualizado!")
                
                # Re-verificar
                print("\n🔄 Re-verificando...")
                main()
                
            except Exception as e:
                print(f"❌ Erro na correção: {e}")
                return False
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
