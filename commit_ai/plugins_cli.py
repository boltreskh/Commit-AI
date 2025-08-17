#!/usr/bin/env python3
"""
CLI para gerenciamento de Plugins do Commit-AI v1.4.0
"""

import click
from pathlib import Path
from typing import Optional
import json

from .plugins_system import plugin_manager, PluginInfo
from .logger import logger


@click.group()
@click.pass_context
def plugins_cli(ctx):
    """🔌 Gerenciamento de Plugins extensíveis"""
    ctx.ensure_object(dict)
    try:
        # Carregar plugins na inicialização
        plugin_manager.load_plugins()
        ctx.obj['manager'] = plugin_manager
    except Exception as e:
        click.echo(click.style(f"[ERROR] Erro ao inicializar gerenciador de plugins: {e}", fg='red'))
        ctx.exit(1)


@plugins_cli.command('list')
@click.option('--category', '-c', 
              type=click.Choice(['ai_provider', 'template', 'workflow', 'integration', 'all']),
              default='all', help='Filtrar por categoria')
@click.option('--enabled-only', is_flag=True, help='Mostrar apenas plugins habilitados')
@click.pass_context
def list_plugins(ctx, category, enabled_only):
    """Lista plugins disponíveis"""
    manager = ctx.obj['manager']
    
    # Filtrar plugins
    plugins = manager.get_available_plugins()
    
    if category != 'all':
        plugins = [p for p in plugins if p.category == category]
    
    if enabled_only:
        plugins = [p for p in plugins if p.enabled]
    
    if not plugins:
        click.echo(click.style("[INFO] Nenhum plugin encontrado com os critérios especificados.", fg='yellow'))
        return
    
    # Agrupar por categoria
    by_category = {}
    for plugin in plugins:
        if plugin.category not in by_category:
            by_category[plugin.category] = []
        by_category[plugin.category].append(plugin)
    
    click.echo(click.style(f"[INFO] {len(plugins)} plugin(s) encontrado(s):", fg='cyan', bold=True))
    
    for cat, cat_plugins in by_category.items():
        click.echo(f"\n[CATEGORY] {cat.upper()}")
        click.echo("-" * 40)
        
        for plugin in cat_plugins:
            # Ícones de status
            status_icon = "✅" if plugin.enabled else "❌"
            
            click.echo(f"{status_icon} {click.style(plugin.name, fg='white', bold=True)} v{plugin.version}")
            click.echo(f"   {plugin.description}")
            click.echo(f"   Autor: {plugin.author}")
            
            if plugin.dependencies:
                deps_color = 'green' if plugin.enabled else 'red'
                click.echo(f"   Dependências: {click.style(', '.join(plugin.dependencies), fg=deps_color)}")
            
            # Mostrar localização
            location = "Sistema" if "commit_ai/plugins" in str(plugin.file_path) else "Usuário"
            click.echo(f"   Local: {location}")
            click.echo()


@plugins_cli.command('info')
@click.argument('plugin_name')
@click.pass_context
def plugin_info(ctx, plugin_name):
    """Mostra informações detalhadas de um plugin"""
    manager = ctx.obj['manager']
    
    plugins = {p.name: p for p in manager.get_available_plugins()}
    
    if plugin_name not in plugins:
        click.echo(click.style(f"[ERROR] Plugin '{plugin_name}' não encontrado.", fg='red'))
        return
    
    plugin = plugins[plugin_name]
    
    # Painel de informações detalhadas
    click.echo(click.style(f"📋 INFORMAÇÕES DO PLUGIN: {plugin.name}", fg='cyan', bold=True))
    click.echo("=" * 50)
    click.echo(f"Nome: {plugin.name}")
    click.echo(f"Versão: {plugin.version}")
    click.echo(f"Descrição: {plugin.description}")
    click.echo(f"Autor: {plugin.author}")
    click.echo(f"Categoria: {plugin.category}")
    click.echo(f"Status: {'✅ Habilitado' if plugin.enabled else '❌ Desabilitado'}")
    click.echo(f"Arquivo: {plugin.file_path}")
    
    if plugin.dependencies:
        click.echo(f"Dependências: {', '.join(plugin.dependencies)}")
    
    # Verificar funcionalidades específicas por categoria
    if plugin.category == 'ai_provider' and plugin.enabled:
        try:
            provider = manager.ai_providers.get(plugin.name)
            if provider:
                click.echo(f"Disponível: {'✅ Sim' if provider.is_available() else '❌ Não'}")
                models = provider.get_supported_models()
                if models:
                    click.echo(f"Modelos suportados: {', '.join(models[:5])}")
                    if len(models) > 5:
                        click.echo(f"   ... e mais {len(models) - 5}")
        except Exception as e:
            click.echo(f"Erro ao obter info específica: {e}")
    
    click.echo("=" * 50)


