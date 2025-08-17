# 🤖 Commit-AI v1.3.0

Um gerador inteligente de mensagens de commit Git usando IA com suporte a múltiplos provedores, templates personalizados e automação via Git Hooks.

## ✨ Funcionalidades

### Principais
- **Geração automática de commits**: Analisa suas mudanças e gera mensagens profissionais
- **4 Provedores de IA**: OpenAI GPT, Google Gemini, Anthropic Claude, Ollama Local
- **Sistema de templates personalizado**: 8 templates padrão + criação de templates customizados
- **Sistema de cache inteligente**: Evita requisições desnecessárias à IA
- **Configuração persistente**: Salva suas preferências automaticamente
- **Logs estruturados**: Sistema de logging completo para debug

### Avançadas v1.2.0
- **CLI de gerenciamento de templates**: Comandos para criar, modificar e gerenciar templates
- **Análise inteligente de diff**: Sugestão automática de tipo de commit baseada nas mudanças
- **Import/Export de templates**: Backup e compartilhamento de configurações
- **Suporte a modelos locais**: Execute IA localmente com Ollama
- **Sistema de configuração**: Configure suas preferências padrão
- **Cache SQLite**: Cache inteligente com controle de expiração
- **Modo verboso**: Debug detalhado de operações
- **Estatísticas de cache**: Visualize métricas de uso do cache
- **Validação robusta**: Verificação de parâmetros e API keys

### 🆕 NOVIDADES v1.3.0 - Interface e Automação
- **Git Hooks Automáticos**: Integração completa com workflow Git
- **Pre-commit Hook**: Análise automática e sugestão de tipos de commit
- **Commit-msg Hook**: Validação e melhoria automática de mensagens
- **Post-commit Hook**: Analytics e coleta de métricas de projeto
- **CLI de Hooks**: Gerenciamento completo via comando `commit-ai hooks`
- **Auto-melhoria**: Melhoria automática de mensagens durante commit
- **Sistema de Saúde**: Monitoramento da integridade dos hooks
- **Configuração Flexível**: Habilitar/desabilitar hooks individualmente

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- Git instalado e configurado
- Uma API key da OpenAI ou Google Gemini

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Commit-AI
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instale as dependências

**Para uso básico:**
```bash
pip install -r requirements.txt
```

**Para desenvolvimento:**
```bash
pip install -r requirements-dev.txt
```

### 5. Configure a API Key

Crie um arquivo `.env` na raiz do projeto:

```env
# Para OpenAI
OPENAI_API_KEY=sua_api_key_aqui

# Para Google Gemini
GEMINI_API_KEY=sua_api_key_aqui
```

**Ou configure via variável de ambiente:**

```bash
# Windows
set OPENAI_API_KEY=sua_api_key_aqui

# Linux/Mac
export OPENAI_API_KEY=sua_api_key_aqui
```

## 🎯 Como Usar

### Uso Básico

1. Faça suas alterações de código
2. Adicione os arquivos ao staging area:
   ```bash
   git add .
   ```
3. Execute o Commit-AI:
   ```bash
   python -m commit_ai.main
   ```

### Opções Avançadas

```bash
# Usar Google Gemini em vez de OpenAI
python -m commit_ai.main --api gemini

# Apenas visualizar a mensagem (não fazer commit)
python -m commit_ai.main --preview

# Commit automático sem confirmação
python -m commit_ai.main --auto

# Usar modelo específico
python -m commit_ai.main --model gpt-3.5-turbo

# Personalizar criatividade da resposta
python -m commit_ai.main --temperature 0.7

# Limitar tokens da resposta
python -m commit_ai.main --max-tokens 50
```

### Exemplos de Uso

```bash
# Uso padrão com OpenAI GPT-4
python -m commit_ai

# Preview com Gemini
python -m commit_ai --api gemini --preview

# Commit automático com configuração personalizada
python -m commit_ai --auto --temperature 0.5 --max-tokens 80

# Gerenciar templates
python -m commit_ai template list
python -m commit_ai template set conventional

# Instalar e gerenciar Git Hooks (v1.3.0)
python -m commit_ai hooks install --all
python -m commit_ai hooks config --auto-improve
python -m commit_ai hooks status
```

