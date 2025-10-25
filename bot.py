import logging
import os
import asyncio
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from scraper import FootballScraper
from openai import OpenAI

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Instância global do scraper
scraper = FootballScraper()

# --- CONFIGURAÇÃO DA API DE IA ---
# A chave da API de IA deve ser configurada como variável de ambiente no Railway (ex: OPENAI_API_KEY)
# O valor que você forneceu é: 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
# O código irá ler a variável de ambiente:
AI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Inicializa o cliente OpenAI
if AI_API_KEY:
    ai_client = OpenAI(api_key=AI_API_KEY)
else:
    ai_client = None
    logger.warning("OPENAI_API_KEY não configurada. Funções de IA estarão desabilitadas.")

def get_ai_response(prompt: str) -> str:
    """
    Chama a API de IA para gerar uma resposta detalhada.
    """
    if not ai_client:
        return "Desculpe, a função de Inteligência Artificial está desabilitada (chave de API não configurada)."

    try:
        # Usando um modelo rápido e capaz de raciocínio
        response = ai_client.chat.completions.create(
            model="gpt-4.1-mini", # Modelo disponível no ambiente
            messages=[
                {"role": "system", "content": "Você é um assistente de análise esportiva. Responda de forma detalhada, profissional e use Markdown para formatar a resposta."},
                {"role": "user", "content": prompt}
            ]
        )
        # Retorna o texto gerado pela IA
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Erro ao chamar a API de IA: {e}")
        return "❌ Ocorreu um erro ao processar a solicitação com a Inteligência Artificial."
# --- FIM DA CONFIGURAÇÃO DA API DE IA ---


class FootballBotHandler:
    """Classe para gerenciar os handlers do bot"""
    
    def __init__(self):
        self.scraper = FootballScraper()
        self.user_preferences = {}  # Armazenar preferências de ligas por usuário
        # Adicionando um estado para o comando /analisar
        self.awaiting_analysis_query = {}
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /start - Mensagem de boas-vindas"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        welcome_message = f"""
🎯 *Bem-vindo ao Bot de Futebol!* 🎯

Olá {user_name}! 👋

Sou seu assistente de estatísticas e probabilidades de futebol. 
Estou aqui para ajudar você com previsões de jogos e análises para suas apostas! ⚽

*Comandos disponíveis:*

/jogos - Ver todos os jogos de hoje
/probabilidades - Ver probabilidades de vitória
/analisar - Pedir uma análise detalhada à Inteligência Artificial
/ligas - Selecionar ligas de interesse
/ajuda - Obter ajuda
/sobre - Informações sobre o bot

