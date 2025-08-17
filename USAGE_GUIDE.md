# 📚 Guia de Uso - Commit-AI v1.2.0

## 🚀 Comandos Principais

### Geração de Commits Básica
```bash
# Geração padrão
commit-ai

# Com provedor específico
commit-ai --api claude
commit-ai --api gemini
commit-ai --api ollama

# Listando provedores disponíveis
commit-ai --list-providers

# Modo preview (não faz commit)
commit-ai --preview

# Auto-commit (sem confirmação)
commit-ai --auto
```

### 🎨 Gerenciamento de Templates

#### Listar Templates
```bash
# Lista todos os templates disponíveis
commit-ai template list

# Mostra detalhes de um template específico
commit-ai template show feat
```

#### Criar Templates Personalizados
```bash
# Adicionar novo template
commit-ai template add hotfix \
  --pattern "hotfix({scope}): {description}" \
  --description "Correção crítica urgente" \
  --example "hotfix(security): corrige vulnerabilidade XSS"

# Múltiplos exemplos
commit-ai template add custom \
  --pattern "custom({scope}): {description}" \
  --description "Tipo personalizado" \
  --example "custom(auth): implementa OAuth" \
  --example "custom(db): otimiza consultas"
```

#### Sugestão Inteligente
```bash
# Sugere tipo baseado no diff atual
commit-ai template suggest

# Sugere tipo baseado em arquivo de diff
commit-ai template suggest --diff-file changes.diff
```

#### Geração com Template
```bash
# Gera mensagem usando template
commit-ai template generate feat "adiciona login social" --scope auth
# Output: feat(auth): adiciona login social

commit-ai template generate fix "corrige bug de validação"
# Output: fix: corrige bug de validação
```

#### Backup e Restauração
```bash
# Exportar templates para backup
commit-ai template export meus-templates.json

# Importar templates (mescla com existentes)
commit-ai template import meus-templates.json

# Importar templates (substitui todos)
commit-ai template import meus-templates.json --replace

# Resetar para templates padrão
commit-ai template reset
```

## 🤖 Configuração de Provedores

### OpenAI
```bash
# No arquivo .env
OPENAI_API_KEY=sk-...

# Modelos suportados: gpt-3.5-turbo, gpt-4, gpt-4-turbo
commit-ai --api openai --model gpt-4
```

### Google Gemini
```bash
# No arquivo .env
GEMINI_API_KEY=...

# Modelos: gemini-pro, gemini-pro-vision
commit-ai --api gemini --model gemini-pro
```

### Anthropic Claude
```bash
# No arquivo .env
ANTHROPIC_API_KEY=sk-ant-...

# Modelos: claude-3-haiku, claude-3-sonnet, claude-3-opus
commit-ai --api claude --model claude-3-sonnet
```

### Ollama (Local)
```bash
# Instalar Ollama primeiro: https://ollama.ai
# Baixar modelo
ollama pull llama2

# Usar com Commit-AI
commit-ai --api ollama --model llama2
```

## ⚙️ Configurações Avançadas

### Parâmetros de IA
```bash
# Criatividade (0.0-1.0)
commit-ai --temperature 0.7

# Limite de tokens
commit-ai --max-tokens 150

# Modo verboso
commit-ai --verbose
```

### Configuração Persistente
```bash
# Definir API padrão
commit-ai --config default_api=claude

# Definir modelo padrão
commit-ai --config default_model=claude-3-sonnet

# Preview padrão
commit-ai --config preview_mode=true

# Configurações salvas em ~/.commit-ai/config.json
```

## 🎯 Exemplos de Templates Padrão

### feat - Nova funcionalidade
```
feat(auth): adiciona autenticação por JWT
feat(ui): implementa componente de botão
feat(api): adiciona endpoint de usuários
```

### fix - Correção de bug
```
fix(login): corrige validação de senha
fix(db): resolve problema de conexão
fix(ui): corrige layout responsivo
```

### docs - Documentação
```
docs(readme): atualiza guia de instalação
docs(api): adiciona documentação dos endpoints
docs(changelog): adiciona release v1.2.0
```

### refactor - Refatoração
```
refactor(auth): simplifica lógica de login
refactor(utils): extrai funções auxiliares
refactor(api): melhora estrutura de rotas
```

### test - Testes
```
test(auth): adiciona testes de login
test(api): implementa testes de integração
test(utils): adiciona testes unitários
```

### chore - Manutenção
```
chore(deps): atualiza dependências
chore(config): ajusta configuração do build
chore(ci): melhora pipeline de deploy
```

### perf - Performance
```
perf(db): otimiza consultas SQL
perf(cache): implementa cache Redis
perf(api): reduz tempo de resposta
```

### style - Formatação
```
style(eslint): corrige warnings de lint
style(format): ajusta indentação do código
style(imports): reorganiza imports
```

## 🔧 Troubleshooting

### Problemas Comuns
```bash
# Provedor não disponível
commit-ai --list-providers  # Verifica quais estão disponíveis

# Template não encontrado
commit-ai template list     # Lista templates disponíveis

# Erro de API key
# Verifique o arquivo .env e as variáveis de ambiente

# Cache corrompido
commit-ai --no-cache       # Força nova consulta à IA
```

### Debug e Logs
```bash
# Modo verboso
commit-ai --verbose

# Logs detalhados em ~/.commit-ai/logs/
```

---
**Desenvolvido com ❤️ - Commit-AI v1.2.0**