@plugins_cli.command('enable')
@click.argument('plugin_name')
@click.pass_context
def enable_plugin(ctx, plugin_name):
    """Habilita um plugin específico"""
    manager = ctx.obj['manager']
    
    click.echo(click.style(f"[INFO] Habilitando plugin: {plugin_name}", fg='yellow'))
    
    if manager.enable_plugin(plugin_name):
        click.echo(click.style(f"[OK] Plugin '{plugin_name}' habilitado com sucesso!", fg='green'))
        
        # Mostrar informações do plugin habilitado
        plugins = {p.name: p for p in manager.get_available_plugins()}
        if plugin_name in plugins:
            plugin = plugins[plugin_name]
            click.echo(f"Categoria: {plugin.category}")
            click.echo(f"Descrição: {plugin.description}")
    else:
        click.echo(click.style(f"[ERROR] Falha ao habilitar plugin '{plugin_name}'", fg='red'))


@plugins_cli.command('disable')
@click.argument('plugin_name')
@click.confirmation_option(prompt='Tem certeza que deseja desabilitar este plugin?')
@click.pass_context
def disable_plugin(ctx, plugin_name):
    """Desabilita um plugin específico"""
    manager = ctx.obj['manager']
    
    click.echo(click.style(f"[INFO] Desabilitando plugin: {plugin_name}", fg='yellow'))
    
    if manager.disable_plugin(plugin_name):
        click.echo(click.style(f"[OK] Plugin '{plugin_name}' desabilitado com sucesso!", fg='green'))
    else:
        click.echo(click.style(f"[ERROR] Falha ao desabilitar plugin '{plugin_name}'", fg='red'))


@plugins_cli.command('install')
@click.argument('plugin_file', type=click.Path(exists=True, path_type=Path))
@click.option('--enable', is_flag=True, help='Habilitar plugin após instalação')
@click.pass_context
def install_plugin(ctx, plugin_file, enable):
    """Instala plugin de arquivo"""
    manager = ctx.obj['manager']
    
    click.echo(click.style(f"[INFO] Instalando plugin: {plugin_file.name}", fg='yellow'))
    
    if manager.install_plugin(plugin_file):
        click.echo(click.style(f"[OK] Plugin instalado com sucesso!", fg='green'))
        
        if enable:
            # Tentar descobrir nome do plugin e habilitar
            plugin_name = plugin_file.stem
            click.echo(click.style(f"[INFO] Habilitando plugin: {plugin_name}", fg='yellow'))
            
            if manager.enable_plugin(plugin_name):
                click.echo(click.style(f"[OK] Plugin '{plugin_name}' habilitado!", fg='green'))
            else:
                click.echo(click.style(f"[WARN] Plugin instalado mas falha ao habilitar", fg='yellow'))
    else:
        click.echo(click.style(f"[ERROR] Falha na instalação do plugin", fg='red'))


