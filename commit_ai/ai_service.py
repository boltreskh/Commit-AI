"""
AIService - Serviço para integração com APIs de IA

Este módulo gerencia a comunicação com diferentes provedores de IA
(OpenAI, Google Gemini) para gerar mensagens de commit.
"""

import os
import re
from typing import Optional
import requests


class AIService:
    """Classe para gerenciar integrações com serviços de IA"""
    
    def __init__(self, provider: str = 'openai', model: Optional[str] = None, 
                 max_tokens: int = 100, temperature: float = 0.3):
        """
        Inicializa o serviço de IA
        
        Args:
            provider: Provedor de IA ('openai' ou 'gemini')
            model: Modelo específico a usar (opcional)
            max_tokens: Número máximo de tokens na resposta
            temperature: Criatividade da resposta (0.0-1.0)
        """
        self.provider = provider.lower()
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Configurar modelo padrão se não especificado
        if model is None:
            if self.provider == 'openai':
                self.model = 'gpt-4'
            elif self.provider == 'gemini':
                self.model = 'gemini-pro'
            else:
                raise ValueError(f"Provedor não suportado: {provider}")
        else:
            self.model = model
        
        # Configurar API key
        self.api_key = self._get_api_key()
    
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
        if not self.is_configured():
            raise Exception(f"API key para {self.provider} não configurada")
        
        if not diff_text.strip():
            raise Exception("Nenhuma alteração encontrada para analisar")
        
        prompt = self._create_prompt(diff_text)
        
        if self.provider == 'openai':
            return self._call_openai_api(prompt)
        elif self.provider == 'gemini':
            return self._call_gemini_api(prompt)
        else:
            raise Exception(f"Provedor não suportado: {self.provider}")
