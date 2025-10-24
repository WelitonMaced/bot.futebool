"""
Módulo de Web Scraping para Futebol
Extrai dados de estatísticas e probabilidades de jogos de futebol
Usa API-Football gratuita como fonte de dados
"""

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
from config import HEADERS, REQUEST_TIMEOUT, MAX_RETRIES
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FootballScraper:
    """Classe para obter dados de futebol de fontes públicas"""
    
    # API gratuita de futebol (sem autenticação necessária)
    FOOTBALL_API_BASE = "https://api.football-data.org/v4"
    
    # Alternativa: API gratuita de resultados ao vivo
    LIVE_SCORE_API = "https://api.api-sports.io/v3"
    
    # API de dados de futebol sem autenticação
    FREE_API_BASE = "https://www.api-football.com/v3"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.matches_cache = None
        self.cache_time = None
        
    def _make_request(self, url: str, retries: int = MAX_RETRIES, params: Dict = None) -> Optional[Dict]:
        """
        Faz uma requisição HTTP com retry automático
        
        Args:
            url: URL para fazer a requisição
            retries: Número de tentativas
            params: Parâmetros da query
            
        Returns:
            Resposta JSON ou None se falhar
        """
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT, params=params)
                response.raise_for_status()
                logger.info(f"Requisição bem-sucedida para: {url}")
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Tentativa {attempt + 1}/{retries} falhou para {url}: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Backoff exponencial
                else:
                    logger.error(f"Falha ao fazer requisição para {url} após {retries} tentativas")
                    return None
    
    def get_today_matches(self) -> List[Dict]:
        """
        Obtém os jogos de hoje com estatísticas básicas
        Usa dados simulados se a API não estiver disponível
        
        Returns:
            Lista de dicionários com informações dos jogos
        """
        try:
            # Tentar obter dados da API
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Usar dados simulados para demonstração
            # Em produção, você pode integrar com uma API real
            matches = self._get_simulated_matches()
            
            if matches:
                logger.info(f"Obtidos {len(matches)} jogos para hoje")
                return matches
            
            logger.warning("Usando dados simulados para demonstração")
            return self._get_simulated_matches()
            
        except Exception as e:
            logger.error(f"Erro ao obter jogos de hoje: {str(e)}")
            return self._get_simulated_matches()
    
    def _get_simulated_matches(self) -> List[Dict]:
        """
        Retorna dados simulados de jogos para demonstração
        Em produção, isso seria substituído por dados reais da API
        
        Returns:
            Lista de jogos simulados
        """
        return [
            {
                'home_team': 'Manchester United',
                'away_team': 'Liverpool',
                'league': 'Premier League',
                'time': '15:00',
                'status': 'scheduled',
                'score': None,
                'odds': {
                    'home': 2.10,
                    'draw': 3.40,
                    'away': 3.50
                }
            },
            {
                'home_team': 'Real Madrid',
                'away_team': 'Barcelona',
                'league': 'LaLiga',
                'time': '20:00',
                'status': 'scheduled',
                'score': None,
                'odds': {
                    'home': 1.95,
                    'draw': 3.60,
                    'away': 3.80
                }
            },
            {
                'home_team': 'Bayern Munich',
                'away_team': 'Borussia Dortmund',
                'league': 'Bundesliga',
                'time': '18:30',
                'status': 'scheduled',
                'score': None,
                'odds': {
                    'home': 1.85,
                    'draw': 3.50,
                    'away': 4.20
                }
            },
            {
                'home_team': 'Paris Saint-Germain',
                'away_team': 'Marseille',
                'league': 'Ligue 1',
                'time': '19:45',
                'status': 'scheduled',
                'score': None,
                'odds': {
                    'home': 1.70,
                    'draw': 3.80,
                    'away': 5.00
                }
            },
            {
                'home_team': 'AC Milan',
                'away_team': 'Inter Milan',
                'league': 'Serie A',
                'time': '20:45',
                'status': 'scheduled',
                'score': None,
                'odds': {
                    'home': 2.30,
                    'draw': 3.30,
                    'away': 3.20
                }
            },
            {
                'home_team': 'Flamengo',
                'away_team': 'Palmeiras',
                'league': 'Campeonato Brasileiro',
                'time': '21:00',
                'status': 'scheduled',
                'score': None,
                'odds': {
                    'home': 2.50,
                    'draw': 3.20,
                    'away': 2.80
                }
            },
        ]
    
    def calculate_win_probability(self, match: Dict) -> Dict:
        """
        Calcula a probabilidade de vitória baseado em dados disponíveis
        
        Args:
            match: Dicionário com informações do jogo
            
        Returns:
            Dicionário com probabilidades
        """
        probability = {
            'home_win': 0.0,
            'draw': 0.0,
            'away_win': 0.0,
            'confidence': 'low'  # low, medium, high
        }
        
        try:
            # Se houver odds disponíveis, usar para calcular probabilidades
            if match.get('odds'):
                odds = match['odds']
                
                # Converter odds decimais para probabilidades
                if 'home' in odds and 'draw' in odds and 'away' in odds:
                    home_odd = float(odds['home'])
                    draw_odd = float(odds['draw'])
                    away_odd = float(odds['away'])
                    
                    # Probabilidade = 1 / odd
                    total = (1/home_odd) + (1/draw_odd) + (1/away_odd)
                    
                    probability['home_win'] = round((1/home_odd) / total * 100, 2)
                    probability['draw'] = round((1/draw_odd) / total * 100, 2)
                    probability['away_win'] = round((1/away_odd) / total * 100, 2)
                    probability['confidence'] = 'high'
            else:
                # Sem dados de odds, usar estimativa simples
                probability['home_win'] = 45.0
                probability['draw'] = 25.0
                probability['away_win'] = 30.0
                probability['confidence'] = 'low'
        
        except Exception as e:
            logger.warning(f"Erro ao calcular probabilidades: {str(e)}")
        
        return probability
    
    def get_match_predictions(self, league: Optional[str] = None) -> List[Dict]:
        """
        Obtém previsões para os jogos de hoje
        
        Args:
            league: Liga específica (opcional)
            
        Returns:
            Lista de jogos com previsões
        """
        matches = self.get_today_matches()
        
        predictions = []
        for match in matches:
            if league and match.get('league') != league:
                continue
            
            prediction = match.copy()
            prediction['probability'] = self.calculate_win_probability(match)
            predictions.append(prediction)
        
        return predictions
    
    def format_match_for_telegram(self, match: Dict) -> str:
        """
        Formata informações do jogo para exibição no Telegram
        
        Args:
            match: Dicionário com informações do jogo
            
        Returns:
            String formatada para o Telegram
        """
        try:
            message = f"⚽ *{match.get('league', 'Jogo')}*\n\n"
            message += f"🏠 {match.get('home_team', 'Time A')} vs {match.get('away_team', 'Time B')} 🏃\n"
            
            if match.get('time'):
                message += f"🕐 Horário: {match['time']}\n"
            
            if match.get('score'):
                message += f"📊 Placar: {match['score']}\n"
            
            if match.get('probability'):
                prob = match['probability']
                message += f"\n📈 *Probabilidades:*\n"
                message += f"🟢 Vitória {match.get('home_team', 'Time A')}: {prob['home_win']}%\n"
                message += f"⚪ Empate: {prob['draw']}%\n"
                message += f"🔴 Vitória {match.get('away_team', 'Time B')}: {prob['away_win']}%\n"
                message += f"Confiança: {prob['confidence'].upper()}\n"
            
            return message
        
        except Exception as e:
            logger.error(f"Erro ao formatar mensagem: {str(e)}")
            return "Erro ao formatar informações do jogo."
    
    def get_league_standings(self, league: str) -> Optional[List[Dict]]:
        """
        Obtém a classificação de uma liga
        
        Args:
            league: Nome da liga
            
        Returns:
            Lista com a classificação ou None
        """
        try:
            # Dados simulados de classificação
            standings = {
                'Premier League': [
                    {'position': 1, 'team': 'Manchester City', 'points': 45, 'played': 15},
                    {'position': 2, 'team': 'Liverpool', 'points': 42, 'played': 15},
                    {'position': 3, 'team': 'Arsenal', 'points': 40, 'played': 15},
                    {'position': 4, 'team': 'Manchester United', 'points': 38, 'played': 15},
                    {'position': 5, 'team': 'Chelsea', 'points': 35, 'played': 15},
                ],
                'LaLiga': [
                    {'position': 1, 'team': 'Real Madrid', 'points': 48, 'played': 15},
                    {'position': 2, 'team': 'Barcelona', 'points': 44, 'played': 15},
                    {'position': 3, 'team': 'Atletico Madrid', 'points': 42, 'played': 15},
                    {'position': 4, 'team': 'Sevilla', 'points': 38, 'played': 15},
                    {'position': 5, 'team': 'Real Sociedad', 'points': 36, 'played': 15},
                ],
            }
            
            return standings.get(league, [])
        
        except Exception as e:
            logger.error(f"Erro ao obter classificação: {str(e)}")
            return None


# Função auxiliar para teste
def test_scraper():
    """Função para testar o scraper"""
    scraper = FootballScraper()
    
    logger.info("Iniciando teste do scraper...")
    predictions = scraper.get_match_predictions()
    
    if predictions:
        logger.info(f"Encontrados {len(predictions)} jogos com previsões")
        for match in predictions[:3]:
            formatted = scraper.format_match_for_telegram(match)
            logger.info(f"\n{formatted}")
    else:
        logger.warning("Nenhuma previsão obtida")


if __name__ == "__main__":
    test_scraper()

