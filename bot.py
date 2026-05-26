import asyncio
import os
import requests
import random

from telegram import Bot
from dotenv import load_dotenv

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
# CACHE
# =====================================================

enviados = {}

# =====================================================
# AMAZON MOCK
# =====================================================

amazon_produtos = [

    {
        "titulo":
        "Echo Dot 5ª Geração",

        "preco":
        "299",

        "imagem":
        "https://m.media-amazon.com/images/I/61EXU8BuGZL._AC_SL1000_.jpg",

        "link":
        f"https://www.amazon.com.br/dp/B09B8VGCR8?tag={AMAZON_TAG}",

        "tipo":
        "amazon"
    },

    {
        "titulo":
        "Fire TV Stick",

        "preco":
        "249",

        "imagem":
        "https://m.media-amazon.com/images/I/51kkwT7uQtL._AC_SL1000_.jpg",

        "link":
        f"https://www.amazon.com.br/dp/B08C1W5N87?tag={AMAZON_TAG}",

        "tipo":
        "amazon"
    }

]

# =====================================================
# MERCADO LIVRE API
# =====================================================

def buscar_mercado_livre():

    produtos = []

    try:

        url = (
            "https://api.mercadolibre.com/"
            "sites/MLB/search?q=iphone"
        )

        response = requests.get(

            url,

            timeout=20

        )

        print(
            f"ML STATUS: "
            f"{response.status_code}"
        )

        data = response.json()

        for item in data["results"][:5]:

            produtos.append({

                "titulo":
                item["title"],

                "preco":
                str(item["price"]),

                "imagem":
                item["thumbnail"],

                "link":
                item["permalink"],

                "tipo":
                "mercadolivre"

            })

        print(
            f"ML PRODUTOS: "
            f"{len(produtos)}"
        )

    except Exception as e:

        print(
            "ERRO ML:",
            e
        )

    return produtos

# =====================================================
# TELEGRAM
# =====================================================

async def enviar_produto(produto):

    emoji = "🟧"

    if produto["tipo"] == "mercadolivre":

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

        await bot.send_photo(

            chat_id=CHAT_ID,

            photo=produto["imagem"],

            caption=texto

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

            produtos = []

            # AMAZON
            produtos.extend(
                random.sample(
                    amazon_produtos,
                    len(amazon_produtos)
                )
            )

            # MERCADO LIVRE
            produtos.extend(
                buscar_mercado_livre()
            )

            print(
                f"TOTAL PRODUTOS: "
                f"{len(produtos)}"
            )

            for produto in produtos:

                if produto["link"] in enviados:

                    continue

                await enviar_produto(
                    produto
                )

                enviados[
                    produto["link"]
                ] = True

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
