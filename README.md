# 🤖 Commit-AI v1.4.0 - "Interface Avançada e Analytics"

Uma suíte completa de produtividade para commits Git com IA, interface rica, analytics avançados e sistema extensível de plugins.

## ⭐ NOVIDADES v1.4.0

### 🎨 Terminal User Interface (TUI)
- **Interface interativa rica**: Navegação visual com Rich library
- **Seleção múltipla de opções**: Escolha entre várias sugestões de commit
- **Preview detalhado**: Visualização completa antes do commit
- **Syntax highlighting**: Destaque de código e diffs
- **Temas personalizáveis**: Interface adaptável ao seu estilo
- **Fallback inteligente**: Funciona em qualquer terminal

### 📊 Sistema de Analytics Avançados
- **Métricas de produtividade**: Análise detalhada do seu workflow
- **Dashboards visuais**: Relatórios de performance e tendências
- **Analytics por provider/template**: Insights de uso e eficiência
- **Score de colaboração**: Análise de padrões de equipe
- **Exportação de dados**: Relatórios em JSON e texto
- **Base SQLite**: Armazenamento persistente de métricas

### 🔌 Sistema de Plugins Extensível
- **Framework completo**: Arquitetura modular para extensões
- **4 tipos de plugins**: AI Providers, Templates, Workflows, Integrações
- **Plugin de exemplo**: Custom Local AI com Ollama
- **CLI de gerenciamento**: Instalar, habilitar, configurar plugins
- **Templates de criação**: Facilita desenvolvimento de novos plugins
- **Hot-loading**: Carregamento dinâmico sem reinicialização

### 🔧 Wizard de Configuração
- **Setup guiado**: Configuração passo-a-passo interativa
- **Detecção automática**: Identifica configurações existentes
- **Interface dupla**: Rich UI + fallback simples
- **Configuração completa**: Providers, hooks, analytics, plugins
- **Validação em tempo real**: Testa conectividade e dependências

## ✨ Funcionalidades Principais

### Core Features
- **Geração inteligente de commits**: IA analisa mudanças e gera mensagens profissionais
- **4 Provedores de IA**: OpenAI GPT, Google Gemini, Anthropic Claude, Ollama Local
- **Sistema de templates avançado**: 8 padrão + templates personalizados
- **Cache SQLite inteligente**: Performance otimizada e uso offline
- **Git Hooks automáticos**: Integração completa no workflow Git
- **Configuração persistente**: Preferências salvas automaticamente

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.8+
- Git instalado e configurado
- API key de pelo menos um provedor de IA (opcional para Ollama)

### 1. Clone e instale

```bash
git clone https://github.com/boltreskh/Commit-AI.git
cd Commit-AI
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/Mac  
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configuração automática

```bash
# Execute o wizard de configuração interativo
commit-ai setup

# Ou configure manualmente criando .env
```

### 3. Comece a usar!

```bash
# Faça suas alterações
git add .

# Gere commit inteligente
commit-ai

# Ou use a interface interativa
commit-ai tui
```

## 🔧 Configuração Detalhada

### Wizard de Configuração (Recomendado)

O Commit-AI v1.4.0 inclui um wizard interativo que configura tudo automaticamente:

```bash
commit-ai setup
```

O wizard irá:
1. ✅ Verificar dependências (Git, Python)
2. 🔑 Configurar API keys dos provedores
3. 📋 Escolher templates e preferências
4. 🪝 Instalar Git hooks automáticos
5. 📊 Configurar sistema de analytics
6. 🔌 Habilitar plugins desejados
7. 🎨 Configurar interface e temas

### Configuração Manual

Se preferir configurar manualmente, crie um arquivo `.env`:

```env
# Para OpenAI
OPENAI_API_KEY=sua_api_key_aqui

# Para Google Gemini  
GEMINI_API_KEY=sua_api_key_aqui

# Para Anthropic Claude
ANTHROPIC_API_KEY=sua_api_key_aqui

# Configurações opcionais
DEFAULT_PROVIDER=openai
DEFAULT_TEMPLATE=conventional
LANGUAGE=portuguese
```

## 🎯 Como Usar

### 🎨 Interface TUI (Recomendado)

A nova interface interativa oferece a melhor experiência:

```bash
# Prepare suas alterações
git add .

