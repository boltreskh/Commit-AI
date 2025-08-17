# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-08-17

### ✨ Adicionado
- Sistema de configuração persistente (`config_manager.py`)
  - Configurações salvas em `~/.commit-ai/config.json`
  - Preferências de API, modelo, temperatura e outros parâmetros
  - Função de reset para valores padrão
- Sistema de logging estruturado (`logger.py`)
  - Logs no console (INFO+) e arquivo (DEBUG+)
  - Arquivos de log salvos em `~/.commit-ai/logs/`
  - Formatação diferenciada para console e arquivo
- Suite de testes automatizados
  - `tests/test_git_handler.py` - Testes para operações Git
  - Configuração com pytest, coverage e mocks
  - Setup de repositórios temporários para testes
- Ambiente de desenvolvimento aprimorado
  - `requirements-dev.txt` - Dependências para desenvolvimento
  - `pytest.ini` - Configuração de testes com cobertura
  - `setup-dev.sh` - Script de configuração automática
  - Integração com Black, MyPy e Flake8

### 📚 Melhorado
- Documentação expandida no README.md
  - Seção de desenvolvimento e testes
  - Guia de contribuição detalhado
  - Changelog integrado
  - Roadmap do projeto
- Estrutura de projeto reorganizada
  - Melhor separação de responsabilidades
  - Documentação de cada módulo
- Versionamento semântico implementado
  - Versão atualizada em todos os arquivos relevantes
  - Metadados do projeto atualizados

### 🔧 Técnico
- Atualização da versão para 1.1.0
- Correção do email do autor (lucascanluiz@gmail.com)
- Estrutura preparada para futuras funcionalidades

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