@plugins_cli.command('uninstall')
@click.argument('plugin_name')
@click.confirmation_option(prompt='Tem certeza que deseja remover este plugin permanentemente?')
@click.pass_context
def uninstall_plugin(ctx, plugin_name):
    """Remove plugin instalado pelo usuário"""
    manager = ctx.obj['manager']
    
    click.echo(click.style(f"[INFO] Removendo plugin: {plugin_name}", fg='yellow'))
    
    if manager.uninstall_plugin(plugin_name):
        click.echo(click.style(f"[OK] Plugin '{plugin_name}' removido com sucesso!", fg='green'))
    else:
        click.echo(click.style(f"[ERROR] Falha ao remover plugin '{plugin_name}'", fg='red'))


@plugins_cli.command('create')
@click.option('--name', prompt='Nome do plugin', help='Nome do plugin')
@click.option('--category', 
              type=click.Choice(['ai_provider', 'template', 'workflow', 'integration']),
              prompt='Categoria do plugin', help='Categoria do plugin')
@click.option('--author', prompt='Autor', help='Nome do autor')
@click.option('--description', prompt='Descrição', help='Descrição do plugin')
@click.pass_context
def create_plugin_template(ctx, name, category, author, description):
    """Cria template de plugin"""
    manager = ctx.obj['manager']
    
    # Criar diretório de plugins do usuário se não existe
    user_plugins_dir = Path.home() / '.commit-ai' / 'plugins'
    user_plugins_dir.mkdir(parents=True, exist_ok=True)
    
    plugin_file = user_plugins_dir / f"{name}.py"
    
    if plugin_file.exists():
        click.echo(click.style(f"[ERROR] Plugin '{name}' já existe!", fg='red'))
        return
    
    # Templates por categoria
    templates = {
        'ai_provider': _get_ai_provider_template,
        'template': _get_template_plugin_template,
        'workflow': _get_workflow_plugin_template,
        'integration': _get_integration_plugin_template
    }
    
    template_func = templates.get(category)
    if not template_func:
        click.echo(click.style(f"[ERROR] Categoria não suportada: {category}", fg='red'))
        return
    
    # Gerar código do template
    plugin_code = template_func(name, author, description)
    
    # Salvar arquivo
    plugin_file.write_text(plugin_code, encoding='utf-8')
    
    click.echo(click.style(f"[OK] Template de plugin criado: {plugin_file}", fg='green'))
    click.echo(f"[INFO] Edite o arquivo e implemente as funcionalidades necessárias.")
    click.echo(f"[INFO] Use 'commit-ai plugins install {plugin_file}' para instalar.")


@plugins_cli.command('test')
@click.argument('plugin_name')
@click.pass_context
def test_plugin(ctx, plugin_name):
    """Testa funcionalidades básicas de um plugin"""
    manager = ctx.obj['manager']
    
    if plugin_name not in manager.plugins:
        click.echo(click.style(f"[ERROR] Plugin '{plugin_name}' não encontrado", fg='red'))
        return
    
    plugin = manager.plugins[plugin_name]
    info = manager.plugin_info[plugin_name]
    
    click.echo(click.style(f"[INFO] Testando plugin: {plugin_name}", fg='yellow'))
    
    try:
        # Teste básico de inicialização
        if plugin.initialize():
            click.echo(click.style("[OK] Inicialização: SUCESSO", fg='green'))
        else:
            click.echo(click.style("[ERROR] Inicialização: FALHA", fg='red'))
            return
        
        # Testes específicos por categoria
        if info.category == 'ai_provider':
            from .plugins_system import AIProviderPlugin
            if isinstance(plugin, AIProviderPlugin):
                click.echo(f"[TEST] Disponibilidade: {plugin.is_available()}")
                click.echo(f"[TEST] Modelos suportados: {len(plugin.get_supported_models())}")
                
                # Teste de geração (diff simulado)
                test_diff = "+print('Hello World')"
                try:
                    message = plugin.generate_commit_message(test_diff, "conventional")
                    click.echo(f"[TEST] Geração de mensagem: OK")
                    click.echo(f"       Resultado: {message[:50]}...")
                except Exception as e:
                    click.echo(click.style(f"[ERROR] Geração de mensagem: {e}", fg='red'))
        
        # Teste de cleanup
        if plugin.cleanup():
            click.echo(click.style("[OK] Cleanup: SUCESSO", fg='green'))
        else:
            click.echo(click.style("[WARN] Cleanup: FALHA", fg='yellow'))
        
        click.echo(click.style("[OK] Teste concluído!", fg='green'))
        
    except Exception as e:
        click.echo(click.style(f"[ERROR] Erro durante teste: {e}", fg='red'))


