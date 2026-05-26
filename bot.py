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

AMAZON_TAG = os.getenv(
    "AMAZON_ASSOCIATE_TAG",
    "promodudia-20"
)

bot = Bot(
    token=BOT_TOKEN
)

# =====================================================
# RSS
# =====================================================

RSS_URL = (
    "https://www.pelando.com.br/rss"
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

            headers={

                "User-Agent":
                "Mozilla/5.0",

                "Accept":
                "application/rss+xml, application/xml",

                "Connection":
                "close"

            },

            timeout=(5, 15),

            allow_redirects=True

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

        for item in items[:20]:

            try:

                titulo = item.title.text

                link = item.link.text

                descricao = ""

                if item.description:

                    descricao = item.description.text

                texto = (
                    titulo + " " + descricao
                ).lower()

                # =================================================
                # AMAZON
                # =================================================

                tipo = None

                if (
                    "amazon" in texto
                ):

                    tipo = "amazon"

                # =================================================
                # MERCADO LIVRE
                # =================================================

                elif (

                    "mercado livre" in texto
                    or "mercadolivre" in texto
                    or "meli" in texto

                ):

                    tipo = "mercadolivre"

                else:

                    continue

                print(
                    f"PROMO: {titulo}"
                )

                # =================================================
                # IMAGEM
                # =================================================

                imagem = None

                img = item.find("enclosure")

                if img:

                    imagem = img.get("url")

                # =================================================
                # PREÇO
                # =================================================

                preco = "0"

                preco_match = re.search(

                    r'R\\$\\s?[\\d\\.,]+',

                    descricao

                )

                if preco_match:

                    preco = (
                        preco_match.group(0)
                        .replace("R$", "")
                        .strip()
                    )

                # =================================================
                # TAG AMAZON
                # =================================================

                if tipo == "amazon":

                    asin_match = re.search(

                        r'/dp/([A-Z0-9]{10})',

                        link

                    )

                    if asin_match:

                        asin = asin_match.group(1)

                        link = (
                            f"https://www.amazon.com.br/dp/{asin}"
                            f"?tag={AMAZON_TAG}"
                        )

                produtos.append({

                    "titulo": titulo,

                    "preco": preco,

                    "imagem": imagem,

                    "link": link,

                    "tipo": tipo

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
        f"TOTAL PROMOS: "
        f"{len(produtos)}"
    )

    return produtos

# =====================================================
# TELEGRAM
# =====================================================

async def enviar_produto(produto):

    emoji = "🟦"

    if produto["tipo"] == "amazon":

        emoji = "🟧"

    elif produto["tipo"] == "mercadolivre":

        emoji = "🟨"

    texto = f"""
🔥 PROMOÇÃO

{emoji} Loja: {produto['tipo'].upper()}

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
