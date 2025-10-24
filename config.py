# Configuração do Bot Telegram de Futebol
# ========================================

# Token do Bot Telegram
TELEGRAM_BOT_TOKEN = "8284008980:AAFGBhdZlWAzSsv6r9OJnai5K2k_4rQW61g"

# Configurações de Scraping
FLASHSCORE_BASE_URL = "https://www.flashscore.com"
FLASHSCORE_FOOTBALL_URL = "https://www.flashscore.com/football/"

# Configurações de Timeout e Retry
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

# Headers para requisições HTTP
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Ligas de Interesse (pode ser expandido)
LEAGUES_OF_INTEREST = [
    "Premier League",
    "LaLiga",
    "Serie A",
    "Bundesliga",
    "Ligue 1",
    "Campeonato Brasileiro",
    "Champions League",
    "Europa League",
]

# Configurações de Logging
LOG_LEVEL = "INFO"
LOG_FILE = "football_bot.log"