Escolha um comando acima para começar! 🚀
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        logger.info(f"Usuário {user_id} iniciou o bot")
    
    async def jogos(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /jogos - Listar todos os jogos de hoje"""
        try:
            await update.message.reply_text("🔄 Buscando jogos de hoje... Por favor, aguarde.", parse_mode='Markdown')
            
            matches = self.scraper.get_today_matches()
            
            if not matches:
                await update.message.reply_text(
                    "❌ Desculpe, não consegui encontrar jogos de hoje no momento.\n"
                    "Tente novamente mais tarde.",
                    parse_mode='Markdown'
                )
                return
            
            # Agrupar jogos por liga
            matches_by_league = {}
            for match in matches:
                league = match.get('league', 'Sem Liga')
                if league not in matches_by_league:
                    matches_by_league[league] = []
                matches_by_league[league].append(match)
            
            # Enviar mensagens por liga
            for league, league_matches in list(matches_by_league.items())[:5]:  # Limitar a 5 ligas
                message = f"🏆 *{league}*\n\n"
                for match in league_matches[:3]:  # Limitar a 3 jogos por liga
                    message += f"⚽ {match.get('home_team', 'Time A')} vs {match.get('away_team', 'Time B')}\n"
                    if match.get('time'):
                        message += f"🕐 {match['time']}\n"
                    message += "\n"
                
                await update.message.reply_text(message, parse_mode='Markdown')
                await asyncio.sleep(0.5)  # Pequeno delay entre mensagens
            
            logger.info(f"Usuário {update.effective_user.id} consultou jogos de hoje")
        
        except Exception as e:
            logger.error(f"Erro ao listar jogos: {str(e)}")
            await update.message.reply_text(
                "❌ Ocorreu um erro ao buscar os jogos. Tente novamente.",
                parse_mode='Markdown'
            )
    
    async def probabilidades(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /probabilidades - Mostrar probabilidades de vitória"""
        try:
            await update.message.reply_text("🔄 Calculando probabilidades... Por favor, aguarde.", parse_mode='Markdown')
            
            predictions = self.scraper.get_match_predictions()
            
            if not predictions:
                await update.message.reply_text(
                    "❌ Desculpe, não consegui calcular probabilidades no momento.",
                    parse_mode='Markdown'
                )
                return
            
            # Enviar as 5 melhores previsões
            for idx, match in enumerate(predictions[:5], 1):
                formatted_message = self.scraper.format_match_for_telegram(match)
                await update.message.reply_text(formatted_message, parse_mode='Markdown')
                await asyncio.sleep(0.5)
            
            logger.info(f"Usuário {update.effective_user.id} consultou probabilidades")
        
        except Exception as e:
            logger.error(f"Erro ao calcular probabilidades: {str(e)}")
            await update.message.reply_text(
                "❌ Ocorreu um erro ao calcular as probabilidades. Tente novamente.",
                parse_mode='Markdown'
            )
    
    async def analisar_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /analisar - Inicia o modo de análise por IA."""
        if not ai_client:
            await update.message.reply_text(
                "❌ A função de Inteligência Artificial está desabilitada. Por favor, configure a variável de ambiente `OPENAI_API_KEY` no Railway.",
                parse_mode='Markdown'
            )
            return

        user_id = update.effective_user.id
        self.awaiting_analysis_query[user_id] = True
        
        await update.message.reply_text(
            "🧠 *Modo de Análise IA Ativado.*\n\n"
            "Envie sua pergunta ou solicitação de análise detalhada sobre qualquer jogo ou estatística. "
            "Ex: 'Qual a chance do time X vencer o time Y hoje?'\n\n"
            "Para sair, use o comando /cancelar.",
            parse_mode='Markdown'
        )

    async def analisar_process(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Processa a mensagem do usuário no modo de análise IA."""
        user_id = update.effective_user.id
        
        if self.awaiting_analysis_query.get(user_id):
            query = update.message.text
            
            # Remove o estado de espera para evitar processamento duplicado
            self.awaiting_analysis_query[user_id] = False
            
            # Mensagem de processamento
            await update.message.reply_text("⏳ *Processando sua solicitação de análise IA...* Isso pode levar alguns segundos.", parse_mode='Markdown')
            
            # Chama a função de IA de forma assíncrona
            loop = asyncio.get_event_loop()
            response_text = await loop.run_in_executor(None, get_ai_response, query)
            
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
            logger.info(f"Usuário {user_id} recebeu resposta da IA para a query: {query[:50]}...")
        else:
            # Caso não esteja no modo de análise, apenas ignora ou usa outro handler
            pass

    async def cancelar(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /cancelar - Sai do modo de análise IA."""
        user_id = update.effective_user.id
        if self.awaiting_analysis_query.pop(user_id, False):
            await update.message.reply_text("✅ Modo de Análise IA cancelado. Você pode usar outros comandos.", parse_mode='Markdown')
        else:
            await update.message.reply_text("Você não estava no modo de Análise IA.", parse_mode='Markdown')

    async def ligas(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /ligas - Selecionar ligas de interesse"""
        keyboard = [
            [InlineKeyboardButton("Premier League", callback_data='liga_premier')],
            [InlineKeyboardButton("LaLiga", callback_data='liga_laliga')],
            [InlineKeyboardButton("Serie A", callback_data='liga_seriea')],
            [InlineKeyboardButton("Bundesliga", callback_data='liga_bundesliga')],
            [InlineKeyboardButton("Ligue 1", callback_data='liga_ligue1')],
            [InlineKeyboardButton("Campeonato Brasileiro", callback_data='liga_brasileirao')],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🏆 *Selecione as ligas de seu interesse:*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def ajuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /ajuda - Mostrar ajuda"""
        help_text = """
*📚 Ajuda do Bot*

Este bot fornece estatísticas e probabilidades de jogos de futebol para auxiliar em apostas.

*Como usar:*

1. **/jogos** - Veja todos os jogos de hoje
2. **/probabilidades** - Veja as probabilidades de vitória
3. **/analisar** - Peça uma análise detalhada à Inteligência Artificial
4. **/ligas** - Selecione suas ligas favoritas
5. **/sobre** - Informações sobre o bot

*Informações importantes:*

⚠️ As probabilidades são baseadas em dados públicos e análises estatísticas.
⚠️ Não garantimos 100% de precisão nas previsões.
⚠️ Use este bot apenas para fins informativos.
⚠️ Aposte responsavelmente!

*Dúvidas?*
Entre em contato com o desenvolvedor através do repositório do projeto.
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def sobre(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Comando /sobre - Informações sobre o bot"""
        about_text = """
*ℹ️ Sobre o Bot de Futebol*

*Versão:* 2.0.0 (com integração de IA)
*Desenvolvido por:* Manus AI
*Data de criação:* 2025

*Funcionalidades:*
✅ Estatísticas de jogos de futebol
✅ Cálculo de probabilidades
✅ Análise detalhada por Inteligência Artificial
✅ Suporte a múltiplas ligas
✅ Interface amigável no Telegram

*Fonte de dados:*
Os dados são coletados de fontes públicas através de web scraping e a análise é feita pela Inteligência Artificial.

*Aviso Legal:*
Este bot é fornecido "como está" e não oferece garantias de precisão.
Use por sua conta e risco!
        """
        
        await update.message.reply_text(about_text, parse_mode='Markdown')
    
    async def handle_league_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler para seleção de ligas"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        league_map = {
            'liga_premier': 'Premier League',
            'liga_laliga': 'LaLiga',
            'liga_seriea': 'Serie A',
            'liga_bundesliga': 'Bundesliga',
            'liga_ligue1': 'Ligue 1',
            'liga_brasileirao': 'Campeonato Brasileiro',
        }
        
        selected_league = league_map.get(query.data)
        if selected_league:
            if user_id not in self.user_preferences:
                self.user_preferences[user_id] = []
            
            if selected_league not in self.user_preferences[user_id]:
                self.user_preferences[user_id].append(selected_league)
                await query.edit_message_text(
                    f"✅ {selected_league} adicionada às suas preferências!"
                )
            else:
                await query.edit_message_text(
                    f"ℹ️ {selected_league} já está nas suas preferências!"
                )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler de erros"""
        logger.error(f"Erro no bot: {context.error}")
        if update and update.message:
            await update.message.reply_text(
                "❌ Ocorreu um erro. Tente novamente mais tarde.",
                parse_mode='Markdown'
            )


async def main():
    """Função principal para iniciar o bot"""
    logger.info("Iniciando Bot de Futebol...")
    
    # Criar aplicação
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Instanciar handler
    handler = FootballBotHandler()
    
    # Registrar handlers de comandos
    application.add_handler(CommandHandler("start", handler.start))
    application.add_handler(CommandHandler("jogos", handler.jogos))
    application.add_handler(CommandHandler("probabilidades", handler.probabilidades))
    application.add_handler(CommandHandler("analisar", handler.analisar_start)) # NOVO
    application.add_handler(CommandHandler("cancelar", handler.cancelar)) # NOVO
    application.add_handler(CommandHandler("ligas", handler.ligas))
    application.add_handler(CommandHandler("ajuda", handler.ajuda))
    application.add_handler(CommandHandler("sobre", handler.sobre))
    
    # Handler para processar a mensagem no modo de análise IA
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handler.analisar_process))
    
    # Registrar handler de callbacks
    application.add_handler(CallbackQueryHandler(handler.handle_league_selection))
    
    # Registrar handler de erros
    application.add_error_handler(handler.error_handler)
    
    logger.info("Bot iniciado com sucesso!")
    logger.info("Aguardando mensagens...")
    
    # Iniciar o bot
    await application.run_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}")
