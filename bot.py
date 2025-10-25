"""
Bot principal do Telegram para estatísticas e probabilidades de futebol.
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN, LEAGUES_OF_INTEREST
from scraper import FootballScraper

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializa o scraper
scraper = FootballScraper()

# --- Comandos do Bot ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas quando o comando /start é emitido."""
    user = update.effective_user
    welcome_message = (
        f"Olá, {user.first_name}! 👋\n\n"
        "Eu sou o seu Bot de Estatísticas de Futebol. Meu objetivo é te ajudar com análises e probabilidades para apostas esportivas.\n\n"
        "Use os comandos abaixo:\n"
        "⚽ /jogos - Lista os jogos de hoje.\n"
        "📈 /probabilidades - Mostra as probabilidades de vitória para os jogos.\n"
        "🏆 /ligas - Seleciona suas ligas favoritas.\n"
        "❓ /ajuda - Exibe esta mensagem de ajuda."
    )
    # Correção: Usando parse_mode='Markdown' para formatação simples
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def matches_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lista os jogos de hoje."""
    await update.message.reply_text("Buscando jogos de hoje...")
    
    try:
        matches = scraper.get_today_matches()
        
        if not matches:
            await update.message.reply_text("Nenhum jogo encontrado para hoje. Tente novamente mais tarde.")
            return

        response = "*Jogos de Hoje:*\n\n"
        
        current_league = ""
        for match in matches:
            if match['league'] != current_league:
                current_league = match['league']
                response += f"\n🏆 *{current_league}*\n"
            
            response += f"  - {match['home_team']} vs {match['away_team']} ({match['time']})\n"

        # Correção: Usando parse_mode='Markdown'
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Erro ao processar comando /jogos: {str(e)}")
        await update.message.reply_text("Ocorreu um erro interno. Por favor, tente novamente mais tarde ou use o comando /ajuda.")


async def probability_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra as probabilidades de vitória."""
    await update.message.reply_text("Calculando probabilidades para os jogos de hoje...")
    
    try:
        predictions = scraper.get_match_predictions()
        
        if not predictions:
            await update.message.reply_text("Não foi possível calcular as probabilidades. Verifique se há jogos hoje ou se a fonte de dados está disponível.")
            return

        response = "*Probabilidades de Vitória:*\n\n"
        
        current_league = ""
        for pred in predictions:
            if pred['league'] != current_league:
                current_league = pred['league']
                response += f"\n🏆 *{current_league}*\n"
            
            prob = pred['probability']
            
            # Determina o time com a maior probabilidade (excluindo empate)
            if prob['home_win'] > prob['away_win']:
                winner = pred['home_team']
                win_prob = prob['home_win']
            else:
                winner = pred['away_team']
                win_prob = prob['away_win']
                
            response += (
                f"  - {pred['home_team']} vs {pred['away_team']} ({pred['time']})\n"
                f"    *Tendência:* {winner} ({win_prob}%)\n"
                f"    *Confiança:* {prob['confidence'].upper()}\n"
            )
            
        # Correção: Usando parse_mode='Markdown'
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Erro ao processar comando /probabilidades: {str(e)}")
        await update.message.reply_text("Ocorreu um erro interno. Por favor, tente novamente mais tarde ou use o comando /ajuda.")


async def leagues_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Permite selecionar ligas favoritas (funcionalidade simplificada)."""
    leagues_list = "\n".join([f"- {league}" for league in LEAGUES_OF_INTEREST])
    response = (
        "*Ligas Atuais Monitoradas:*\n\n"
        f"{leagues_list}\n\n"
        "Para adicionar ou remover ligas, você precisará editar o arquivo `config.py` no repositório do GitHub e fazer um novo deploy."
    )
    # Correção: Usando parse_mode='Markdown'
    await update.message.reply_text(response, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe a mensagem de ajuda."""
    await start_command(update, context)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informações sobre o bot."""
    response = (
        "*Sobre o Bot:*\n\n"
        "Desenvolvido por Manus AI.\n"
        "Versão: 1.0.0\n"
        "Este bot usa dados de fontes públicas (simuladas) para calcular probabilidades de jogos de futebol.\n\n"
        "Lembre-se: Use para fins informativos e aposte com responsabilidade."
    )
    # Correção: Usando parse_mode='Markdown'
    await update.message.reply_text(response, parse_mode='Markdown')

# --- Tratamento de Erros ---

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Loga o erro e envia uma mensagem de erro para o usuário."""
    logger.error("Exceção capturada:", exc_info=context.error)
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Ocorreu um erro interno. Por favor, tente novamente mais tarde ou use o comando /ajuda."
        )

# --- Função Principal ---

if __name__ == '__main__':
    # A função main é chamada de forma síncrona para iniciar o bot
    # O run_polling() dentro de main() gerencia o loop de eventos
    try:
        # Cria o ApplicationBuilder
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Adiciona os Handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("jogos", matches_command))
        application.add_handler(CommandHandler("probabilidades", probability_command))
        application.add_handler(CommandHandler("ligas", leagues_command))
        application.add_handler(CommandHandler("ajuda", help_command))
        application.add_handler(CommandHandler("sobre", about_command))

        # Adiciona o Handler de erros
        application.add_error_handler(error_handler)

        logger.info("Bot iniciado com sucesso! Aguardando mensagens...")
        
        # Usa run_polling() para iniciar o bot de forma síncrona,
        # o que é mais compatível com o ambiente do Railway/Docker
        application.run_polling(poll_interval=1.0)
        
    except Exception as e:
        logger.error(f"Erro fatal na inicialização do bot: {str(e)}")