# Interface interativa rica
commit-ai tui

# Com tema específico
commit-ai tui --theme dark
```

**Navegação na TUI:**
- `↑/↓` - Navegar entre opções
- `ENTER` - Confirmar seleção  
- `TAB` - Preview detalhado
- `r` - Regenerar opções
- `ESC` - Cancelar

### ⚡ Comando Básico (CLI)

```bash
# Gerar commit automaticamente
commit-ai

# Com opções específicas
commit-ai --provider gemini --template detailed --auto-commit
```

### 📊 Analytics e Métricas

```bash
# Dashboard completo
commit-ai analytics

# Período específico
commit-ai analytics --period 30d

# Exportar relatório
commit-ai analytics --export json --output report.json
```

### 🔌 Gerenciamento de Plugins

```bash
# Listar plugins disponíveis
commit-ai plugin list

# Informações de um plugin
commit-ai plugin info custom_local_ai

# Habilitar/desabilitar
commit-ai plugin enable custom_local_ai
commit-ai plugin disable custom_local_ai

# Criar novo plugin
commit-ai plugin create meu_plugin
```

### 🪝 Git Hooks Automáticos

```bash
# Instalar hooks (automático via wizard)
commit-ai hooks install

# Status dos hooks
commit-ai hooks status

# Atualizar hooks
commit-ai hooks update

# Habilitar auto-commit
commit-ai hooks install --auto-commit
```

### Opções Avançadas do CLI

```bash
# Geração personalizada
commit-ai --provider gemini --template detailed --language english

# Preview sem commit
commit-ai --preview

# Auto-commit sem confirmação  
commit-ai --auto

# Modo verboso para debug
commit-ai --verbose

# Com modelos específicos
commit-ai --model gpt-4 --temperature 0.7 --max-tokens 100
```

## 📚 Comandos Disponíveis

### Comandos Principais

```bash
commit-ai                    # Geração básica de commit
commit-ai tui               # Interface interativa (TUI)
commit-ai setup             # Wizard de configuração
commit-ai analytics         # Dashboard de métricas
```

### Gerenciamento de Configuração

```bash
commit-ai configure         # Configurar sistema
commit-ai providers         # Gerenciar providers de IA
commit-ai templates         # Gerenciar templates
commit-ai cache             # Gerenciar cache
```

### Git Hooks (Automação)

```bash
commit-ai hooks install     # Instalar hooks automáticos
commit-ai hooks status      # Status dos hooks
commit-ai hooks update      # Atualizar hooks
commit-ai hooks remove      # Remover hooks
```

### Sistema de Plugins

```bash
commit-ai plugin list       # Listar plugins
commit-ai plugin info <name> # Informações do plugin
commit-ai plugin enable <name>   # Habilitar plugin
commit-ai plugin disable <name>  # Desabilitar plugin
commit-ai plugin install <path>  # Instalar plugin
commit-ai plugin create <name>   # Criar template de plugin
```

### Analytics e Relatórios

```bash
commit-ai analytics                    # Dashboard completo
commit-ai analytics --period 7d        # Últimos 7 dias
commit-ai analytics --export json      # Exportar JSON
commit-ai analytics --provider openai  # Métricas por provider
```

## 🎨 Templates de Mensagem

O Commit-AI inclui 8 templates profissionais + sistema de templates personalizados:

### Templates Padrão

| Template | Descrição | Exemplo |
|----------|-----------|---------|
| **conventional** | Conventional Commits padrão | `feat: adicionar sistema de autenticação` |
| **detailed** | Mensagens detalhadas com contexto | `feat(auth): implementar JWT authentication\n\n- Adicionar middleware de autenticação\n- Criar endpoints de login/logout` |
| **simple** | Mensagens concisas e diretas | `Adicionar autenticação JWT` |
| **semantic** | Semantic commit com escopo | `feat(api): add user authentication endpoints` |
| **gitmoji** | Emojis descritivos + conventional | `✨ feat: adicionar sistema de login` |
| **angular** | Estilo Angular com breaking changes | `feat(core): add authentication module\n\nBREAKING CHANGE: requires new env vars` |
| **atom** | Estilo Atom (imperativo) | `Add user authentication system` |
| **karma** | Estilo Karma com tipo e escopo | `feat(auth): implement JWT tokens` |

### Gerenciar Templates

```bash
# Listar templates disponíveis
commit-ai templates list

