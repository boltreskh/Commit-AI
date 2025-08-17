# 🤖 Commit-AI v1.1.0

Um gerador inteligente de mensagens de commit Git usando IA (OpenAI GPT & Google Gemini).

## ✨ Funcionalidades

### Principais
- **Geração automática de commits**: Analisa suas mudanças e gera mensagens profissionais
- **Multi-provider IA**: Suporte para OpenAI GPT e Google Gemini
- **Sistema de cache inteligente**: Evita requisições desnecessárias à IA
- **Configuração persistente**: Salva suas preferências automaticamente
- **Logs estruturados**: Sistema de logging completo para debug

### Avançadas v1.1.0
- **Sistema de configuração**: Configure suas preferências padrão
- **Cache SQLite**: Cache inteligente com controle de expiração
- **Modo verboso**: Debug detalhado de operações
- **Estatísticas de cache**: Visualize métricas de uso do cache
- **Validação robusta**: Verificação de parâmetros e API keys

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
python -m commit_ai.main

# Preview com Gemini
python -m commit_ai.main --api gemini --preview

# Commit automático com configuração personalizada
python -m commit_ai.main --auto --temperature 0.5 --max-tokens 80
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
│   ├── __init__.py          # Inicialização do pacote (v1.1.0)
│   ├── main.py              # Ponto de entrada principal
│   ├── git_handler.py       # Operações do Git
│   ├── ai_service.py        # Integração com APIs de IA
│   ├── config_manager.py    # 🆕 Gerenciador de configurações
│   └── logger.py            # 🆕 Sistema de logging
├── tests/                   # 🆕 Testes automatizados
│   └── test_git_handler.py  # Testes do GitHandler
├── requirements.txt         # Dependências de produção
├── requirements-dev.txt     # 🆕 Dependências de desenvolvimento
├── pyproject.toml          # Configuração do projeto (v1.1.0)
├── pytest.ini              # 🆕 Configuração de testes
├── setup-dev.sh            # 🆕 Script de setup para desenvolvedores
├── .env.example            # Exemplo de configuração
├── demo.py                 # Script de demonstração
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

### v1.2.0 (Próxima versão)
- [ ] Sistema de cache para respostas da IA
- [ ] Suporte para mais provedores (Claude, Ollama)
- [ ] Templates de commit personalizáveis
- [ ] Integração com hooks do Git

### v2.0.0 (Futuro)
- [ ] Interface gráfica opcional
- [ ] Análise semântica avançada do código
- [ ] Integração com CI/CD
- [ ] Plugin para VS Code

## 📞 Suporte

Se encontrar problemas ou tiver sugestões:
1. Verifique a seção de troubleshooting
2. Abra uma issue no repositório
3. Entre em contato com os mantenedores

---

**Desenvolvido com ❤️ e IA por boltreskh para desenvolvedores que querem commits melhores!**

📧 Contato: lucascanluiz@gmail.com
