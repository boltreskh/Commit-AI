#!/usr/bin/env python3
"""
Script para atualizar versão do Commit-AI

Atualiza a versão em todos os arquivos relevantes e cria uma entrada no changelog.

Uso:
    python update_version.py 1.2.0
    python update_version.py 1.2.0 --changelog "Nova funcionalidade X"
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List


def update_version_in_file(file_path: Path, old_version: str, new_version: str) -> bool:
    """Atualiza a versão em um arquivo específico"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Padrões para diferentes tipos de arquivo
        patterns = {
            'version = "': f'version = "{new_version}"',
            '__version__ = "': f'__version__ = "{new_version}"',
            '**v': f'**v{new_version}**',
        }
        
        updated = False
        for pattern, replacement in patterns.items():
            if pattern in content:
                old_pattern = pattern + old_version
                new_pattern = replacement
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    updated = True
        
        if updated:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ Atualizado: {file_path}")
            return True
        else:
            print(f"⚠️  Não encontrado: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro em {file_path}: {e}")
        return False


def get_current_version() -> str:
    """Obtém a versão atual do projeto"""
    init_file = Path("commit_ai/__init__.py")
    if init_file.exists():
        content = init_file.read_text()
        match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return "0.0.0"


def update_changelog(new_version: str, description: str = ""):
    """Atualiza o CHANGELOG.md com a nova versão"""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        print("❌ CHANGELOG.md não encontrado")
        return
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Lê o conteúdo atual
    lines = changelog_path.read_text(encoding='utf-8').split('\n')
    
    # Encontra onde inserir a nova versão
    insert_index = 0
    for i, line in enumerate(lines):
        if line.startswith('## ['):
            insert_index = i
            break
    
    # Cria a nova entrada
    new_entry = [
        f"## [{new_version}] - {current_date}",
        "",
        "### ✨ Adicionado",
        f"- {description}" if description else "- [Descrever mudanças aqui]",
        "",
        "### 📚 Melhorado",
        "- [Descrever melhorias aqui]",
        "",
        "### 🐛 Corrigido", 
        "- [Descrever correções aqui]",
        "",
    ]
    
    # Insere a nova entrada
    lines[insert_index:insert_index] = new_entry
    
    # Salva o arquivo
    changelog_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✅ CHANGELOG.md atualizado com v{new_version}")


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("❌ Uso: python update_version.py <nova_versao> [--changelog <descricao>]")
        print("   Exemplo: python update_version.py 1.2.0 --changelog 'Nova funcionalidade'")
        sys.exit(1)
    
    new_version = sys.argv[1]
    changelog_desc = ""
    
    # Parse dos argumentos
    if "--changelog" in sys.argv:
        changelog_idx = sys.argv.index("--changelog")
        if len(sys.argv) > changelog_idx + 1:
            changelog_desc = sys.argv[changelog_idx + 1]
    
    # Validar formato da versão
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print(f"❌ Formato de versão inválido: {new_version}")
        print("   Use o formato: X.Y.Z (ex: 1.2.0)")
        sys.exit(1)
    
    current_version = get_current_version()
    print(f"🔄 Atualizando versão: {current_version} → {new_version}")
    
    # Arquivos para atualizar
    files_to_update = [
        Path("commit_ai/__init__.py"),
        Path("pyproject.toml"),
        Path("README.md"),
        Path(".github/copilot-instructions.md"),
    ]
    
    # Atualizar cada arquivo
    success_count = 0
    for file_path in files_to_update:
        if file_path.exists():
            if update_version_in_file(file_path, current_version, new_version):
                success_count += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {file_path}")
    
    # Atualizar changelog
    update_changelog(new_version, changelog_desc)
    
    print(f"\n🎉 Versão atualizada com sucesso!")
    print(f"   📁 Arquivos atualizados: {success_count}/{len(files_to_update)}")
    print(f"   📝 CHANGELOG.md atualizado")
    print(f"\n💡 Próximos passos:")
    print(f"   1. Edite o CHANGELOG.md para detalhar as mudanças")
    print(f"   2. Teste a aplicação: python -m commit_ai.main --help")
    print(f"   3. Commit as mudanças: git add . && git commit -m 'chore: bump version to {new_version}'")
    print(f"   4. Crie uma tag: git tag v{new_version}")


if __name__ == "__main__":
    main()