async def matches_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lista os jogos de hoje."""
    await update.message.reply_text("Buscando jogos de hoje...")
    
    matches = scraper.get_today_matches()
    
    if not matches:
        await update.message.reply_text("Nenhum jogo encontrado para hoje. Tente novamente mais tarde.")
        return

    response = "*Jogos de Hoje:*\n\n"
    
    current_league = ""
    for match in matches:
        if match['league'] != current_league:
            current_league = match['league']
            response += f"\n🏆 *{current_league}*\n"
        
        response += f"  - {match['home_team']} vs {match['away_team']} ({match['time']})\n"

    await update.message.reply_markdown_v2(response)

async def probability_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra as probabilidades de vitória."""
    await update.message.reply_text("Calculando probabilidades para os jogos de hoje...")
    
    predictions = scraper.get_match_predictions()
    
    if not predictions:
        await update.message.reply_text("Não foi possível calcular as probabilidades. Verifique se há jogos hoje ou se a fonte de dados está disponível.")
        return

    response = "*Probabilidades de Vitória:*\n\n"
    
    current_league = ""
    for pred in predictions:
        if pred['league'] != current_league:
            current_league = pred['league']
            response += f"\n🏆 *{current_league}*\n"
        
        prob = pred['probability']
        
        # Determina o time com a maior probabilidade (excluindo empate)
        if prob['home_win'] > prob['away_win']:
            winner = pred['home_team']
            win_prob = prob['home_win']
        else:
            winner = pred['away_team']
            win_prob = prob['away_win']
            
        response += (
            f"  - {pred['home_team']} vs {pred['away_team']} ({pred['time']})\n"
            f"    *Tendência:* {winner} ({win_prob}%)\n"
            f"    *Confiança:* {prob['confidence'].upper()}\n"
        )
        
    await update.message.reply_markdown_v2(response)


async def leagues_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Permite selecionar ligas favoritas (funcionalidade simplificada)."""
    leagues_list = "\n".join([f"- {league}" for league in LEAGUES_OF_INTEREST])
    response = (
        "*Ligas Atuais Monitoradas:*\n\n"
        f"{leagues_list}\n\n"
        "Para adicionar ou remover ligas, você precisará editar o arquivo `config.py` no repositório do GitHub e fazer um novo deploy."
    )
    await update.message.reply_markdown_v2(response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe a mensagem de ajuda."""
    await start_command(update, context)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informações sobre o bot."""
    response = (
        "*Sobre o Bot:*\n\n"
        "Desenvolvido por Manus AI.\n"
        "Versão: 1.0.0\n"
        "Este bot usa dados de fontes públicas (simuladas) para calcular probabilidades de jogos de futebol.\n\n"
        "Lembre-se: Use para fins informativos e aposte com responsabilidade."
    )
    await update.message.reply_markdown_v2(response)

# --- Tratamento de Erros ---

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Loga o erro e envia uma mensagem de erro para o usuário."""
    logger.error("Exceção capturada:", exc_info=context.error)
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Ocorreu um erro interno. Por favor, tente novamente mais tarde ou use o comando /ajuda."
        )

# --- Função Principal ---

# A função main() foi modificada para usar run_polling()
async def main() -> None:
    """Inicia o bot usando o método run_polling para compatibilidade com o Railway."""
    # Cria o ApplicationBuilder
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Adiciona os Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("jogos", matches_command))
    application.add_handler(CommandHandler("probabilidades", probability_command))
    application.add_handler(CommandHandler("ligas", leagues_command))
    application.add_handler(CommandHandler("ajuda", help_command))
    application.add_handler(CommandHandler("sobre", about_command))

    # Adiciona o Handler de erros
    application.add_error_handler(error_handler)

    logger.info("Bot iniciado com sucesso! Aguardando mensagens...")
    
    # Usa run_polling() para iniciar o bot de forma síncrona,
    # o que é mais compatível com o ambiente do Railway/Docker
    application.run_polling(poll_interval=1.0)


if __name__ == '__main__':
    # A função main é chamada de forma síncrona para iniciar o bot
    # O run_polling() dentro de main() gerencia o loop de eventos
    try:
        # Cria o ApplicationBuilder
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Adiciona os Handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("jogos", matches_command))
        application.add_handler(CommandHandler("probabilidades", probability_command))
        application.add_handler(CommandHandler("ligas", leagues_command))
        application.add_handler(CommandHandler("ajuda", help_command))
        application.add_handler(CommandHandler("sobre", about_command))

        # Adiciona o Handler de erros
        application.add_error_handler(error_handler)

        logger.info("Bot iniciado com sucesso! Aguardando mensagens...")
        
        # Usa run_polling() para iniciar o bot de forma síncrona,
        # o que é mais compatível com o ambiente do Railway/Docker
        application.run_polling(poll_interval=1.0)
        
    except Exception as e:
        logger.error(f"Erro fatal na inicialização do bot: {str(e)}")
