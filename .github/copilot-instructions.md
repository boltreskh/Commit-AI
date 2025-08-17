# Commit-AI - Instruções do Copilot

## Projeto
Um assistente CLI que gera mensagens de commit para o Git usando IA.

## Autor
**boltreskh** (lucascanluiz@gmail.com)

## Versão Atual
**v1.2.0** - Atualizada em 17/08/2025

## Status do Projeto
✅ PROJETO COMPLETAMENTE CONFIGURADO E FUNCIONAL

## Estrutura
- `commit_ai/` - Pacote principal com CLI expandido, múltiplos provedores AI e sistema de templates
- Suporte para OpenAI GPT, Google Gemini, Anthropic Claude e Ollama local
- Sistema completo de templates personalizado com 8 padrões + customização
- Interface CLI completa com subcomandos para gerenciamento
- Documentação abrangente no README.md
- Script de demonstração incluído
- Licença MIT

## Como Usar
1. Configure API key em arquivo .env (OpenAI/Gemini/Claude) ou instale Ollama
2. Execute: `git add .` para staging
3. Execute: `commit-ai` ou `python -m commit_ai` para gerar commits
4. Use: `commit-ai template list` para gerenciar templates

## Funcionalidades Implementadas
- Geração inteligente de commits via IA (4 provedores)
- Sistema completo de templates personalizado (8 padrão + custom)
- Suporte múltiplas APIs (OpenAI/Gemini/Claude/Ollama)
- CLI de gerenciamento de templates
- Análise de diff para sugestão automática de tipos
- Modo preview e auto-commit
- Configuração de modelo e parâmetros
- Tratamento completo de erros
- Interface de usuário amigável
- Sistema de configuração persistente
- Logging estruturado
- Testes automatizados
