import asyncio
import os
import requests

from dotenv import load_dotenv

# =====================================================
# ENV
# =====================================================

load_dotenv()

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

AMAZON_TAG = os.getenv(
    "AMAZON_ASSOCIATE_TAG",
    "promodudia-20"
)

# =====================================================
# CACHE
# =====================================================

enviados = {}

# =====================================================
# AMAZON
# =====================================================

amazon_produtos = [

    {
        "titulo":
        "Echo Dot 5ª Geração Alexa",

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
        "Fire TV Stick Amazon",

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
# MERCADO LIVRE
# =====================================================

def buscar_mercado_livre():

    produtos = []

    try:

        print(
            "CONSULTANDO ML..."
        )

        url = (
            "https://api.mercadolibre.com/"
            "sites/MLB/search?q=iphone"
        )

        response = requests.get(

            url,

            timeout=(5, 15)

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

def enviar_telegram(produto):

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

        print(
            f"ENVIANDO: "
            f"{produto['titulo']}"
        )

        url = (
            f"https://api.telegram.org/bot"
            f"{BOT_TOKEN}/sendPhoto"
        )

        payload = {

            "chat_id":
            CHAT_ID,

            "photo":
            produto["imagem"],

            "caption":
            texto

        }

        response = requests.post(

            url,

            data=payload,

            timeout=(5, 20)

        )

        print(
            f"TELEGRAM STATUS: "
            f"{response.status_code}"
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

            print(
                "MONTANDO PRODUTOS..."
            )

            produtos = []

            # AMAZON
            for p in amazon_produtos:

                produtos.append(p)

            # ML
            produtos_ml = buscar_mercado_livre()

            for p in produtos_ml:

                produtos.append(p)

            print(
                f"TOTAL PRODUTOS: "
                f"{len(produtos)}"
            )

            for produto in produtos:

                if produto["link"] in enviados:

                    continue

                enviar_telegram(
                    produto
                )

                enviados[
                    produto["link"]
                ] = True

                await asyncio.sleep(10)

        except Exception as e:

            print(
                "ERRO LOOP:",
                e
            )

        print(
            "AGUARDANDO 10 MIN..."
        )

        await asyncio.sleep(600)
