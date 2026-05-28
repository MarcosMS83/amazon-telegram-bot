import re
import asyncio
import os
import requests

from telethon import TelegramClient, events
from dotenv import load_dotenv

# =====================================================
# ENV
# =====================================================

load_dotenv()

API_ID = int(
    os.getenv("API_ID")
)

API_HASH = os.getenv(
    "API_HASH"
)

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN")
    
CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

AMAZON_TAG = os.getenv(
    "AMAZON_ASSOCIATE_TAG",
    "promodudia-20"
)

SOURCE_GROUPS = os.getenv(
    "SOURCE_GROUPS",
    ""
)

GRUPOS = [

    int(g.strip())

    for g in SOURCE_GROUPS.split(",")

    if g.strip()

]

print(
    f"GRUPOS MONITORADOS: "
    f"{GRUPOS}"
)

# =====================================================
# CACHE
# =====================================================

links_enviados = set()

# =====================================================
# EXTRAIR LINKS
# =====================================================

def extrair_links(texto):

    regex = r'(https?://[^\s]+)'

    return re.findall(
        regex,
        texto
    )

# =====================================================
# AMAZON TAG
# =====================================================

def adicionar_tag_amazon(link):

    try:

        if "amazon" not in link.lower():

            return link

        asin = re.search(

            r'/dp/([A-Z0-9]{10})',

            link

        )

        if asin:

            codigo = asin.group(1)

            novo_link = (
                f"https://www.amazon.com.br/dp/"
                f"{codigo}?tag={AMAZON_TAG}"
            )

            return novo_link

    except Exception as e:

        print(
            "ERRO AMAZON TAG:",
            e
        )

    return link

# =====================================================
# ENVIAR TELEGRAM
# =====================================================

def enviar_mensagem(texto):

    try:

        url = (
            f"https://api.telegram.org/bot"
            f"{BOT_TOKEN}/sendMessage"
        )

        payload = {

            "chat_id":
            CHAT_ID,

            "text":
            texto,

            "disable_web_page_preview":
            False

        }

        response = requests.post(

            url,

            data=payload,

            timeout=(5, 20)

        )

        print(
            f"MENSAGEM ENVIADA: "
            f"{response.status_code}"
        )

    except Exception as e:

        print(
            "ERRO ENVIO:",
            e
        )

# =====================================================
# MAIN
# =====================================================

async def main():

    print(
        "INICIANDO TELETHON..."
    )

    print(
        os.path.exists(
            "session.session"
        )
    )

    client = TelegramClient(
        "session",
        API_ID,
        API_HASH
    )

    # =================================================
    # EVENTO NOVA MSG
    # =================================================

    @client.on(events.NewMessage)

    async def nova_mensagem(event):

        try:

            # =========================================
            # FILTRO GRUPOS
            # =========================================

            if event.chat_id not in GRUPOS:

                return

            print(
                f"NOVA MSG: "
                f"{event.chat_id}"
            )

            texto = event.raw_text

            if not texto:

                return

            # =========================================
            # EXTRAIR LINKS
            # =========================================

            links = extrair_links(
                texto
            )

            print(
                f"LINKS: "
                f"{len(links)}"
            )

            # =========================================
            # PROCESSAR LINKS
            # =========================================

            for link in links:

                # =====================================
                # DUPLICADO
                # =====================================

                if link in links_enviados:

                    continue

                marketplaces = [

                    "amazon",
                    "mercadolivre",
                    "meli",
                    "shopee"

                ]

                valido = False

                for marketplace in marketplaces:

                    if marketplace in link.lower():

                        valido = True
                        break

                if not valido:

                    continue

                links_enviados.add(
                    link
                )

                # =====================================
                # AMAZON TAG
                # =====================================

                if "amazon" in link.lower():

                    link = adicionar_tag_amazon(
                        link
                    )

                # =====================================
                # MENSAGEM
                # =====================================

                mensagem = f"""
🔥 PROMOÇÃO ENCONTRADA

📦 Grupo:
{event.chat_id}

🛒 Link:
{link}
"""

                enviar_mensagem(
                    mensagem
                )

                print(
                    "PROMOÇÃO ENVIADA"
                )

        except Exception as e:

            print(
                "ERRO MSG:",
                e
            )

    # =================================================
    # START TELETHON
    # =================================================

    try:

        await client.start()

        print(
            "TELETHON ONLINE"
        )

    except Exception as e:

        print(
            "ERRO TELETHON:",
            e
        )

        return

    # =================================================
    # LOOP
    # =================================================

    await client.run_until_disconnected()
