"""
Commit-AI - Gerador inteligente de mensagens de commit usando IA

Um assistente CLI que analisa suas mudanças de código e gera
mensagens de commit profissionais usando OpenAI GPT ou Google Gemini.
"""

from .version import VERSION, get_version, get_version_info

__version__ = VERSION
__author__ = "boltreskh"
__email__ = "lucascanluiz@gmail.com"
__license__ = "MIT"

def version_info():
    """Informações detalhadas da versão atual"""
    return get_version_info()

# Metadados do pacote
__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__license__",
    "version_info"
]
