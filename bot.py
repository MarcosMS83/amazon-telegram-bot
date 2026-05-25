import os
import asyncio

from telegram import Bot
from dotenv import load_dotenv

from amazon_api import (
    buscar_promocoes_amazon
)

from filters import (
    produto_valido
)

# =====================================================
# CARREGA .ENV
# =====================================================

load_dotenv()

# =====================================================
# VARIÁVEIS
# =====================================================

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
# ENVIAR PRODUTO
# =====================================================

async def enviar_produto(produto):

    texto = f"""
🔥 PROMOÇÃO AMAZON

📦 {produto['titulo']}

💰 R$ {produto['preco']}

🛒 Comprar:
{produto['link']}

🏪 Origem:
{produto['origem']}
"""

    await bot.send_photo(

        chat_id=CHAT_ID,

        photo=produto["imagem"],

        caption=texto

    )

# =====================================================
# LOOP PRINCIPAL
# =====================================================

async def loop_promocoes():

    enviados = set()

    while True:

        try:

            produtos = (
                buscar_promocoes_amazon()
            )

            for produto in produtos:

                # evita repetidos
                if produto["link"] in enviados:
                    continue

                # filtro
                if not produto_valido(
                    produto
                ):
                    continue

                try:

                    await enviar_produto(
                        produto
                    )

                    enviados.add(
                        produto["link"]
                    )

                    print(
                        "ENVIADO:",
                        produto["titulo"]
                    )

                    # anti flood
                    await asyncio.sleep(10)

                except Exception as e:

                    print(
                        "ERRO ENVIO:",
                        e
                    )

            print(
                "AGUARDANDO NOVAS PROMOÇÕES..."
            )

        except Exception as e:

            print(
                "ERRO LOOP:",
                e
            )

        # procura promoções a cada 30 minutos
        await asyncio.sleep(1800)

# =====================================================

asyncio.run(
    loop_promocoes()
)
