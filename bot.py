import asyncio
import os
import requests
import feedparser
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

    try:

        feed = feedparser.parse(
            RSS_URL
        )

        print(
            f"RSS ENTRIES: "
            f"{len(feed.entries)}"
        )

        for entry in feed.entries[:20]:

            try:

                titulo = entry.title

                link_post = entry.link

                print(
                    f"ANALISANDO: {titulo}"
                )

                response = requests.get(

                    link_post,

                    timeout=20,

                    headers={
                        "User-Agent":
                        "Mozilla/5.0"
                    }

                )

                soup = BeautifulSoup(

                    response.text,

                    "html.parser"

                )

                links = soup.find_all(
                    "a",
                    href=True
                )

                amazon_link = None

                for a in links:

                    href = a["href"]

                    if (
                        "amazon.com.br" in href
                        or "amzn.to" in href
                    ):

                        amazon_link = href
                        break

                if not amazon_link:

                    continue

                asin_match = re.search(

                    r'/dp/([A-Z0-9]{10})',

                    amazon_link

                )

                if asin_match:

                    asin = asin_match.group(1)

                    amazon_link = (
                        f"https://www.amazon.com.br/dp/{asin}"
                        f"?tag={TAG}"
                    )

                preco = "0"

                preco_match = re.search(

                    r'R\\$\\s?[\\d\\.,]+',

                    soup.get_text()

                )

                if preco_match:

                    preco = (
                        preco_match.group(0)
                        .replace("R$", "")
                        .strip()
                    )

                imagem = None

                img = soup.find("img")

                if img:

                    imagem = img.get("src")

                produtos.append({

                    "titulo": titulo,

                    "preco": preco,

                    "imagem": imagem,

                    "link": amazon_link

                })

                print(
                    f"PROMO ENCONTRADA: "
                    f"{titulo}"
                )

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
        f"TOTAL PROMOS: "
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
