# Commit-AI 🤖

Um assistente de linha de comando (CLI) inteligente que gera mensagens de commit para o Git usando Inteligência Artificial.

## 📋 Sobre o Projeto

O **Commit-AI** analisa suas alterações de código (via `git diff`) e utiliza APIs de IA (OpenAI GPT ou Google Gemini) para gerar mensagens de commit profissionais, concisas e descritivas automaticamente.

## ✨ Funcionalidades

- 🤖 **Geração Inteligente**: Usa IA para criar mensagens de commit baseadas nas alterações do código
- 🔄 **Múltiplos Provedores**: Suporte para OpenAI GPT e Google Gemini
- 🎯 **Formato Convencional**: Segue padrões de commit convencionais
- 👀 **Modo Preview**: Visualize a mensagem antes de fazer o commit
- ⚡ **Modo Automático**: Commit automático sem confirmação
- 🛠️ **Configurável**: Personalize modelo, temperatura e outros parâmetros

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

```bash
pip install -r requirements.txt
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
│   ├── __init__.py          # Inicialização do pacote
│   ├── main.py              # Ponto de entrada principal
│   ├── git_handler.py       # Operações do Git
│   └── ai_service.py        # Integração com APIs de IA
├── requirements.txt         # Dependências
├── pyproject.toml          # Configuração do projeto
├── .env.example            # Exemplo de configuração
└── README.md               # Este arquivo
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças usando o próprio Commit-AI! 😉
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

**Desenvolvido por:** boltreskh (lucascanluiz@gmail.com)

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🐛 Problemas Conhecidos

- Mensagens muito longas são truncadas em 72 caracteres
- Requer conexão com internet para acessar as APIs
- APIs têm limites de uso que podem afetar a funcionalidade

## 📞 Suporte

Se encontrar problemas ou tiver sugestões:
1. Verifique a seção de troubleshooting
2. Abra uma issue no repositório
3. Entre em contato com os mantenedores

---

**Desenvolvido com ❤️ e IA por boltreskh para desenvolvedores que querem commits melhores!**

📧 Contato: lucascanluiz@gmail.com
