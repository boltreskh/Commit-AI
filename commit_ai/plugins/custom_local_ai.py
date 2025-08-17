#!/usr/bin/env python3
"""
Plugin de exemplo: Custom Local AI Provider
Demonstra como criar um provider de IA personalizado usando Ollama local.
"""

from typing import Dict, List, Any
import requests
import json
from pathlib import Path
import sys

# Adicionar caminho para importar do Commit-AI
sys.path.append(str(Path(__file__).parent.parent))

from plugins_system import AIProviderPlugin


class CustomLocalAI(AIProviderPlugin):
    """Provider customizado usando IA local (Ollama)"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "codellama:7b"
        self.available = self._check_availability()
    
    def get_info(self) -> Dict[str, Any]:
        """Informações do plugin"""
        return {
            'name': 'custom_local_ai',
            'version': '1.0.0',
            'description': 'Provider de IA local customizado usando Ollama CodeLlama',
            'author': 'Commit-AI Team',
            'category': 'ai_provider',
            'dependencies': ['requests']
        }
    
    def initialize(self) -> bool:
        """Inicializa o provider"""
        try:
            self.available = self._check_availability()
            if self.available:
                print(f"✅ Custom Local AI inicializado (modelo: {self.model})")
                return True
            else:
                print("❌ Ollama não está rodando ou modelo não disponível")
                return False
        except Exception as e:
            print(f"❌ Erro ao inicializar Custom Local AI: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Limpa recursos"""
        return True
    
    def _check_availability(self) -> bool:
        """Verifica se Ollama está rodando e modelo disponível"""
        try:
            # Verificar se Ollama está rodando
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                return False
            
            # Verificar se modelo está disponível
            models = response.json().get('models', [])
            available_models = [m['name'] for m in models]
            
            return any(self.model in model for model in available_models)
            
        except:
            return False
    
    def is_available(self) -> bool:
        """Verifica se o provider está disponível"""
        return self.available
    
    def get_supported_models(self) -> List[str]:
        """Retorna modelos suportados"""
        return [
            "codellama:7b",
            "codellama:13b", 
            "codellama:34b",
            "llama2:7b",
            "llama2:13b",
            "mistral:7b"
        ]
    
    def generate_commit_message(self, 
                               diff: str, 
                               template: str = "conventional",
                               **kwargs) -> str:
        """Gera mensagem de commit usando IA local"""
        if not self.is_available():
            raise Exception("Custom Local AI não está disponível")
        
        # Criar prompt específico para commits
        prompt = self._build_commit_prompt(diff, template)
        
        try:
            # Fazer requisição para Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get('temperature', 0.3),
                        "top_p": kwargs.get('top_p', 0.9),
                        "max_tokens": kwargs.get('max_tokens', 100)
                    }
                },
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"Erro na API Ollama: {response.status_code}")
            
            result = response.json()
            message = result.get('response', '').strip()
            
            # Processar resposta para extrair apenas a mensagem de commit
            return self._extract_commit_message(message)
            
        except Exception as e:
            raise Exception(f"Erro ao gerar mensagem com Custom Local AI: {e}")
    
    def _build_commit_prompt(self, diff: str, template: str) -> str:
        """Constrói prompt para geração de commit"""
        template_instructions = {
            'conventional': '''Use o formato Conventional Commits:
tipo(escopo): descrição breve

Onde tipo pode ser: feat, fix, docs, style, refactor, test, chore''',
            
            'angular': '''Use o formato Angular:
tipo(escopo): descrição breve

Inclua corpo detalhado se necessário.
Tipos: feat, fix, docs, style, refactor, perf, test, chore''',
            
            'gitmoji': '''Use emojis do Gitmoji seguido da descrição:
:emoji: descrição breve

Escolha emoji apropriado para o tipo de mudança.'''
        }
        
        instruction = template_instructions.get(template, template_instructions['conventional'])
        
        prompt = f"""Você é um assistente especializado em gerar mensagens de commit Git.

Instruções de formato:
{instruction}

Analise as seguintes mudanças de código e gere UMA mensagem de commit concisa e descritiva:

```diff
{diff[:2000]}  # Limitar tamanho do diff
```

IMPORTANTE:
- Responda APENAS com a mensagem de commit
- Seja conciso e descritivo
- Use português
- Máximo 50 caracteres na primeira linha
- NÃO inclua explicações ou comentários extras

Mensagem de commit:"""

        return prompt
    
    def _extract_commit_message(self, response: str) -> str:
        """Extrai mensagem de commit da resposta da IA"""
        # Limpar resposta
        message = response.strip()
        
        # Remover possíveis prefixos comuns
        prefixes_to_remove = [
            "Mensagem de commit:",
            "Commit:",
            "```",
            "Resposta:",
            "A mensagem de commit seria:"
        ]
        
        for prefix in prefixes_to_remove:
            if message.startswith(prefix):
                message = message[len(prefix):].strip()
        
        # Pegar apenas primeira linha se houver múltiplas
        lines = message.split('\n')
        first_line = lines[0].strip()
        
        # Verificar se tem corpo (segunda linha em branco, terceira com conteúdo)
        if len(lines) >= 3 and lines[1].strip() == '' and lines[2].strip():
            return first_line + '\n\n' + lines[2].strip()
        
        return first_line
    
    def set_model(self, model: str) -> bool:
        """Define modelo a ser usado"""
        if model in self.get_supported_models():
            self.model = model
            return True
        return False
    
    def get_current_model(self) -> str:
        """Retorna modelo atual"""
        return self.model


if __name__ == "__main__":
    # Teste do plugin
    plugin = CustomLocalAI()
    
    print("Informações do plugin:")
    info = plugin.get_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print(f"\nDisponível: {plugin.is_available()}")
    print(f"Modelos suportados: {plugin.get_supported_models()}")
    
    if plugin.initialize():
        # Teste de geração (diff simulado)
        test_diff = """
+def authenticate_user(username: str, password: str) -> bool:
+    \"\"\"Autentica usuário no sistema\"\"\"
+    if not username or not password:
+        return False
+    
+    return check_credentials(username, password)
"""
        
        try:
            message = plugin.generate_commit_message(test_diff, "conventional")
            print(f"\nMensagem gerada: {message}")
        except Exception as e:
            print(f"Erro no teste: {e}")
        
        plugin.cleanup()
    else:
        print("Falha na inicialização do plugin")
