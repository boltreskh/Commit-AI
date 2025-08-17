#!/bin/bash
# Script de setup para desenvolvimento

echo "🔧 Configurando ambiente de desenvolvimento..."

# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv .venv
fi

# Ativar ambiente virtual
echo "⚡ Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências de desenvolvimento
echo "📚 Instalando dependências..."
pip install -r requirements-dev.txt

# Instalar o pacote em modo desenvolvimento
echo "🔨 Instalando pacote em modo desenvolvimento..."
pip install -e .

# Configurar pre-commit hooks (opcional)
echo "🪝 Configurando hooks..."
# pre-commit install

echo "✅ Setup completo!"
echo ""
echo "🚀 Para começar:"
echo "   source .venv/bin/activate"
echo "   pytest                     # Executar testes"
echo "   black commit_ai/           # Formatar código"
echo "   python -m commit_ai.main   # Executar aplicação"