def _get_ai_provider_template(name: str, author: str, description: str) -> str:
    """Template para plugin de AI Provider"""
    return f'''#!/usr/bin/env python3
"""
{description}
"""

from typing import Dict, List, Any
import sys
from pathlib import Path

# Adicionar caminho para importar do Commit-AI
sys.path.append(str(Path(__file__).parent.parent))

from plugins_system import AIProviderPlugin


class {name.title().replace('_', '')}Provider(AIProviderPlugin):
    """Provider customizado: {description}"""
    
    def __init__(self):
        # TODO: Configurar seu provider aqui
        self.api_key = None
        self.base_url = None
        self.model = None
    
    def get_info(self) -> Dict[str, Any]:
        """Informações do plugin"""
        return {{
            'name': '{name}',
            'version': '1.0.0',
            'description': '{description}',
            'author': '{author}',
            'category': 'ai_provider',
            'dependencies': []  # TODO: Adicionar dependências necessárias
        }}
    
    def initialize(self) -> bool:
        """Inicializa o provider"""
        # TODO: Implementar inicialização
        return True
    
    def cleanup(self) -> bool:
        """Limpa recursos"""
        # TODO: Implementar cleanup se necessário
        return True
    
    def is_available(self) -> bool:
        """Verifica se o provider está disponível"""
        # TODO: Verificar se API/serviço está disponível
        return True
    
    def get_supported_models(self) -> List[str]:
        """Retorna modelos suportados"""
        # TODO: Retornar lista de modelos suportados
        return ["model1", "model2"]
    
    def generate_commit_message(self, 
                               diff: str, 
                               template: str = "conventional",
                               **kwargs) -> str:
        """Gera mensagem de commit"""
        # TODO: Implementar geração de mensagem usando sua IA
        
        if not self.is_available():
            raise Exception("Provider não está disponível")
        
        # Exemplo básico - SUBSTITUA pela sua implementação
        return f"feat: implement {{len(diff)}} characters of changes"


if __name__ == "__main__":
    # Teste do plugin
    plugin = {name.title().replace('_', '')}Provider()
    print("Teste do plugin:", plugin.get_info())
'''

def _get_template_plugin_template(name: str, author: str, description: str) -> str:
    """Template para plugin de Template"""
    return f'''#!/usr/bin/env python3
"""
{description}
"""

from typing import Dict, Any
import sys
from pathlib import Path

# Adicionar caminho para importar do Commit-AI
sys.path.append(str(Path(__file__).parent.parent))

from plugins_system import TemplatePlugin


class {name.title().replace('_', '')}Template(TemplatePlugin):
    """Template customizado: {description}"""
    
    def get_info(self) -> Dict[str, Any]:
        """Informações do plugin"""
        return {{
            'name': '{name}',
            'version': '1.0.0',
            'description': '{description}',
            'author': '{author}',
            'category': 'template',
            'dependencies': []
        }}
    
    def initialize(self) -> bool:
        """Inicializa o template"""
        return True
    
    def cleanup(self) -> bool:
        """Limpa recursos"""
        return True
    
    def get_template(self) -> Dict[str, Any]:
        """Retorna definição do template"""
        return {{
            'name': '{name}',
            'description': '{description}',
            'format': 'tipo(escopo): descrição',
            'types': [
                'feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore'
            ],
            'scopes': [],
            'examples': [
                'feat(auth): add user login system',
                'fix(api): resolve timeout issue'
            ]
        }}
    
    def format_message(self, commit_type: str, description: str, **kwargs) -> str:
        """Formata mensagem usando o template"""
        scope = kwargs.get('scope', '')
        
        if scope:
            return f"{{commit_type}}({{scope}}): {{description}}"
        else:
            return f"{{commit_type}}: {{description}}"


if __name__ == "__main__":
    plugin = {name.title().replace('_', '')}Template()
    print("Template:", plugin.get_template())
'''

