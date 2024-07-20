import logging
from datetime import datetime, timedelta
import random
import telebot
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configurações do bot
bot_token = '6249217860:AAHG26aMODZnU2kcSjIwrW_zRb3UVhd18z8'  # Substitua pelo seu token de bot
chat_id = "-1002013317198"
user_id = "5884590075"

LINK_SITE = '[JOGUE AGORA](https://sshortly1.com/8lxMRH)'

# Inicialização do bot
bot = telebot.TeleBot(token=bot_token)

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da sessão de requests com timeout e retry
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session = requests.Session()
session.mount("https://", adapter)
session.request = requests.request
telebot.apihelper.session = session

def generate_message():
    resultados = range(1, 26)
    aposta = random.sample(resultados, 5)
    dc = {i: "🟦" for i in range(1, 26)}
    
    for i in aposta:
        dc[i] = "🌟."

    bb = random.randint(3, 3)
    tt = random.randint(3, 3)
    ha = datetime.now()
    na = random.randint(3, 3)
    ta = timedelta(minutes=na)
    nh = (ha + ta).strftime('%H:%M')

    msg = (f'''
✅ ENTRADA CONFIRMADA ✅
Seguinte sinal gerado:
Aposte com: {bb} 💣

{dc[1]} {dc[2]} {dc[3]} {dc[4]} {dc[5]}
{dc[6]} {dc[7]} {dc[8]} {dc[9]} {dc[10]}
{dc[11]} {dc[12]} {dc[13]} {dc[14]} {dc[15]}
{dc[16]} {dc[17]} {dc[18]} {dc[19]} {dc[20]}
{dc[21]} {dc[22]} {dc[23]} {dc[24]} {dc[25]}

⏰ Válido até: {nh}
🎯 Tentativas: {tt}x
🖥 Site: {LINK_SITE}''')
    
    return msg, nh

def send_message_with_retry(chat_id, text):
    try:
        bot.send_message(chat_id=chat_id, text=text, parse_mode='MARKDOWN', disable_web_page_preview=True)
        logger.info("Message sent successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")

while True:
    try:
        msg, nh = generate_message()
        send_message_with_retry(user_id, msg)
        
        while True:
            hc = datetime.now().strftime('%H:%M')
            if hc == nh:
                send_message_with_retry(user_id, '✅ Sinal Expirado.')
                na = random.randint(120, 300)
                time.sleep(na)
                break
    except requests.exceptions.ReadTimeout:
        logger.error("Read timeout occurred, retrying in 60 seconds.")
        time.sleep(60)
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        time.sleep(60)  # Sleep for a minute before retrying
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        time.sleep(60)
