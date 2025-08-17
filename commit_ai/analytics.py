#!/usr/bin/env python3
"""
Sistema de Analytics Avançados para Commit-AI v1.4.0

Coleta, processa e apresenta métricas detalhadas sobre padrões de commit,
produtividade de desenvolvimento e insights colaborativos.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import statistics

from .git_handler import GitHandler
from .config_manager import ConfigManager
from .logger import logger


@dataclass
class CommitMetric:
    """Métrica individual de commit"""
    hash: str
    message: str
    author: str
    date: datetime
    type: str
    provider: str
    template: str
    confidence: float
    files_changed: int
    lines_added: int
    lines_deleted: int
    processing_time: float


@dataclass
class ProductivityMetrics:
    """Métricas de produtividade"""
    total_commits: int
    commits_per_day: float
    avg_processing_time: float
    most_used_provider: str
    most_used_template: str
    most_common_type: str
    avg_confidence: float
    total_lines_changed: int
    files_touched: int


@dataclass
class TeamInsights:
    """Insights colaborativos"""
    team_members: List[str]
    commits_by_author: Dict[str, int]
    avg_commits_per_author: float
    most_active_author: str
    common_patterns: List[str]
    collaboration_score: float


class AnalyticsDatabase:
    """Gerenciador do banco de dados de analytics"""
    
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            config_dir = Path.home() / '.commit-ai'
            config_dir.mkdir(exist_ok=True)
            db_path = config_dir / 'analytics.db'
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        """Inicializa estrutura do banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS commits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash TEXT UNIQUE NOT NULL,
                    message TEXT NOT NULL,
                    author TEXT NOT NULL,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    template TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    files_changed INTEGER NOT NULL,
                    lines_added INTEGER NOT NULL,
                    lines_deleted INTEGER NOT NULL,
                    processing_time REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    commits_count INTEGER DEFAULT 0,
                    total_processing_time REAL DEFAULT 0.0,
                    providers_used TEXT,
                    templates_used TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS project_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_path TEXT UNIQUE NOT NULL,
                    total_commits INTEGER DEFAULT 0,
                    last_commit_date TEXT,
                    most_used_provider TEXT,
                    most_used_template TEXT,
                    avg_confidence REAL DEFAULT 0.0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Índices para performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_commits_date ON commits(date)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_commits_author ON commits(author)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_commits_type ON commits(type)')
    
    def record_commit(self, metric: CommitMetric) -> None:
        """Registra uma métrica de commit"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO commits 
                    (hash, message, author, date, type, provider, template, 
                     confidence, files_changed, lines_added, lines_deleted, 
                     processing_time, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    metric.hash,
                    metric.message,
                    metric.author,
                    metric.date.isoformat(),
                    metric.type,
                    metric.provider,
                    metric.template,
                    metric.confidence,
                    metric.files_changed,
                    metric.lines_added,
                    metric.lines_deleted,
                    metric.processing_time,
                    datetime.now().isoformat()
                ))
                
                logger.debug(f"Métrica de commit registrada: {metric.hash}")
                
        except Exception as e:
            logger.error(f"Erro ao registrar métrica de commit: {e}")
    
    def get_commits(self, 
                   days: int = 30, 
                   author: Optional[str] = None) -> List[CommitMetric]:
        """Recupera commits do período especificado"""
        try:
            since_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                query = '''
                    SELECT hash, message, author, date, type, provider, template,
                           confidence, files_changed, lines_added, lines_deleted,
                           processing_time
                    FROM commits 
                    WHERE date >= ?
                '''
                params = [since_date.isoformat()]
                
                if author:
                    query += ' AND author = ?'
                    params.append(author)
                
                query += ' ORDER BY date DESC'
                
                cursor = conn.execute(query, params)
                commits = []
                
                for row in cursor.fetchall():
                    commits.append(CommitMetric(
                        hash=row[0],
                        message=row[1],
                        author=row[2],
                        date=datetime.fromisoformat(row[3]),
                        type=row[4],
                        provider=row[5],
                        template=row[6],
                        confidence=row[7],
                        files_changed=row[8],
                        lines_added=row[9],
                        lines_deleted=row[10],
                        processing_time=row[11]
                    ))
                
                return commits
                
        except Exception as e:
            logger.error(f"Erro ao recuperar commits: {e}")
            return []


class AnalyticsEngine:
    """Motor de analytics para processar e gerar insights"""
    
    def __init__(self):
        self.db = AnalyticsDatabase()
        self.git_handler = GitHandler()
        self.config_manager = ConfigManager()
    
    def collect_commit_metrics(self, 
                              commit_hash: str,
                              message: str,
                              provider: str,
                              template: str,
                              confidence: float,
                              processing_time: float) -> None:
        """Coleta métricas de um commit"""
        try:
            # Obter informações do commit via Git
            commit_info = self.git_handler.get_commit_info(commit_hash)
            if not commit_info:
                logger.warning(f"Não foi possível obter info do commit {commit_hash}")
                return
            
            # Obter estatísticas de mudanças
            stats = self.git_handler.get_commit_stats(commit_hash)
            
            # Determinar tipo de commit
            commit_type = self._extract_commit_type(message)
            
            # Criar métrica
            metric = CommitMetric(
                hash=commit_hash,
                message=message,
                author=commit_info.get('author', 'Unknown'),
                date=datetime.fromisoformat(commit_info.get('date', datetime.now().isoformat())),
                type=commit_type,
                provider=provider,
                template=template,
                confidence=confidence,
                files_changed=stats.get('files_changed', 0),
                lines_added=stats.get('lines_added', 0),
                lines_deleted=stats.get('lines_deleted', 0),
                processing_time=processing_time
            )
            
            # Registrar no banco
            self.db.record_commit(metric)
            
        except Exception as e:
            logger.error(f"Erro ao coletar métricas do commit: {e}")
    
    def _extract_commit_type(self, message: str) -> str:
        """Extrai o tipo do commit da mensagem"""
        types = ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']
        
        message_lower = message.lower()
        for commit_type in types:
            if message_lower.startswith(f"{commit_type}:") or message_lower.startswith(f"{commit_type}("):
                return commit_type
        
        return 'other'
    
    def calculate_productivity_metrics(self, days: int = 30) -> ProductivityMetrics:
        """Calcula métricas de produtividade"""
        commits = self.db.get_commits(days=days)
        
        if not commits:
            return ProductivityMetrics(
                total_commits=0,
                commits_per_day=0.0,
                avg_processing_time=0.0,
                most_used_provider="N/A",
                most_used_template="N/A",
                most_common_type="N/A",
                avg_confidence=0.0,
                total_lines_changed=0,
                files_touched=0
            )
        
        # Calcular estatísticas básicas
        total_commits = len(commits)
        commits_per_day = total_commits / days
        avg_processing_time = statistics.mean([c.processing_time for c in commits])
        avg_confidence = statistics.mean([c.confidence for c in commits])
        
        # Contadores para elementos mais usados
        provider_counter = Counter([c.provider for c in commits])
        template_counter = Counter([c.template for c in commits])
        type_counter = Counter([c.type for c in commits])
        
        # Estatísticas de código
        total_lines_changed = sum([c.lines_added + c.lines_deleted for c in commits])
        files_touched = sum([c.files_changed for c in commits])
        
        return ProductivityMetrics(
            total_commits=total_commits,
            commits_per_day=round(commits_per_day, 2),
            avg_processing_time=round(avg_processing_time, 2),
            most_used_provider=provider_counter.most_common(1)[0][0] if provider_counter else "N/A",
            most_used_template=template_counter.most_common(1)[0][0] if template_counter else "N/A",
            most_common_type=type_counter.most_common(1)[0][0] if type_counter else "N/A",
            avg_confidence=round(avg_confidence, 3),
            total_lines_changed=total_lines_changed,
            files_touched=files_touched
        )
    
    def generate_team_insights(self, days: int = 30) -> TeamInsights:
        """Gera insights colaborativos da equipe"""
        commits = self.db.get_commits(days=days)
        
        if not commits:
            return TeamInsights(
                team_members=[],
                commits_by_author={},
                avg_commits_per_author=0.0,
                most_active_author="N/A",
                common_patterns=[],
                collaboration_score=0.0
            )
        
        # Análise por autor
        commits_by_author = defaultdict(int)
        for commit in commits:
            commits_by_author[commit.author] += 1
        
        team_members = list(commits_by_author.keys())
        avg_commits_per_author = statistics.mean(commits_by_author.values()) if commits_by_author else 0.0
        most_active_author = max(commits_by_author, key=commits_by_author.get) if commits_by_author else "N/A"
        
        # Análise de padrões comuns
        common_patterns = self._analyze_commit_patterns(commits)
        
        # Calcular score de colaboração
        collaboration_score = self._calculate_collaboration_score(commits_by_author, len(commits))
        
        return TeamInsights(
            team_members=team_members,
            commits_by_author=dict(commits_by_author),
            avg_commits_per_author=round(avg_commits_per_author, 2),
            most_active_author=most_active_author,
            common_patterns=common_patterns,
            collaboration_score=round(collaboration_score, 2)
        )
    
    def _analyze_commit_patterns(self, commits: List[CommitMetric]) -> List[str]:
        """Analisa padrões comuns nos commits"""
        patterns = []
        
        # Análise de tipos mais usados
        type_counter = Counter([c.type for c in commits])
        if type_counter:
            most_common_type = type_counter.most_common(1)[0]
            patterns.append(f"{most_common_type[1]} commits do tipo '{most_common_type[0]}'")
        
        # Análise de templates
        template_counter = Counter([c.template for c in commits])
        if template_counter:
            most_common_template = template_counter.most_common(1)[0]
            patterns.append(f"Template '{most_common_template[0]}' usado {most_common_template[1]} vezes")
        
        # Análise de confiança
        confidences = [c.confidence for c in commits]
        if confidences:
            avg_confidence = statistics.mean(confidences)
            if avg_confidence > 0.8:
                patterns.append("Alta confiança nas mensagens geradas (>80%)")
            elif avg_confidence < 0.6:
                patterns.append("Baixa confiança nas mensagens geradas (<60%)")
        
        # Análise temporal
        if len(commits) > 7:
            recent_commits = commits[:7]  # Últimos 7 commits
            recent_types = Counter([c.type for c in recent_commits])
            if len(recent_types) == 1:
                patterns.append(f"Foco recente em commits do tipo '{list(recent_types.keys())[0]}'")
        
        return patterns
    
    def _calculate_collaboration_score(self, commits_by_author: dict, total_commits: int) -> float:
        """Calcula score de colaboração baseado na distribuição de commits"""
        if not commits_by_author or total_commits == 0:
            return 0.0
        
        num_authors = len(commits_by_author)
        if num_authors == 1:
            return 0.0  # Sem colaboração
        
        # Calcular entropia da distribuição de commits
        probabilities = [count / total_commits for count in commits_by_author.values()]
        entropy = -sum(p * log2(p) for p in probabilities if p > 0)
        
        # Normalizar para escala 0-1
        max_entropy = log2(num_authors)
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return normalized_entropy
    
    def export_analytics_report(self, 
                               format: str = 'json',
                               days: int = 30) -> Optional[str]:
        """Exporta relatório de analytics em formato especificado"""
        try:
            productivity = self.calculate_productivity_metrics(days)
            team_insights = self.generate_team_insights(days)
            commits = self.db.get_commits(days)
            
            report_data = {
                'report_date': datetime.now().isoformat(),
                'period_days': days,
                'productivity_metrics': asdict(productivity),
                'team_insights': asdict(team_insights),
                'recent_commits': [asdict(commit) for commit in commits[:10]],
                'summary': {
                    'total_commits': len(commits),
                    'unique_authors': len(team_insights.team_members),
                    'avg_daily_commits': productivity.commits_per_day,
                    'dominant_type': productivity.most_common_type,
                    'quality_score': productivity.avg_confidence
                }
            }
            
            if format == 'json':
                return json.dumps(report_data, indent=2, default=str)
            elif format == 'text':
                return self._format_text_report(report_data)
            else:
                logger.warning(f"Formato não suportado: {format}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao exportar relatório: {e}")
            return None
    
    def _format_text_report(self, data: Dict[str, Any]) -> str:
        """Formata relatório em texto simples"""
        report = []
        report.append("=" * 60)
        report.append("📊 RELATÓRIO DE ANALYTICS - COMMIT-AI")
        report.append("=" * 60)
        report.append(f"Período: {data['period_days']} dias")
        report.append(f"Gerado em: {data['report_date']}")
        report.append("")
        
        # Métricas de produtividade
        prod = data['productivity_metrics']
        report.append("🚀 PRODUTIVIDADE")
        report.append("-" * 30)
        report.append(f"Total de commits: {prod['total_commits']}")
        report.append(f"Commits por dia: {prod['commits_per_day']}")
        report.append(f"Tempo médio de processamento: {prod['avg_processing_time']}s")
        report.append(f"Provider mais usado: {prod['most_used_provider']}")
        report.append(f"Template mais usado: {prod['most_used_template']}")
        report.append(f"Tipo mais comum: {prod['most_common_type']}")
        report.append(f"Confiança média: {prod['avg_confidence']:.1%}")
        report.append(f"Linhas alteradas: {prod['total_lines_changed']}")
        report.append("")
        
        # Insights da equipe
        team = data['team_insights']
        report.append("👥 COLABORAÇÃO")
        report.append("-" * 30)
        report.append(f"Membros da equipe: {len(team['team_members'])}")
        report.append(f"Mais ativo: {team['most_active_author']}")
        report.append(f"Score de colaboração: {team['collaboration_score']}")
        report.append("")
        
        if team['common_patterns']:
            report.append("Padrões identificados:")
            for pattern in team['common_patterns']:
                report.append(f"  • {pattern}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


def log2(x):
    """Logaritmo base 2"""
    import math
    return math.log2(x)


# Instância global do analytics engine
analytics_engine = AnalyticsEngine()


if __name__ == "__main__":
    # Teste do sistema de analytics
    engine = AnalyticsEngine()
    
    # Simular algumas métricas
    test_metrics = [
        ("abc123", "feat: add user authentication", "openai", "conventional", 0.95, 2.5),
        ("def456", "fix: resolve login bug", "gemini", "conventional", 0.88, 1.8),
        ("ghi789", "docs: update README", "claude", "conventional", 0.92, 1.2)
    ]
    
    for metric_data in test_metrics:
        engine.collect_commit_metrics(*metric_data)
    
    # Gerar relatórios
    productivity = engine.calculate_productivity_metrics(7)
    team_insights = engine.generate_team_insights(7)
    
    print("Métricas de Produtividade:", productivity)
    print("Insights da Equipe:", team_insights)
    
    # Exportar relatório
    report = engine.export_analytics_report('text', 7)
    if report:
        print("\n" + report)