def _get_workflow_plugin_template(name: str, author: str, description: str) -> str:
    """Template para plugin de Workflow"""
    return f'''#!/usr/bin/env python3
"""
{description}
"""

from typing import Dict, Any, Optional
import sys
from pathlib import Path

# Adicionar caminho para importar do Commit-AI
sys.path.append(str(Path(__file__).parent.parent))

from plugins_system import WorkflowPlugin


class {name.title().replace('_', '')}Workflow(WorkflowPlugin):
    """Workflow customizado: {description}"""
    
    def get_info(self) -> Dict[str, Any]:
        """Informações do plugin"""
        return {{
            'name': '{name}',
            'version': '1.0.0',
            'description': '{description}',
            'author': '{author}',
            'category': 'workflow',
            'dependencies': []
        }}
    
    def initialize(self) -> bool:
        """Inicializa o workflow"""
        return True
    
    def cleanup(self) -> bool:
        """Limpa recursos"""
        return True
    
    def pre_commit_hook(self, diff: str) -> Optional[Dict[str, Any]]:
        """Hook executado antes do commit"""
        # TODO: Implementar lógica pré-commit
        # Retorne dict com dados ou None
        
        return {{
            'suggestion': 'Sugestão baseada no diff',
            'confidence': 0.8,
            'metadata': {{
                'files_analyzed': 1,
                'complexity': 'low'
            }}
        }}
    
    def post_commit_hook(self, commit_info: Dict[str, Any]) -> None:
        """Hook executado após o commit"""
        # TODO: Implementar lógica pós-commit
        print(f"Commit processado: {{commit_info.get('hash', 'N/A')}}")


if __name__ == "__main__":
    plugin = {name.title().replace('_', '')}Workflow()
    print("Workflow plugin:", plugin.get_info())
'''

def _get_integration_plugin_template(name: str, author: str, description: str) -> str:
    """Template para plugin de Integração"""
    return f'''#!/usr/bin/env python3
"""
{description}
"""

from typing import Dict, Any
import sys
from pathlib import Path

# Adicionar caminho para importar do Commit-AI
sys.path.append(str(Path(__file__).parent.parent))

from plugins_system import IntegrationPlugin


class {name.title().replace('_', '')}Integration(IntegrationPlugin):
    """Integração customizada: {description}"""
    
    def __init__(self):
        self.connected = False
        self.config = {{}}
    
    def get_info(self) -> Dict[str, Any]:
        """Informações do plugin"""
        return {{
            'name': '{name}',
            'version': '1.0.0',
            'description': '{description}',
            'author': '{author}',
            'category': 'integration',
            'dependencies': []  # TODO: Adicionar dependências (ex: requests)
        }}
    
    def initialize(self) -> bool:
        """Inicializa a integração"""
        return True
    
    def cleanup(self) -> bool:
        """Limpa recursos"""
        if self.connected:
            # TODO: Desconectar serviços
            self.connected = False
        return True
    
    def connect(self, config: Dict[str, Any]) -> bool:
        """Conecta com serviço externo"""
        # TODO: Implementar conexão
        self.config = config
        self.connected = True
        return True
    
    def send_data(self, data: Dict[str, Any]) -> bool:
        """Envia dados para serviço externo"""
        if not self.connected:
            return False
        
        # TODO: Implementar envio de dados
        print(f"Enviando dados: {{len(data)}} itens")
        return True


if __name__ == "__main__":
    plugin = {name.title().replace('_', '')}Integration()
    print("Integration plugin:", plugin.get_info())
'''


if __name__ == '__main__':
    plugins_cli()
