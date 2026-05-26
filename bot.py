import os
import asyncio

from telegram import Bot
from dotenv import load_dotenv

# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

bot = Bot(
    token=BOT_TOKEN
)

# =====================================================
# LOOP
# =====================================================

async def loop_bot():

    while True:

        try:

            texto = """
🔥 TESTE PROMOÇÃO

📦 Echo Dot 5ª Geração

💰 R$ 299

🛒 https://www.amazon.com.br/

🏪 Amazon
"""

            await bot.send_photo(

                chat_id=CHAT_ID,

                photo="https://m.media-amazon.com/images/I/714Rq4k05UL._AC_SL1000_.jpg",

                caption=texto

            )

            print(
                "MENSAGEM ENVIADA"
            )

        except Exception as e:

            print(
                "ERRO:",
                e
            )

        await asyncio.sleep(600)

# =====================================================
# START
# =====================================================

def start_bot():

    asyncio.run(
        loop_bot()
    )
# =====================================================
# START BOT
# =====================================================

def start_bot():

    print(
        "START BOT EXECUTADO"
    )

    asyncio.run(
        loop_bot()
    )
