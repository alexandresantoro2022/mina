import logging
from datetime import datetime, timedelta
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os

# Configurações do bot
bot_token ="6673968105:AAFHgDcPJWr49bXzFrO1o4dURjpNGxGStcA"  # Use variáveis de ambiente para segurança
chat_id ="-1002249980702"  # Substitua pelo chat_id do seu grupo ou canal
user_id = "5884590075"  # Substitua pelo user
LINK_SITE_1 = 'https://sshortly1.com/8lxMRH'
LINK_SITE_2 = 'https://api.whatsapp.com/send?phone=5511979577190&text=TENHA%20SUA%20SALA%20DE%20SINAIS%20E%20GANHE%20DINHEIRO%20ONLINE%20POR%20APENAS%20%20R$:79,90%20TENHA%20SEU%20PROPRIO%20BOTSINAIS%20MINES'

# Inicialização do bot
bot = telebot.TeleBot(token=bot_token)

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuração da sessão de requests com timeout e retry
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session = requests.Session()
session.mount("https://", adapter)
telebot.apihelper.session = session

def generate_message():
    resultados = range(1, 26)
    aposta = random.sample(resultados, 5)
    dc = {i: "🟦" for i in range(1, 26)}

    for i in aposta:
        dc[i] = "💎"

    bb = random.randint(3, 3)
    tt = random.randint(3, 3)
    ha = datetime.now()
    na = random.randint(3, 3)
    ta = timedelta(minutes=na)
    nh = (ha + ta).strftime('%H:%M')

    msg = (f'''
✅ENTRADACONFIRMADA✅
 
APOSTE COM: {bb} 💣
🎯 TENTATIVAS: {tt}X
🎲 CASA PLAYPIX
🎮 MINES

{dc[1]} {dc[2]} {dc[3]} {dc[4]} {dc[5]}
{dc[6]} {dc[7]} {dc[8]} {dc[9]} {dc[10]}
{dc[11]} {dc[12]} {dc[13]} {dc[14]} {dc[15]}
{dc[16]} {dc[17]} {dc[18]} {dc[19]} {dc[20]}
{dc[21]} {dc[22]} {dc[23]} {dc[24]} {dc[25]}
⬇️DEPÓSITO MÍNIMO R$30,00⬇️
''')

    return msg, nh

def send_message_with_retry(chat_id, text, reply_markup=None):
    try:
        bot.send_message(chat_id=chat_id, text=text, parse_mode='MARKDOWN', disable_web_page_preview=True, reply_markup=reply_markup)
        logger.info("Message sent successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
    except telebot.apihelper.ApiException as e:
        logger.error(f"Telegram API error: {e}")

def create_inline_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="🤑 CADASTRE-SE", url=LINK_SITE_1)
    button2 = InlineKeyboardButton(text="��TENHA SUA SALA DE SINAIS", url=LINK_SITE_2)
  
    keyboard.add(button1)
    keyboard.add(button2)

    return keyboard

def main():
    while True:
        try:
            logger.info(f"Using chat_id: {chat_id}")
            msg, nh = generate_message()
            keyboard = create_inline_keyboard()
            logger.info(f"Sending message to chat_id {chat_id}: {msg}")
            send_message_with_retry(chat_id, msg, reply_markup=keyboard)

            while True:
                hc = datetime.now().strftime('%H:%M')
                if hc == nh:
                    logger.info(f"Sending final signal message to chat_id {chat_id}.")
                    send_message_with_retry(chat_id, '🚨 ENTRADA FINALIZADA 🚨✅✅ VITORIA! ✅✅.')
                    na = random.randint(120, 300)
                    time.sleep(na)
                    break
                time.sleep(10)  # Check time every 10 seconds to avoid excessive looping
        except requests.exceptions.ReadTimeout:
            logger.error("Read timeout occurred, retrying in 60 seconds.")
            time.sleep(60)
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            time.sleep(60)  # Sleep for a minute before retrying
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            time.sleep(60)  # Sleep for a minute before retrying

if __name__ == "__main__":
    main()