## 🔗 Git Hooks (v1.3.0)

### Instalação de Hooks

```bash
# Instalar todos os hooks automaticamente
commit-ai hooks install --all

# Instalar hooks específicos
commit-ai hooks install --hook pre-commit --hook commit-msg

# Verificar status dos hooks
commit-ai hooks status

# Testar funcionamento de um hook
commit-ai hooks test pre-commit
```

### Configuração de Hooks

```bash
# Ver configurações atuais
commit-ai hooks config

# Habilitar auto-melhoria de mensagens
commit-ai hooks config --auto-improve

# Habilitar/desabilitar hooks
commit-ai hooks config --enable
commit-ai hooks config --disable
```

### Funcionamento dos Hooks

#### Pre-commit Hook
- **Ativação**: Executado automaticamente no `git commit`
- **Funcionalidade**: Analisa alterações e sugere tipo de commit
- **Saída**: Exibe sugestão de tipo (feat, fix, docs, etc.) com nível de confiança

#### Commit-msg Hook
- **Ativação**: Executado após edição da mensagem de commit
- **Funcionalidade**: Valida formato e melhora mensagem automaticamente
- **Auto-melhoria**: Se habilitado, usa IA para melhorar mensagens ruins

#### Post-commit Hook
- **Ativação**: Executado após commit bem-sucedido
- **Funcionalidade**: Coleta analytics e métricas do projeto
- **Analytics**: Padrões de commit, produtividade, sugestões

### Desinstalação de Hooks

```bash
# Remover hook específico
commit-ai hooks uninstall --hook pre-commit

# Remover todos os hooks
commit-ai hooks uninstall --all

# Ver logs dos hooks
commit-ai hooks logs --lines 10
```

## 📖 Como Funciona

1. **Verificação**: O Commit-AI verifica se você está em um repositório Git e se há alterações staged
2. **Análise**: Obtém o diff das alterações via `git diff --cached`
3. **IA**: Envia o diff para a API de IA com um prompt otimizado
4. **Geração**: A IA analisa as alterações e gera uma mensagem de commit apropriada
5. **Confirmação**: Mostra a mensagem e pede confirmação (exceto no modo `--auto`)
6. **Commit**: Executa `git commit` com a mensagem gerada

## 🔧 Configuração

### APIs Suportadas

#### OpenAI
- **Modelos**: gpt-4, gpt-3.5-turbo, gpt-4-turbo
- **API Key**: https://platform.openai.com/api-keys
- **Variável**: `OPENAI_API_KEY`

#### Google Gemini
- **Modelos**: gemini-pro, gemini-pro-vision
- **API Key**: https://makersuite.google.com/app/apikey
- **Variável**: `GEMINI_API_KEY` ou `GOOGLE_API_KEY`

### Parâmetros Personalizáveis

- **model**: Modelo específico da IA
- **temperature**: Criatividade (0.0-1.0, padrão: 0.3)
- **max-tokens**: Tamanho máximo da resposta (padrão: 100)

## 🛠️ Estrutura do Projeto

```
Commit-AI/
├── commit_ai/
│   ├── __init__.py          # Inicialização do pacote (v1.2.0)
│   ├── __main__.py          # Execução como módulo
│   ├── main.py              # Ponto de entrada principal (CLI expandido)
│   ├── git_handler.py       # Operações do Git
│   ├── ai_service.py        # Integração com APIs de IA (4 provedores)
│   ├── templates.py         # Sistema de templates personalizado
│   ├── template_cli.py      # CLI de gerenciamento de templates
│   ├── git_hooks.py         # 🆕 Sistema de Git Hooks automáticos (v1.3.0)
│   ├── hooks_cli.py         # 🆕 CLI de gerenciamento de hooks (v1.3.0)
│   ├── config_manager.py    # Gerenciador de configurações
│   ├── cache.py            # Sistema de cache SQLite
│   ├── version.py           # Sistema de versionamento centralizado
│   └── logger.py            # Sistema de logging
├── tests/                   # Testes automatizados
│   ├── test_git_handler.py  # Testes do GitHandler
│   └── test_git_hooks.py    # 🆕 Testes do sistema de hooks (v1.3.0)
├── requirements.txt         # Dependências de produção
├── requirements-dev.txt     # Dependências de desenvolvimento
├── pyproject.toml          # Configuração do projeto (v1.2.0)
├── pytest.ini              # Configuração de testes
├── setup-dev.sh            # Script de setup para desenvolvedores
├── demo.py                 # Script de demonstração
├── demo_hooks.py           # 🆕 Demonstração de Git Hooks (v1.3.0)
├── .env.example            # Exemplo de configuração
├── CHANGELOG_v1.3.0.md     # 🆕 Changelog da versão atual
├── LICENSE                 # Licença MIT
└── README.md               # Este arquivo
```

