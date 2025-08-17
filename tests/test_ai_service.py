"""
Testes para o AIService

Testa funcionalidades do serviço de IA com mocks.
"""

import pytest
from unittest.mock import patch, MagicMock
from commit_ai.ai_service import AIService


class TestAIService:
    """Classe de testes para AIService"""
    
    def test_init_openai_default(self):
        """Testa inicialização com OpenAI (padrão)"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai')
            
            assert service.provider == 'openai'
            assert service.model == 'gpt-4'
            assert service.temperature == 0.3
            assert service.max_tokens == 100
    
    def test_init_gemini(self):
        """Testa inicialização com Gemini"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            service = AIService(provider='gemini')
            
            assert service.provider == 'gemini'
            assert service.model == 'gemini-pro'
    
    def test_init_custom_model(self):
        """Testa inicialização com modelo customizado"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai', model='gpt-3.5-turbo')
            
            assert service.model == 'gpt-3.5-turbo'
    
    def test_init_invalid_provider(self):
        """Testa inicialização com provedor inválido"""
        with pytest.raises(ValueError, match="Provedor não suportado"):
            AIService(provider='invalid-provider')
    
    def test_is_configured_true(self):
        """Testa is_configured quando API key está presente"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai')
            assert service.is_configured() is True
    
    def test_is_configured_false(self):
        """Testa is_configured quando API key não está presente"""
        with patch.dict('os.environ', {}, clear=True):
            service = AIService(provider='openai')
            assert service.is_configured() is False
    
    def test_create_prompt(self):
        """Testa criação de prompt"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai')
            
            diff = "diff --git a/test.py b/test.py\n+print('hello')"
            prompt = service._create_prompt(diff)
            
            assert "MENSAGEM DE COMMIT:" in prompt
            assert diff in prompt
            assert "REGRAS PARA A MENSAGEM:" in prompt
    
    def test_clean_commit_message(self):
        """Testa limpeza de mensagem de commit"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai')
            
            # Teste com aspas
            result = service._clean_commit_message('"feat: add new feature"')
            assert result == "feat: add new feature"
            
            # Teste com quebras de linha
            result = service._clean_commit_message("feat: add\nnew\nfeature")
            assert result == "feat: add new feature"
            
            # Teste com truncamento
            long_message = "feat: " + "a" * 70
            result = service._clean_commit_message(long_message)
            assert len(result) <= 72
            assert result.endswith("...")
    
    @patch('requests.post')
    def test_call_openai_api_success(self, mock_post):
        """Testa chamada bem-sucedida da API OpenAI"""
        # Mock da resposta da API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'feat: add new feature'
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai')
            result = service._call_openai_api("test prompt")
            
            assert result == "feat: add new feature"
            mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_call_gemini_api_success(self, mock_post):
        """Testa chamada bem-sucedida da API Gemini"""
        # Mock da resposta da API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [
                {
                    'content': {
                        'parts': [
                            {
                                'text': 'fix: correct validation logic'
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            service = AIService(provider='gemini')
            result = service._call_gemini_api("test prompt")
            
            assert result == "fix: correct validation logic"
            mock_post.assert_called_once()
    
    def test_generate_commit_message_not_configured(self):
        """Testa geração quando não configurado"""
        with patch.dict('os.environ', {}, clear=True):
            service = AIService(provider='openai')
            
            with pytest.raises(Exception, match="API key.*não configurada"):
                service.generate_commit_message("test diff")
    
    def test_generate_commit_message_empty_diff(self):
        """Testa geração com diff vazio"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai')
            
            with pytest.raises(Exception, match="Nenhuma alteração encontrada"):
                service.generate_commit_message("")
    
    @patch('commit_ai.ai_service.AIService._call_openai_api')
    def test_generate_commit_message_success(self, mock_call_api):
        """Testa geração bem-sucedida"""
        mock_call_api.return_value = "feat: add new functionality"
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai', use_cache=False)
            result = service.generate_commit_message("test diff content")
            
            assert result == "feat: add new functionality"
            mock_call_api.assert_called_once()
    
    @patch('commit_ai.ai_service.AIService._call_openai_api')
    def test_generate_commit_message_with_cache(self, mock_call_api):
        """Testa geração com cache habilitado"""
        mock_call_api.return_value = "feat: cached response"
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            service = AIService(provider='openai', use_cache=True)
            
            # Primeira chamada - deve chamar a API
            result1 = service.generate_commit_message("test diff for cache")
            assert result1 == "feat: cached response"
            assert mock_call_api.call_count == 1
            
            # Segunda chamada com mesmo diff - deve usar cache
            result2 = service.generate_commit_message("test diff for cache") 
            assert result2 == "feat: cached response"
            # API não deve ser chamada novamente
            assert mock_call_api.call_count == 1


if __name__ == '__main__':
    pytest.main([__file__])
