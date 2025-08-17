# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-08-17

### ✨ Adicionado
- **Suporte a múltiplos provedores de IA**
  - Anthropic Claude (claude-3-haiku, claude-3-sonnet, claude-3-opus)
  - Ollama local (llama2, codellama, mistral, e outros modelos open-source)
  - Arquitetura modular expandida no `ai_service.py`
  - Detecção automática de disponibilidade de provedores
- **Sistema completo de templates personalizado** (`templates.py`)
  - 8 templates padrão: feat, fix, docs, style, refactor, test, chore, perf
  - Criação e gerenciamento de templates customizados
  - Persistência em JSON com configuração flexível
  - Análise inteligente de diff para sugestão automática de tipos
- **CLI de gerenciamento de templates** (`template_cli.py`)
  - `commit-ai template list` - Lista todos os templates disponíveis
  - `commit-ai template add` - Adiciona templates personalizados
  - `commit-ai template remove` - Remove templates customizados
  - `commit-ai template suggest` - Sugere tipo baseado no diff
  - `commit-ai template generate` - Gera mensagem usando template
  - `commit-ai template export/import` - Backup e restauração
- **Execução como módulo Python** (`__main__.py`)
  - Comando `python -m commit_ai` funcional
  - Integração seamless com CLI principal
- **Arquitetura CLI expandida**
  - CLI principal transformado em grupo de comandos
  - Subcomandos organizados e estruturados
  - Compatibilidade total com versões anteriores

### 🔧 Melhorado
- **AIService expandido**
  - Refatoração completa com método por provedor
  - Tratamento de erros específico para cada API
  - Integração nativa com sistema de templates
  - Validação robusta de credenciais e modelos
- **Sistema de prompt inteligente**
  - Templates integrados na geração de prompts
  - Análise de contexto baseada em diff
  - Sugestões automáticas de escopo e tipo

### 📦 Dependências
- Adicionado `anthropic>=0.3.0` para suporte ao Claude
- Adicionado `ollama>=0.1.0` para modelos locais
- Atualização nas dependências do projeto

## [1.1.0] - 2025-08-17

### ✨ Adicionado
- **Sistema de cache inteligente** (`cache.py`)
  - Cache SQLite com chaves baseadas em hash do diff
  - Controle automático de expiração (24h padrão)
  - Economia significativa de chamadas para APIs de IA
  - Estatísticas de uso e performance
- **Sistema de configuração persistente** (`config_manager.py`)
  - Configurações salvas em `~/.commit-ai/config.json`
  - Preferências de API, modelo, temperatura e outros parâmetros
  - Função de reset para valores padrão
  - Configuração via CLI: `--config key=value`
- **Sistema de logging estruturado** (`logger.py`)
  - Logs no console (INFO+) e arquivo (DEBUG+)
  - Arquivos de log salvos em `~/.commit-ai/logs/`
  - Formatação diferenciada para console e arquivo
  - Modo verbose com `--verbose` flag
- **CLI de gerenciamento de cache** (`cache_cli.py`)
  - Comando `cache-stats` para estatísticas
  - Comandos para limpar e gerenciar cache
  - Informações detalhadas do sistema de cache
- **Suite de testes automatizados**
  - `tests/test_git_handler.py` - Testes para operações Git
  - `tests/test_cache.py` - Testes para sistema de cache
  - `tests/test_ai_service.py` - Testes para integração IA
  - Configuração com pytest, coverage e mocks
  - Setup de repositórios temporários para testes
- **Validação robusta de parâmetros**
  - Verificação de tipos e ranges para temperature/max_tokens
  - Mensagens de erro mais informativas
  - Tratamento de edge cases

### 📚 Melhorado
- **CLI principal aprimorado** (`main.py`)
  - Nova opção `--verbose` para debug detalhado
  - Nova opção `--no-cache` para bypass do cache
  - Nova opção `--cache-stats` para visualizar estatísticas
  - Melhor feedback visual com emojis e cores
  - Tratamento de erros mais robusto
