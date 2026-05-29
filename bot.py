import os
import re
import requests

from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("VERSAO BOT 29-05-2026")
print("=" * 50)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SOURCE_GROUPS = os.getenv("SOURCE_GROUPS", "")

GRUPOS = [
    int(x.strip())
    for x in SOURCE_GROUPS.split(",")
    if x.strip()
]

SESSION_FILE = "/opt/render/project/src/session.session"

print("API_ID:", API_ID)
print("GRUPOS:", GRUPOS)

print("ARQUIVOS:")
print(os.listdir("."))

print("SESSION EXISTE:", os.path.exists(SESSION_FILE))

if os.path.exists(SESSION_FILE):
    print("SESSION SIZE:", os.path.getsize(SESSION_FILE))

links_enviados = set()


def extrair_links(texto):
    return re.findall(r"https?://[^\s]+", texto)


def enviar_telegram(texto):
    try:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        r = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": texto,
                "disable_web_page_preview": False,
            },
            timeout=20,
        )

        print("SEND STATUS:", r.status_code)

    except Exception as e:
        print("ERRO TELEGRAM:", e)


async def main():

    print("=" * 50)
    print("INICIANDO TELETHON")
    print("=" * 50)

    try:

        print("PASSO 1")

        client = TelegramClient(
            SESSION_FILE,
            API_ID,
            API_HASH
        )

        print("PASSO 2 - CLIENT CRIADO")

        await client.connect()

        print("PASSO 3 - CLIENT CONNECTADO")

        autorizado = await client.is_user_authorized()

        print("PASSO 4 - AUTH:", autorizado)

        if not autorizado:
            print("SESSION INVALIDA")
            return

    except Exception as e:

        print("=" * 50)
        print("ERRO TELETHON")
        print(type(e).__name__)
        print(str(e))
        print("=" * 50)

        return

    print("=" * 50)
    print("MONITORANDO GRUPOS")
    print("=" * 50)

    @client.on(events.NewMessage(chats=GRUPOS))
    async def handler(event):

        try:

            texto = event.raw_text or ""

            links = extrair_links(texto)

            if links:
                print("LINKS:", links)

            for link in links:

                if link in links_enviados:
                    continue

                if not any(
                    palavra in link.lower()
                    for palavra in [
                        "amazon",
                        "mercadolivre",
                        "meli",
                        "shopee"
                    ]
                ):
                    continue

                links_enviados.add(link)

                mensagem = (
                    "🔥 PROMOÇÃO ENCONTRADA\n\n"
                    f"Grupo: {event.chat_id}\n\n"
                    f"{link}"
                )

                enviar_telegram(mensagem)

                print("ENVIADO:", link)

        except Exception as e:

            print("ERRO HANDLER:")
            print(type(e).__name__)
            print(str(e))

    await client.run_until_disconnected()