## � Desenvolvimento e Testes

### Configuração para Desenvolvedores

```bash
# Configuração automática (Linux/Mac)
./setup-dev.sh

# Configuração manual (Windows)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pip install -e .
```

### Executando Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=commit_ai

# Executar testes específicos
pytest tests/test_git_handler.py

# Executar com verbose
pytest -v
```

### Formatação e Qualidade de Código

```bash
# Formatar código
black commit_ai/

# Verificar tipos
mypy commit_ai/

# Verificar estilo
flake8 commit_ai/
```

## 🔧 Configurações Avançadas

### Sistema de Configuração Persistente

O Commit-AI agora salva suas preferências em `~/.commit-ai/config.json`:

```json
{
  "default_api": "openai",
  "default_model": "gpt-4",
  "temperature": 0.3,
  "max_tokens": 100,
  "commit_types": ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
}
```

### Sistema de Logs

Os logs são salvos automaticamente em `~/.commit-ai/logs/commit-ai.log`:

- **Console**: Mensagens INFO e superiores
- **Arquivo**: Todas as mensagens (DEBUG+)
- **Configurável**: Via código ou environment variables

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Configure o ambiente de desenvolvimento (`./setup-dev.sh` ou manual)
4. Faça suas alterações e adicione testes se necessário
5. Execute os testes (`pytest`)
6. Formate o código (`black commit_ai/`)
7. Commit suas mudanças usando o próprio Commit-AI! 😉
8. Push para a branch (`git push origin feature/AmazingFeature`)
9. Abra um Pull Request

**Desenvolvido por:** boltreskh (lucascanluiz@gmail.com)

## 📈 Changelog

### v1.2.0 (17/08/2025)
- ✨ **NOVO**: Suporte a 4 provedores de IA (OpenAI, Gemini, Claude, Ollama)
- ✨ **NOVO**: Sistema completo de templates personalizados (8 padrão + custom)
- ✨ **NOVO**: CLI de gerenciamento de templates (`commit-ai template`)
- ✨ **NOVO**: Análise inteligente de diff para sugestão de tipos
- ✨ **NOVO**: Import/export de templates em JSON
- ✨ **NOVO**: Execução como módulo (`python -m commit_ai`)
- 🔧 **MELHORIA**: AIService expandido com arquitetura modular
- 🔧 **MELHORIA**: Integração seamless entre templates e IA

### v1.1.0 (17/08/2025)
- ✨ **NOVO**: Sistema de configuração persistente (`config_manager.py`)
- ✨ **NOVO**: Sistema de logging estruturado (`logger.py`)
- ✨ **NOVO**: Suite de testes automatizados com pytest
- ✨ **NOVO**: Dependências de desenvolvimento (`requirements-dev.txt`)
- ✨ **NOVO**: Script de setup para desenvolvedores (`setup-dev.sh`)
- ✨ **NOVO**: Configuração de testes com cobertura (`pytest.ini`)
- 📚 **MELHORIA**: Documentação expandida com seções de desenvolvimento
- 🔧 **MELHORIA**: Estrutura de projeto mais organizada

### v1.0.0 (17/08/2025)
- 🎉 **LANÇAMENTO**: Versão inicial do Commit-AI
- 🤖 Geração de commits com OpenAI GPT e Google Gemini
- 👀 Modo preview e commit automático
- 🛠️ Interface CLI completa com Click
- 📝 Documentação abrangente

## 🤝 Contribuindo

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🐛 Problemas Conhecidos

- Mensagens muito longas são truncadas em 72 caracteres
- Requer conexão com internet para acessar as APIs
- APIs têm limites de uso que podem afetar a funcionalidade

## 🎯 Roadmap

### ✅ v1.2.0 (Implementado - 17/08/2025)
- [x] **Suporte para mais provedores de IA**
  - [x] Anthropic Claude (claude-3-sonnet, claude-3-haiku, claude-3-opus)
  - [x] Ollama local (llama2, codellama, mistral, etc.)
- [x] **Sistema de templates personalizados**
  - [x] 8 templates padrão (feat, fix, docs, style, refactor, test, chore, perf)
  - [x] Criação de templates customizados
  - [x] Análise inteligente de diff para sugestão automática
  - [x] Import/export de templates em JSON
- [x] **CLI expandido**
  - [x] Subcomandos para gerenciamento (`commit-ai template`)
  - [x] Execução como módulo Python (`python -m commit_ai`)

### ✅ v1.1.0 (Implementado - 17/08/2025)
- [x] **Sistema de cache SQLite inteligente** - Cache baseado em hash com controle de expiração
- [x] **Configurações persistentes** - Sistema de config JSON em ~/.commit-ai/
- [x] **Logging estruturado** - Logs detalhados em console e arquivo
- [x] **Suite de testes automatizados** - pytest + coverage completo
- [x] **CLI aprimorado** - Modo verbose, cache-stats, validação robusta
- [x] **Cache management CLI** - Ferramentas para gerenciar cache

### 🚀 v1.3.0 - Interface e Automação (Em desenvolvimento)
- [x] **Git Hooks automáticos**
  - [x] Pre-commit hook para análise automática
  - [x] Commit-msg hook para validação e melhoria
  - [x] Post-commit hook para analytics
- [x] **CLI de gerenciamento de hooks**
  - [x] Instalação/desinstalação de hooks
  - [x] Configuração e testes de hooks
  - [x] Sistema de saúde e logs
- [ ] **Interface gráfica (GUI)**
  - [ ] Aplicativo desktop com Tkinter/PyQt
  - [ ] Preview visual de mudanças
- [ ] **TUI (Terminal UI) interativa**
  - [ ] Interface de seleção visual
  - [ ] Preview com syntax highlighting
  - [ ] Wizard de configuração inicial

### 🔧 v1.4.0 (Q2 2026)
- [ ] **Integração com ferramentas de desenvolvimento**
  - [ ] Plugin para VS Code
  - [ ] Extensão para JetBrains IDEs
  - [ ] Integração com GitHub CLI
- [ ] **Recursos colaborativos**
  - [ ] Templates compartilhados por equipe
  - [ ] Consistency checks entre desenvolvedores
  - [ ] Estatísticas de usage por projeto

### 🏢 v2.0.0 (Q3 2026) - Versão Empresarial
- [ ] **Interface gráfica multiplataforma**
  - [ ] GUI desktop (Electron/Tauri)
  - [ ] Web interface para configuração
  - [ ] Mobile app para review
- [ ] **Recursos empresariais**
  - [ ] Integração com CI/CD (GitHub Actions, GitLab, Jenkins)
  - [ ] Analytics e relatórios de commit quality
  - [ ] Compliance e audit trails
- [ ] **IA avançada**
  - [ ] Fine-tuning em código da empresa
  - [ ] Análise semântica de mudanças
  - [ ] Sugestões de refactoring baseadas em commits

### 🔮 Futuro (v2.1.0+)
- [ ] **Machine Learning personalizado**
  - [ ] Modelo treinado no estilo de commits da equipe
  - [ ] Predição de impacto de mudanças
  - [ ] Auto-categorização de commits
- [ ] **Integrações avançadas**
  - [ ] Jira/Linear ticket linking
  - [ ] Slack/Teams notifications
  - [ ] Code review automation

## 📞 Suporte

Se encontrar problemas ou tiver sugestões:
1. Verifique a seção de troubleshooting
2. Abra uma issue no repositório
3. Entre em contato com os mantenedores

---

**Desenvolvido com ❤️ e IA por boltreskh para desenvolvedores que querem commits melhores!**

📧 Contato: lucascanluiz@gmail.com
