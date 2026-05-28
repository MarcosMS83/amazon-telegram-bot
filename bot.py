import re
import os
import asyncio
import requests

from telethon import TelegramClient, events
from dotenv import load_dotenv

# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()

API_ID = int(
    os.getenv("API_ID")
)

API_HASH = os.getenv(
    "API_HASH"
)

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

SOURCE_GROUPS = os.getenv(
    "SOURCE_GROUPS",
    ""
)

# =====================================================
# GRUPOS
# =====================================================

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
# CACHE LINKS
# =====================================================

links_enviados = set()

# =====================================================
# EXTRAIR LINKS
# =====================================================

def extrair_links(texto):

    regex = r"(https?://[^\s]+)"

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

            r"/dp/([A-Z0-9]{10})",

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
            "ERRO AMAZON:",
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

    existe = os.path.exists(
        "session.session"
    )

    print(
        f"SESSION EXISTE: "
        f"{existe}"
    )

    # =================================================
    # SESSION
    # =================================================

    SESSION_FILE = os.path.join(
        os.getcwd(),
        "session"
    )

    print(
        f"SESSION FILE: "
        f"{SESSION_FILE}"
    )

    # =================================================
    # CLIENT
    # =================================================

    client = TelegramClient(
        SESSION_FILE,
        API_ID,
        API_HASH
    )

    # =================================================
    # CONNECT
    # =================================================

    conectado = False

    for tentativa in range(5):

        try:

            print(
                f"TENTANDO CONECTAR: "
                f"{tentativa + 1}"
            )

            await asyncio.wait_for(

                client.connect(),

                timeout=20

            )

            print(
                "CLIENT CONNECTADO"
            )

            conectado = True

            break

        except Exception as e:

            print(
                f"ERRO CONEXAO: "
                f"{e}"
            )

            await asyncio.sleep(5)

    if not conectado:

        print(
            "NAO FOI POSSIVEL CONECTAR"
        )

        return

    # =================================================
    # AUTH
    # =================================================

    try:

        autorizado = await client.is_user_authorized()

        print(
            f"AUTH: "
            f"{autorizado}"
        )

        if not autorizado:

            print(
                "SESSION INVALIDA"
            )

            return

    except Exception as e:

        print(
            "ERRO AUTH:",
            e
        )

        return

    print(
        "TELETHON ONLINE"
    )

    # =================================================
    # EVENTO NOVA MSG
    # =================================================

    @client.on(events.NewMessage)

    async def nova_mensagem(event):

        try:

            if event.chat_id not in GRUPOS:

                return

            print(
                f"NOVA MSG: "
                f"{event.chat_id}"
            )

            texto = event.raw_text

            if not texto:

                return

            links = extrair_links(
                texto
            )

            print(
                f"LINKS: "
                f"{len(links)}"
            )

            for link in links:

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

                if "amazon" in link.lower():

                    link = adicionar_tag_amazon(
                        link
                    )

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
    # LOOP
    # =================================================

    print(
        "MONITORANDO GRUPOS..."
    )

    await client.run_until_disconnected()
