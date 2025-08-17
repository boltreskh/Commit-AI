"""
AIService - Serviço para integração com APIs de IA

Este módulo gerencia a comunicação com diferentes provedores de IA
(OpenAI, Google Gemini, Anthropic Claude, Ollama) para gerar mensagens de commit.
"""

import os
import re
from typing import Optional, Dict, Any
import requests
from .logger import logger
from .cache import CommitCache
from .templates import CommitTemplateManager

# Importações condicionais para providers
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.debug("Anthropic não disponível - instale com: pip install anthropic")

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.debug("Ollama não disponível - instale com: pip install ollama")


class AIService:
    """Classe para gerenciar integrações com serviços de IA"""
    
    SUPPORTED_PROVIDERS = {
        'openai': {
            'name': 'OpenAI GPT',
            'models': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
            'default_model': 'gpt-4'
        },
        'gemini': {
            'name': 'Google Gemini',
            'models': ['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash'],
            'default_model': 'gemini-pro'
        },
        'claude': {
            'name': 'Anthropic Claude',
            'models': ['claude-3-5-sonnet-20241022', 'claude-3-haiku-20240307', 'claude-3-opus-20240229'],
            'default_model': 'claude-3-5-sonnet-20241022'
        },
        'ollama': {
            'name': 'Ollama Local',
            'models': ['llama3', 'codellama', 'mistral', 'gemma2'],
            'default_model': 'llama3'
        }
    }
    
    def __init__(self, provider: str = 'openai', model: Optional[str] = None, 
                 max_tokens: int = 100, temperature: float = 0.3, use_cache: bool = True,
                 use_templates: bool = True):
        """
        Inicializa o serviço de IA
        
        Args:
            provider: Provedor de IA ('openai', 'gemini', 'claude', 'ollama')
            model: Modelo específico a usar (opcional)
            max_tokens: Número máximo de tokens na resposta
            temperature: Criatividade da resposta (0.0-1.0)
            use_cache: Se deve usar cache (padrão: True)
            use_templates: Se deve usar templates personalizados (padrão: True)
        """
        self.provider = provider.lower()
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.use_cache = use_cache
        self.use_templates = use_templates
        
        logger.debug(f"Inicializando AIService: provider={provider}, max_tokens={max_tokens}, temperature={temperature}, cache={use_cache}, templates={use_templates}")
        
        # Validar provider
        if self.provider not in self.SUPPORTED_PROVIDERS:
            supported = ', '.join(self.SUPPORTED_PROVIDERS.keys())
            raise ValueError(f"Provider '{provider}' não suportado. Use: {supported}")
        
        # Verificar disponibilidade do provider
        if self.provider == 'claude' and not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic Claude não disponível. Instale com: pip install anthropic")
        
        if self.provider == 'ollama' and not OLLAMA_AVAILABLE:
            raise ImportError("Ollama não disponível. Instale com: pip install ollama")
        
        # Inicializar cache se habilitado
        if self.use_cache:
            self.cache = CommitCache()
        else:
            self.cache = None
        
        # Inicializar sistema de templates se habilitado
        if self.use_templates:
            self.template_manager = CommitTemplateManager()
        else:
            self.template_manager = None
        
        # Configurar modelo padrão se não especificado
        if model is None:
            self.model = self.SUPPORTED_PROVIDERS[self.provider]['default_model']
        else:
            self.model = model
            # Validar se o modelo é suportado pelo provider
            supported_models = self.SUPPORTED_PROVIDERS[self.provider]['models']
            if model not in supported_models:
                logger.warning(f"Modelo '{model}' pode não ser suportado pelo provider '{provider}'. Modelos suportados: {supported_models}")
        
        logger.info(f"AIService configurado: {self.SUPPORTED_PROVIDERS[self.provider]['name']} - {self.model}")
        
        # Inicializar cliente específico do provider
        self._init_provider_client()
    
    def _init_provider_client(self):
        """Inicializa o cliente específico para cada provider"""
        if self.provider == 'openai':
            self._init_openai_client()
        elif self.provider == 'gemini':
            self._init_gemini_client()
        elif self.provider == 'claude':
            self._init_claude_client()
        elif self.provider == 'ollama':
            self._init_ollama_client()
    
    def _init_openai_client(self):
        """Inicializa cliente OpenAI"""
        try:
            import openai
            self.api_key = os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY não configurada")
            
            self.client = openai.OpenAI(api_key=self.api_key)
            logger.debug("Cliente OpenAI inicializado com sucesso")
        except ImportError:
            raise ImportError("OpenAI não disponível. Instale com: pip install openai")
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente OpenAI: {e}")
            raise
    
    def _init_gemini_client(self):
        """Inicializa cliente Gemini"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY não configurada")
        logger.debug("Cliente Gemini inicializado com sucesso")
    
    def _init_claude_client(self):
        """Inicializa cliente Anthropic Claude"""
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic não disponível")
        
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        logger.debug("Cliente Claude inicializado com sucesso")
    
    def _init_ollama_client(self):
        """Inicializa cliente Ollama"""
        if not OLLAMA_AVAILABLE:
            raise ImportError("Ollama não disponível")
        
        # Ollama geralmente roda localmente, sem API key necessária
        try:
            self.client = ollama.Client()
            logger.debug("Cliente Ollama inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar com Ollama: {e}")
            raise ValueError("Ollama não está rodando. Inicie o servidor Ollama.")
    
    @classmethod
    def get_supported_providers(cls) -> Dict[str, Dict[str, Any]]:
        """Retorna informações sobre providers suportados"""
        return cls.SUPPORTED_PROVIDERS.copy()
    
    @classmethod 
    def is_provider_available(cls, provider: str) -> bool:
        """Verifica se um provider está disponível"""
        provider = provider.lower()
        if provider not in cls.SUPPORTED_PROVIDERS:
            return False
        
        if provider == 'claude':
            return ANTHROPIC_AVAILABLE
        elif provider == 'ollama':
            return OLLAMA_AVAILABLE
        else:
            return True  # OpenAI e Gemini são sempre disponíveis
    
    def _get_api_key(self) -> Optional[str]:
        """
        Obtém a API key do provedor configurado
        
        Returns:
            str: API key ou None se não encontrada
        """
        if self.provider == 'openai':
            return os.getenv('OPENAI_API_KEY')
        elif self.provider == 'gemini':
            return os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        return None
    
    def is_configured(self) -> bool:
        """
        Verifica se o serviço está configurado corretamente
        
        Returns:
            bool: True se configurado, False caso contrário
        """
        return self.api_key is not None
    
    def _create_prompt(self, diff_text: str) -> str:
        """
        Cria um prompt otimizado para geração de mensagens de commit
        
        Args:
            diff_text: Diff das alterações do Git
            
        Returns:
            str: Prompt formatado
        """
        prompt = f"""Analise as seguintes alterações de código Git e gere uma mensagem de commit concisa e descritiva em português brasileiro.

