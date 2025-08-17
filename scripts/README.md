# Scripts de Automação

Esta pasta contém scripts úteis para desenvolvimento e manutenção do projeto.

## 📋 Scripts Disponíveis

### `update_version.py`
Script para atualizar a versão do projeto automaticamente.

**Funcionalidades:**
- Atualiza versão em todos os arquivos relevantes
- Cria entrada automática no CHANGELOG.md
- Validação de formato de versão
- Instruções pós-atualização

**Uso:**
```bash
# Atualizar apenas a versão
python scripts/update_version.py 1.2.0

# Atualizar versão com descrição no changelog
python scripts/update_version.py 1.2.0 --changelog "Adiciona sistema de cache"
```

**Arquivos atualizados automaticamente:**
- `commit_ai/__init__.py` - `__version__`
- `pyproject.toml` - `version`
- `README.md` - Badge de versão
- `.github/copilot-instructions.md` - Versão atual
- `CHANGELOG.md` - Nova entrada

## 🚀 Como Usar

1. **Vá para a raiz do projeto:**
   ```bash
   cd Commit-AI
   ```

2. **Execute o script:**
   ```bash
   python scripts/update_version.py 1.2.0
   ```

3. **Siga as instruções exibidas:**
   - Edite o CHANGELOG.md
   - Teste a aplicação
   - Faça commit das mudanças
   - Crie tag da versão

## 📝 Convenções

### Versionamento Semântico
- **X.Y.Z** onde:
  - **X** (MAJOR): Mudanças incompatíveis
  - **Y** (MINOR): Novas funcionalidades compatíveis
  - **Z** (PATCH): Correções compatíveis

### Exemplo de Fluxo
```bash
# 1. Atualizar versão
python scripts/update_version.py 1.2.0 --changelog "Nova funcionalidade de cache"

# 2. Editar CHANGELOG.md manualmente (detalhar mudanças)

# 3. Testar
python -m commit_ai.main --help

# 4. Commit
git add .
git commit -m "chore: bump version to 1.2.0"

# 5. Tag
git tag v1.2.0
git push origin main --tags
```
