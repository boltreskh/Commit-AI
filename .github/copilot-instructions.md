# Commit-AI - Instruções do Copilot

## Projeto
Um assistente CLI que gera mensagens de commit para o Git usando IA.

## Autor
**boltreskh** (lucascanluz@gmail.com)

## Status do Projeto
✅ PROJETO COMPLETAMENTE CONFIGURADO E FUNCIONAL

## Estrutura
- `commit_ai/` - Pacote principal com CLI, Git handler e AI service
- Suporte para OpenAI GPT e Google Gemini  
- Interface CLI completa com múltiplas opções
- Documentação abrangente no README.md
- Script de demonstração incluído
- Licença MIT

## Como Usar
1. Configure API key em arquivo .env
2. Execute: `git add .` para staging
3. Execute: `python -m commit_ai.main` para gerar commits

## Funcionalidades Implementadas
- Geração inteligente de commits via IA
- Suporte múltiplas APIs (OpenAI/Gemini)
- Modo preview e auto-commit
- Configuração de modelo e parâmetros
- Tratamento completo de erros
- Interface de usuário amigável
