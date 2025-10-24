"""
Script de teste para o módulo de scraping
Verifica se o scraper consegue conectar e extrair dados
"""

import logging
from scraper import FootballScraper

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_scraper_connection():
    """Testa a conexão com o FlashScore"""
    logger.info("=" * 60)
    logger.info("TESTE 1: Conexão com FlashScore")
    logger.info("=" * 60)
    
    scraper = FootballScraper()
    
    try:
        matches = scraper.get_today_matches()
        
        if matches:
            logger.info(f"✅ Sucesso! Encontrados {len(matches)} jogos")
            logger.info("\nPrimeiros 3 jogos encontrados:")
            for i, match in enumerate(matches[:3], 1):
                logger.info(f"\n{i}. {match.get('home_team', 'N/A')} vs {match.get('away_team', 'N/A')}")
                logger.info(f"   Liga: {match.get('league', 'N/A')}")
                logger.info(f"   Horário: {match.get('time', 'N/A')}")
        else:
            logger.warning("⚠️ Nenhum jogo encontrado. O site pode estar indisponível ou a estrutura mudou.")
    
    except Exception as e:
        logger.error(f"❌ Erro ao conectar: {str(e)}")


def test_probability_calculation():
    """Testa o cálculo de probabilidades"""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 2: Cálculo de Probabilidades")
    logger.info("=" * 60)
    
    scraper = FootballScraper()
    
    # Criar um jogo de exemplo
    sample_match = {
        'home_team': 'Manchester United',
        'away_team': 'Liverpool',
        'league': 'Premier League',
        'time': '15:00',
        'odds': {
            'home': 2.10,
            'draw': 3.40,
            'away': 3.50
        }
    }
    
    try:
        probability = scraper.calculate_win_probability(sample_match)
        
        logger.info(f"✅ Probabilidades calculadas com sucesso!")
        logger.info(f"\nJogo: {sample_match['home_team']} vs {sample_match['away_team']}")
        logger.info(f"Vitória do {sample_match['home_team']}: {probability['home_win']}%")
        logger.info(f"Empate: {probability['draw']}%")
        logger.info(f"Vitória do {sample_match['away_team']}: {probability['away_win']}%")
        logger.info(f"Confiança: {probability['confidence'].upper()}")
    
    except Exception as e:
        logger.error(f"❌ Erro ao calcular probabilidades: {str(e)}")


def test_telegram_formatting():
    """Testa a formatação de mensagens para o Telegram"""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 3: Formatação para Telegram")
    logger.info("=" * 60)
    
    scraper = FootballScraper()
    
    # Criar um jogo de exemplo com probabilidades
    sample_match = {
        'home_team': 'Real Madrid',
        'away_team': 'Barcelona',
        'league': 'LaLiga',
        'time': '20:00',
        'score': '2-1',
        'probability': {
            'home_win': 55.25,
            'draw': 25.50,
            'away_win': 19.25,
            'confidence': 'high'
        }
    }
    
    try:
        formatted_message = scraper.format_match_for_telegram(sample_match)
        
        logger.info("✅ Mensagem formatada com sucesso!\n")
        logger.info("Prévia da mensagem para Telegram:")
        logger.info("-" * 60)
        logger.info(formatted_message)
        logger.info("-" * 60)
    
    except Exception as e:
        logger.error(f"❌ Erro ao formatar mensagem: {str(e)}")


def test_predictions():
    """Testa a obtenção de previsões"""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 4: Obtenção de Previsões")
    logger.info("=" * 60)
    
    scraper = FootballScraper()
    
    try:
        predictions = scraper.get_match_predictions()
        
        if predictions:
            logger.info(f"✅ Sucesso! Obtidas {len(predictions)} previsões")
            logger.info("\nPrimeira previsão:")
            if predictions:
                pred = predictions[0]
                logger.info(f"Jogo: {pred.get('home_team', 'N/A')} vs {pred.get('away_team', 'N/A')}")
                if pred.get('probability'):
                    logger.info(f"Probabilidade de vitória: {pred['probability']['home_win']}%")
        else:
            logger.warning("⚠️ Nenhuma previsão obtida.")
    
    except Exception as e:
        logger.error(f"❌ Erro ao obter previsões: {str(e)}")


def main():
    """Executa todos os testes"""
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 58 + "║")
    logger.info("║" + "  TESTES DO BOT DE FUTEBOL - MÓDULO DE SCRAPING".center(58) + "║")
    logger.info("║" + " " * 58 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    
    # Executar testes
    test_scraper_connection()
    test_probability_calculation()
    test_telegram_formatting()
    test_predictions()
    
    logger.info("\n" + "=" * 60)
    logger.info("TESTES CONCLUÍDOS")
    logger.info("=" * 60)
    logger.info("\n✅ Se todos os testes passaram, o bot está pronto para usar!")
    logger.info("❌ Se algum teste falhou, verifique os logs acima.\n")


if __name__ == "__main__":
    main()