- **Documentação expandida** (README.md)
  - Seção de desenvolvimento e testes
  - Guia de contribuição detalhado
  - Roadmap atualizado e detalhado
  - Exemplos de uso completos
  - FAQ e troubleshooting
- **Estrutura de projeto reorganizada**
  - Melhor separação de responsabilidades
  - Documentação de cada módulo
  - Configuração de desenvolvimento padronizada
- **Ambiente de desenvolvimento aprimorado**
  - `requirements-dev.txt` - Dependências para desenvolvimento
  - `pytest.ini` - Configuração de testes com cobertura
  - Integração com Black, MyPy e Flake8
  - Scripts de automação

### 🔧 Técnico
- Atualização da versão para 1.1.0 em todos os arquivos
- Correção do email do autor (lucascanluiz@gmail.com)
- Estrutura preparada para futuras funcionalidades
- Melhoria na arquitetura modular
- Performance otimizada com sistema de cache
- Logging para debugging e monitoramento

## [1.0.0] - 2025-08-17

### 🎉 Lançamento Inicial
- Geração inteligente de mensagens de commit usando IA
- Suporte para OpenAI GPT-4 e Google Gemini
- Interface CLI completa com Click
- Múltiplos modos de operação:
  - Modo normal com confirmação
  - Modo preview (apenas visualizar)
  - Modo automático (sem confirmação)
- Configuração flexível de parâmetros:
  - Escolha do provedor de IA
  - Modelo específico
  - Temperatura (criatividade)
  - Número máximo de tokens
- Integração completa com Git:
  - Detecção de repositório
  - Análise de alterações staged
  - Geração de diff para análise da IA
  - Commit automático
- Sistema de tratamento de erros robusto
- Documentação abrangente
- Script de demonstração
- Licença MIT
- Configuração via arquivo .env
- Suporte multiplataforma (Windows, Linux, Mac)

### 📦 Dependências
- click>=8.1.0 (Interface CLI)
- requests>=2.31.0 (Requisições HTTP)
- openai>=1.0.0 (API OpenAI)
- python-dotenv>=1.0.0 (Variáveis de ambiente)
- gitpython>=3.1.40 (Integração Git)

---

## 🎯 Roadmap de Versões Futuras

### [1.2.0] - Planejado para Q4 2025
- **Suporte para mais provedores de IA**
  - Anthropic Claude (claude-3-sonnet, claude-3-haiku)
  - Ollama local (llama3, codellama, mistral)
  - Cohere Command
- **Templates de commit personalizáveis**
  - Sistema de templates com variáveis
  - Templates por tipo de projeto
  - Import/export de templates
- **Integração avançada com Git**
  - Git hooks automáticos
  - Análise de branch e contexto do PR

### [1.3.0] - Planejado para Q1 2026
- **Interface e UX melhorados**
  - TUI (Terminal UI) interativa
  - Preview com syntax highlighting
  - Wizard de configuração inicial
- **Análise de código aprimorada**
  - Detecção de linguagem
  - Context awareness por tipo de arquivo

### [2.0.0] - Planejado para Q3 2026
- **Interface gráfica multiplataforma**
- **Recursos empresariais**
- **Integração com CI/CD**
- **IA avançada e análise semântica**

---

## Padrão de Versionamento

Este projeto segue o [Semantic Versioning](https://semver.org/):
- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Funcionalidades adicionadas de forma compatível
- **PATCH**: Correções de bugs compatíveis

## Tipos de Mudanças
- `✨ Adicionado` para novas funcionalidades
- `📚 Melhorado` para mudanças em funcionalidades existentes
- `🐛 Corrigido` para correções de bugs
- `🔧 Técnico` para mudanças que não afetam o usuário final
- `❌ Removido` para funcionalidades removidas
- `🔒 Segurança` para vulnerabilidades corrigidas