# Definir template padrão
commit-ai templates set conventional

# Criar template personalizado
commit-ai templates create meu_template

# Importar/Exportar templates
commit-ai templates export --output templates_backup.json
commit-ai templates import templates_backup.json
```

## 🤖 Provedores de IA

### Provedores Suportados

| Provider | Modelos | Configuração | Status |
|----------|---------|--------------|--------|
| **OpenAI** | GPT-4, GPT-3.5-turbo, GPT-4-turbo | `OPENAI_API_KEY` | ✅ Funcional |
| **Google Gemini** | gemini-pro, gemini-pro-vision | `GEMINI_API_KEY` | ✅ Funcional |
| **Anthropic Claude** | claude-3-sonnet, claude-3-haiku | `ANTHROPIC_API_KEY` | ✅ Funcional |
| **Ollama Local** | llama2, codellama, mistral | Instalação local | ✅ Funcional |

### Configuração de Providers

```bash
# Listar providers disponíveis
commit-ai providers list

# Definir provider padrão
commit-ai providers set openai

# Configurar modelo específico
commit-ai configure --provider gemini --model gemini-pro

# Testar conectividade
commit-ai providers test openai
```

### Configuração Ollama (Local)

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar modelo
ollama pull llama2

# Configurar no Commit-AI
commit-ai providers set ollama --model llama2
```

## 🔌 Sistema de Plugins v1.4.0

### Plugins Disponíveis

| Plugin | Tipo | Descrição | Status |
|--------|------|-----------|--------|
| **custom_local_ai** | AI Provider | Ollama personalizado | ✅ Incluído |
| **enhanced_templates** | Template | Templates avançados | 🔄 Em desenvolvimento |
| **slack_integration** | Integration | Notificações Slack | 🔄 Em desenvolvimento |
| **jira_workflow** | Workflow | Integração Jira | 🔄 Em desenvolvimento |

### Desenvolvimento de Plugins

```bash
# Criar novo plugin
commit-ai plugin create meu_plugin --type ai_provider

# Estrutura gerada:
plugins/meu_plugin.py
├── MeuPluginProvider(AIProviderPlugin)
├── get_info()
├── initialize()  
└── generate_commit_message()
```

## 📊 Analytics e Métricas v1.4.0

### Métricas Coletadas

- **Produtividade**: Commits/dia, frequência, padrões temporais
- **Qualidade**: Score de confiança, tipos mais comuns
- **Performance**: Tempo de processamento por provider
- **Colaboração**: Análise de equipe, entropia de contribuições
- **Uso**: Providers/templates mais utilizados

### Relatórios Disponíveis

```bash
# Dashboard principal
commit-ai analytics

# Métricas específicas
commit-ai analytics --period 30d --provider openai
commit-ai analytics --team --export csv
```

## 📖 Como Funciona

1. **Análise Inteligente**: Verifica repositório Git e analisa mudanças staged
2. **IA Contextual**: Envia diff para provider de IA com prompt otimizado
3. **Geração Profissional**: IA gera mensagem seguindo template escolhido
4. **Interface Rica**: TUI permite seleção visual entre múltiplas opções
5. **Analytics Automáticos**: Coleta métricas de uso e produtividade
6. **Integração Completa**: Git hooks automáticos para workflow seamless

## 🛠️ Estrutura do Projeto v1.4.0