REGRAS PARA A MENSAGEM:
1. Use no máximo 72 caracteres
2. Comece com um verbo no imperativo (Add, Fix, Update, Remove, etc.)
3. Seja específico sobre o que foi alterado
4. Não inclua explicações longas
5. Use formato convencional: "tipo: descrição breve"

TIPOS COMUNS:
- feat: nova funcionalidade
- fix: correção de bug
- docs: documentação
- style: formatação
- refactor: refatoração
- test: testes
- chore: tarefas de manutenção

ALTERAÇÕES GIT:
```
{diff_text}
```

MENSAGEM DE COMMIT:"""
        
        return prompt
    
    def _call_openai_api(self, prompt: str) -> str:
        """
        Chama a API da OpenAI
        
        Args:
            prompt: Prompt para a API
            
        Returns:
            str: Resposta da API
            
        Raises:
            Exception: Se a chamada da API falhar
        """
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente especializado em gerar mensagens de commit Git concisas e profissionais."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            message = result['choices'][0]['message']['content'].strip()
            return self._clean_commit_message(message)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na chamada da API OpenAI: {str(e)}")
        except KeyError as e:
            raise Exception(f"Resposta inesperada da API OpenAI: {str(e)}")
    
    def _call_gemini_api(self, prompt: str) -> str:
        """
        Chama a API do Google Gemini
        
        Args:
            prompt: Prompt para a API
            
        Returns:
            str: Resposta da API
            
        Raises:
            Exception: Se a chamada da API falhar
        """
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        params = {
            "key": self.api_key
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": self.max_tokens,
                "temperature": self.temperature
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            message = result['candidates'][0]['content']['parts'][0]['text'].strip()
            return self._clean_commit_message(message)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na chamada da API Gemini: {str(e)}")
        except KeyError as e:
            raise Exception(f"Resposta inesperada da API Gemini: {str(e)}")
    
    def _clean_commit_message(self, message: str) -> str:
        """
        Limpa e formata a mensagem de commit
        
        Args:
            message: Mensagem bruta da IA
            
        Returns:
            str: Mensagem limpa e formatada
        """
        # Remove quebras de linha e espaços extras
        message = re.sub(r'\s+', ' ', message.strip())
        
        # Remove aspas se presentes
        message = message.strip('"\'`')
        
        # Limita o tamanho da mensagem
        if len(message) > 72:
            message = message[:69] + "..."
        
        return message
    
    def generate_commit_message(self, diff_text: str) -> str:
        """
        Gera uma mensagem de commit baseada no diff
        
        Args:
            diff_text: Diff das alterações do Git
            
        Returns:
            str: Mensagem de commit gerada
            
        Raises:
            Exception: Se a geração falhar
        """
        logger.info(f"Gerando commit message com {self.SUPPORTED_PROVIDERS[self.provider]['name']} ({self.model})")
        
        if not diff_text.strip():
            logger.error("Diff vazio fornecido")
            raise Exception("Nenhuma alteração encontrada para analisar")
        
        logger.debug(f"Tamanho do diff: {len(diff_text)} caracteres")
        
        # Verificar cache primeiro (se habilitado)
        if self.cache:
            cached_result = self.cache.get(
                diff_text, self.provider, self.model, 
                self.temperature, self.max_tokens
            )
            if cached_result:
                logger.info("Cache hit - usando resposta em cache")
                return cached_result
        
        # Gerar mensagem usando o provider específico
        try:
            if self.provider == 'openai':
                raw_message = self._generate_openai(diff_text)
            elif self.provider == 'gemini':
                raw_message = self._generate_gemini(diff_text)
            elif self.provider == 'claude':
                raw_message = self._generate_claude(diff_text)
            elif self.provider == 'ollama':
                raw_message = self._generate_ollama(diff_text)
            else:
                raise ValueError(f"Provider {self.provider} não implementado")
            
            # Processar e limpar a mensagem
            processed_message = self._clean_commit_message(raw_message)
            
            # Salvar no cache (se habilitado)
            if self.cache:
                self.cache.set(
                    diff_text, processed_message, self.provider, self.model,
                    self.temperature, self.max_tokens
                )
                logger.debug("Resposta salva no cache")
            
            logger.info("Commit message gerada com sucesso")
            return processed_message
            
        except Exception as e:
            logger.error(f"Erro ao gerar commit message: {e}")
            raise Exception(f"Falha na geração da mensagem: {str(e)}")
    
    def _generate_openai(self, diff_text: str) -> str:
        """Gera commit message usando OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": self._get_enhanced_prompt(diff_text)
                    },
                    {
                        "role": "user", 
                        "content": f"Analise o seguinte diff do Git e gere uma mensagem de commit concisa e profissional:\n\n{diff_text}"
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Erro na API OpenAI: {e}")
            raise
    
    def _generate_gemini(self, diff_text: str) -> str:
        """Gera commit message usando Google Gemini"""
        prompt = f"{self._get_enhanced_prompt(diff_text)}\n\nAnalise o seguinte diff do Git:\n\n{diff_text}"
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        headers = {'Content-Type': 'application/json'}
        
        data = {
            'contents': [{
                'parts': [{'text': prompt}]
            }],
            'generationConfig': {
                'temperature': self.temperature,
                'maxOutputTokens': self.max_tokens
            }
        }
        
        try:
            response = requests.post(f"{url}?key={self.api_key}", headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Erro na API Gemini: {e}")
            raise
    
    def _generate_claude(self, diff_text: str) -> str:
        """Gera commit message usando Anthropic Claude"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self._get_enhanced_prompt(diff_text),
                messages=[
                    {
                        "role": "user",
                        "content": f"Analise o seguinte diff do Git e gere uma mensagem de commit concisa e profissional:\n\n{diff_text}"
                    }
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Erro na API Claude: {e}")
            raise
    
    def _generate_ollama(self, diff_text: str) -> str:
        """Gera commit message usando Ollama"""
        try:
            response = self.client.generate(
                model=self.model,
                prompt=f"{self._get_enhanced_prompt(diff_text)}\n\nAnalise o seguinte diff do Git:\n\n{diff_text}",
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            return response['response'].strip()
        except Exception as e:
            logger.error(f"Erro na API Ollama: {e}")
            raise
    
    def _get_enhanced_prompt(self, diff_text: str = "") -> str:
        """Retorna um prompt aprimorado para gerar commits melhores"""
        base_prompt = """Você é um assistente especializado em gerar mensagens de commit Git profissionais.

Regras para a mensagem de commit:
1. Use o formato: <tipo>: <descrição>
2. Tipos válidos: feat, fix, docs, style, refactor, test, chore, perf, ci, build
3. Máximo 50 caracteres no título
4. Use imperativos (adiciona, corrige, atualiza)
5. Seja específico e claro
6. Use português brasileiro
7. Não use pontos finais no título

Exemplos:
- feat: adiciona sistema de cache SQLite
- fix: corrige validação de entrada do usuário
- docs: atualiza documentação da API
- refactor: melhora estrutura do código de login"""
        
        # Adicionar informações de template se disponível
        if self.template_manager and diff_text:
            suggested_type = self.template_manager.analyze_diff_and_suggest_type(diff_text)
            template = self.template_manager.get_template(suggested_type)
            
            if template:
                base_prompt += f"\n\nTipo sugerido baseado nas alterações: {suggested_type} - {template['description']}"
                base_prompt += f"\nExemplos deste tipo:"
                for example in template['examples'][:2]:  # Mostrar apenas 2 exemplos
                    base_prompt += f"\n- {example}"
        
        base_prompt += "\n\nAnalise as alterações e gere APENAS a mensagem de commit, sem explicações adicionais."
        return base_prompt
