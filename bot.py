import asyncio
import os

from telegram import Bot
from dotenv import load_dotenv

# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

CHAT_ID = int(

    os.getenv(
        "TELEGRAM_CHAT_ID"
    )

)

bot = Bot(
    token=BOT_TOKEN
)

# =====================================================
# LOOP BOT
# =====================================================

async def loop_bot():

    print(
        "LOOP BOT INICIADO"
    )

    while True:

        try:

            print(
                "ENVIANDO TESTE TELEGRAM..."
            )

            await asyncio.wait_for(

                bot.send_message(

                    chat_id=CHAT_ID,

                    text="✅ BOT ONLINE"

                ),

                timeout=20

            )

            print(
                "MENSAGEM ENVIADA"
            )

        except Exception as e:

            print(
                "ERRO TELEGRAM:",
                e
            )

        await asyncio.sleep(60)
