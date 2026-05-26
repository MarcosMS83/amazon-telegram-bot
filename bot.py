import asyncio
import os
import requests
import re

from telegram import Bot
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# =====================================================
# ENV
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

TAG = os.getenv(
    "AMAZON_ASSOCIATE_TAG",
    "promodudia-20"
)

bot = Bot(
    token=BOT_TOKEN
)

# =====================================================
# RSS PROMOBIT
# =====================================================

RSS_URL = (
    "https://www.promobit.com.br/feed/"
)

# =====================================================
# CACHE
# =====================================================

enviados = {}

# =====================================================
# BUSCAR PROMOÇÕES
# =====================================================

def buscar_promocoes():

    produtos = []

    print(
        "INICIANDO RSS..."
    )

    try:

        response = requests.get(

            RSS_URL,

            timeout=20,

            headers={
                "User-Agent":
                "Mozilla/5.0"
            }

        )

        print(
            f"RSS STATUS: "
            f"{response.status_code}"
        )

        soup = BeautifulSoup(

            response.text,

            "xml"

        )

        items = soup.find_all(
            "item"
        )

        print(
            f"RSS ITEMS: "
            f"{len(items)}"
        )

        for item in items[:10]:

            try:

                titulo = item.title.text

                link = item.link.text

                print(
                    f"POST: {titulo}"
                )

                produtos.append({

                    "titulo": titulo,

                    "preco": "0",

                    "imagem": None,

                    "link": link

                })

            except Exception as e:

                print(
                    "ERRO ITEM:",
                    e
                )

    except Exception as e:

        print(
            "ERRO RSS:",
            e
        )

    print(
        f"TOTAL PRODUTOS: "
        f"{len(produtos)}"
    )

    return produtos

# =====================================================
# ENVIAR TELEGRAM
# =====================================================

async def enviar_produto(produto):

    texto = f"""
🔥 PROMOÇÃO AMAZON

📦 {produto['titulo']}

💰 R$ {produto['preco']}

🛒 Comprar:
{produto['link']}
"""

    try:

        if produto["imagem"]:

            await asyncio.wait_for(

                bot.send_photo(

                    chat_id=CHAT_ID,

                    photo=produto["imagem"],

                    caption=texto

                ),

                timeout=30

            )

        else:

            await asyncio.wait_for(

                bot.send_message(

                    chat_id=CHAT_ID,

                    text=texto

                ),

                timeout=30

            )

        print(
            "PROMO ENVIADA"
        )

    except Exception as e:

        print(
            "ERRO TELEGRAM:",
            e
        )

# =====================================================
# LOOP
# =====================================================

async def loop_bot():

    print(
        "LOOP BOT INICIADO"
    )

    while True:

        try:

            produtos = buscar_promocoes()

            agora = asyncio.get_event_loop().time()

            expirados = []

            for k, v in enviados.items():

                if agora - v > 43200:

                    expirados.append(k)

            for k in expirados:

                del enviados[k]

            for produto in produtos:

                if produto["link"] in enviados:

                    continue

                await enviar_produto(
                    produto
                )

                enviados[
                    produto["link"]
                ] = agora

                await asyncio.sleep(15)

        except Exception as e:

            print(
                "ERRO LOOP:",
                e
            )

        print(
            "AGUARDANDO 10 MIN..."
        )

        await asyncio.sleep(600)
