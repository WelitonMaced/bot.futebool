# Bot Telegram de Futebol - Estatísticas e Probabilidades

Um bot do Telegram completo para fornecer estatísticas e probabilidades de jogos de futebol, auxiliando em apostas esportivas. O bot utiliza **web scraping** para obter dados de fontes públicas e oferece análises em tempo real.

## 🎯 Funcionalidades

- **Listagem de Jogos**: Visualize todos os jogos de hoje organizados por liga
- **Cálculo de Probabilidades**: Obtenha as probabilidades de vitória para cada jogo
- **Seleção de Ligas**: Customize suas preferências de ligas favoritas
- **Interface Amigável**: Comandos simples e intuitivos no Telegram
- **Análise Estatística**: Dados baseados em estatísticas públicas

## 📋 Requisitos

- Python 3.9+
- Pip (gerenciador de pacotes Python)
- Token de Bot Telegram (obtenha em [@BotFather](https://t.me/botfather))
- Conexão com a internet

## 🚀 Instalação Local

### 1. Clonar ou Baixar o Projeto

```bash
git clone <seu-repositorio>
cd football_bot
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Credenciais

Edite o arquivo `config.py` e adicione seu **Token do Bot Telegram**:

```python
TELEGRAM_BOT_TOKEN = "seu_token_aqui"
```

### 5. Executar o Bot Localmente

```bash
python3 bot.py
```

Se tudo estiver correto, você verá:
```
INFO:__main__:Iniciando Bot de Futebol...
INFO:__main__:Bot iniciado com sucesso!
INFO:__main__:Aguardando mensagens...
```

## 🌐 Deploy no Railway (Recomendado)

O Railway é uma plataforma gratuita e funcional para hospedar bots Python 24/7.

### Passo 1: Criar Conta no Railway

1. Acesse [railway.app](https://railway.app)
2. Clique em "Start a New Project"
3. Faça login com GitHub ou Email

### Passo 2: Conectar o Repositório

1. Clique em "Deploy from GitHub"
2. Selecione seu repositório do projeto
3. Autorize o Railway a acessar seu GitHub

### Passo 3: Configurar Variáveis de Ambiente

1. No painel do Railway, vá para "Variables"
2. Adicione a variável de ambiente:
   - **Nome**: `TELEGRAM_BOT_TOKEN`
   - **Valor**: Seu token do bot

### Passo 4: Deploy Automático

O Railway detectará o `Dockerfile` e fará o deploy automaticamente. Você verá:
```
✓ Build completed
✓ Deployment successful
```

### Passo 5: Verificar o Status

1. Vá para o painel do Railway
2. Verifique se o serviço está "Running"
3. Teste o bot no Telegram com o comando `/start`

## 📱 Usando o Bot

Após iniciar o bot, você pode usar os seguintes comandos no Telegram:

| Comando | Descrição |
|---------|-----------|
| `/start` | Mensagem de boas-vindas e instruções |
| `/jogos` | Listar todos os jogos de hoje |
| `/probabilidades` | Ver probabilidades de vitória |
| `/ligas` | Selecionar ligas de interesse |
| `/ajuda` | Obter ajuda e informações |
| `/sobre` | Informações sobre o bot |

## 🔧 Estrutura do Projeto

```
football_bot/
├── bot.py                 # Bot principal do Telegram
├── scraper.py            # Módulo de web scraping
├── config.py             # Configurações e credenciais
├── requirements.txt      # Dependências Python
├── Dockerfile            # Configuração para Docker
├── railway.json          # Configuração para Railway
├── .gitignore           # Arquivos a ignorar no Git
└── README.md            # Este arquivo
```

## 📊 Como Funciona

### 1. Web Scraping

O módulo `scraper.py` coleta dados de fontes públicas (como FlashScore) para obter:
- Informações dos times
- Horários dos jogos
- Ligas e competições
- Odds (probabilidades)

### 2. Processamento de Dados

Os dados coletados são processados para:
- Calcular probabilidades de vitória
- Organizar por liga
- Formatar para exibição no Telegram

### 3. Interação com o Usuário

O bot responde aos comandos do usuário e fornece:
- Listagens de jogos
- Análises de probabilidade
- Recomendações baseadas em dados

## ⚠️ Avisos Importantes

1. **Responsabilidade**: Use este bot apenas para fins informativos. As previsões não garantem 100% de precisão.
2. **Apostas Responsáveis**: Aposte apenas o que você pode perder. Nunca aposte mais do que seu orçamento permite.
3. **Termos de Serviço**: Respeite os termos de serviço dos sites de onde os dados são coletados.
4. **Atualização**: Os dados podem estar desatualizados. Sempre verifique as informações oficiais antes de tomar decisões.

## 🐛 Solução de Problemas

### O bot não responde

**Solução:**
1. Verifique se o token está correto em `config.py`
2. Verifique se o bot está rodando (veja os logs)
3. Reinicie o bot

### Erro ao fazer scraping

**Solução:**
1. Verifique sua conexão com a internet
2. O site de dados pode estar indisponível - tente novamente mais tarde
3. Verifique se a estrutura do site mudou (pode ser necessário atualizar o scraper)

### Deploy no Railway falha

**Solução:**
1. Verifique se o `Dockerfile` está correto
2. Verifique os logs no painel do Railway
3. Certifique-se de que todas as variáveis de ambiente estão configuradas

## 📚 Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação
- **python-telegram-bot**: Biblioteca para integração com Telegram
- **BeautifulSoup4**: Web scraping
- **Requests**: Requisições HTTP
- **Railway**: Hospedagem na nuvem
- **Docker**: Containerização

## 🤝 Contribuições

Contribuições são bem-vindas! Se você encontrar bugs ou tiver sugestões de melhorias, sinta-se livre para:

1. Abrir uma issue
2. Fazer um fork do projeto
3. Enviar um pull request

## 📝 Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Desenvolvedor

**Manus AI** - Assistente de IA para desenvolvimento de software

## 📞 Suporte

Para dúvidas ou problemas, você pode:

1. Verificar a seção de "Solução de Problemas" acima
2. Consultar a documentação oficial do [python-telegram-bot](https://docs.python-telegram-bot.org/)
3. Entrar em contato através do repositório do projeto

---

**Última atualização**: Outubro de 2025

**Versão**: 1.0.0

Aproveite o bot e aposte responsavelmente! ⚽🎯