```
Commit-AI/
├── commit_ai/
│   ├── __init__.py              # Módulo principal
│   ├── main.py                  # CLI expandido v1.4.0
│   ├── version.py               # Versionamento e roadmap
│   ├── config_manager.py        # Gerenciamento de configuração
│   ├── git_handler.py           # Integração Git
│   ├── logger.py                # Sistema de logging
│   ├── ai_providers/            # Providers de IA (4 tipos)
│   ├── templates/               # Sistema de templates
│   ├── hooks/                   # Git hooks automáticos
│   ├── tui.py                   # ✨ NOVO: Interface TUI rica
│   ├── analytics.py             # ✨ NOVO: Sistema analytics
│   ├── plugins_system.py        # ✨ NOVO: Framework plugins
│   ├── plugins_cli.py           # ✨ NOVO: CLI de plugins  
│   ├── config_wizard.py         # ✨ NOVO: Wizard setup
│   └── plugins/                 # ✨ NOVO: Plugins extensíveis
│       └── custom_local_ai.py   # Plugin exemplo
├── tests/                       # Suite de testes
├── requirements.txt             # Dependências (+ Rich)
├── .env.example                 # Template configuração
└── docs/                        # Documentação expandida
```

## 🚀 Desenvolvimento

### Setup de Desenvolvimento

```bash
# Clone e configure
git clone https://github.com/boltreskh/Commit-AI.git
cd Commit-AI

# Ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Instalar em modo desenvolvimento
pip install -e .
```

### Testes e Qualidade

```bash
# Executar testes
pytest --cov=commit_ai

# Formatação de código
black commit_ai/

# Verificação de tipos
mypy commit_ai/

# Linting
flake8 commit_ai/
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Configure o ambiente de desenvolvimento
4. Faça suas alterações e adicione testes
5. Execute os testes (`pytest`)
6. Formate o código (`black commit_ai/`)
7. Commit usando o próprio Commit-AI! 😉
8. Push para a branch (`git push origin feature/AmazingFeature`)
9. Abra um Pull Request

## 📈 Changelog v1.4.0

### ✨ NOVIDADES v1.4.0 "Interface Avançada e Analytics" (17/08/2025)

#### 🎨 Terminal User Interface (TUI)
- **Interface interativa rica** com Rich library
- **Seleção múltipla** entre opções de commit
- **Preview detalhado** com syntax highlighting  
- **Temas personalizáveis** e fallback inteligente

#### 📊 Sistema de Analytics Avançados
- **Base SQLite** para métricas persistentes
- **Dashboards visuais** de produtividade
- **Análise por provider/template** com insights
- **Score de colaboração** baseado em entropia
- **Exportação** em JSON/CSV para relatórios

#### 🔌 Framework de Plugins Extensível
- **Arquitetura modular** para 4 tipos de plugins
- **CLI completo** para gerenciamento de plugins
- **Plugin exemplo** (Custom Local AI)
- **Hot-loading** e verificação de dependências

#### 🔧 Wizard de Configuração Interativo
- **Setup guiado** passo-a-passo
- **Interface dupla** (Rich + fallback simples)
- **Detecção automática** de configurações
- **Validação em tempo real** de conectividade

### ⚡ Melhorias de Performance
- **Cache otimizado** com índices SQLite
- **Carregamento lazy** de componentes  
- **Progress indicators** para UX
- **Fallbacks** para dependências opcionais

### 🔄 Retrocompatibilidade 100%
- ✅ Todos os comandos anteriores mantidos
- ✅ Git hooks v1.3.0 funcionais
- ✅ Templates e configurações preservadas
- ✅ APIs e interfaces inalteradas

## 🎯 Próximos Passos (Roadmap)

### 🚀 v1.5.0 - "Interface Gráfica e Colaboração" (Q1 2026)
- 🖥️ Interface gráfica desktop (GUI)
- 🔗 Integração com IDEs (VS Code, JetBrains)
- ☁️ Sincronização em nuvem de configurações
- 🤝 Recursos colaborativos avançados

### 🏢 v2.0.0 - "Versão Empresarial" (Q2 2026)
- 📱 Interface web para configuração
- 🌐 Marketplace de plugins comunitários
- 🔐 Recursos enterprise e compliance
- 🧠 Machine Learning personalizado

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/boltreskh/Commit-AI/issues)
- 📚 **Documentação**: Consulte este README e arquivos em `docs/`
- 💬 **Contato**: lucascanluiz@gmail.com

---

**Desenvolvido com ❤️ e IA por [boltreskh](https://github.com/boltreskh) para desenvolvedores que querem commits melhores!**

⭐ Gostou? Deixe uma estrela no projeto!
