import os
import re
import requests

from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

print("====================================")
print("INICIANDO BOT")
print("====================================")

print("API_ID:", os.getenv("API_ID"))
print("API_HASH:", bool(os.getenv("API_HASH")))
print("BOT_TOKEN:", bool(os.getenv("TELEGRAM_BOT_TOKEN")))
print("CHAT_ID:", os.getenv("TELEGRAM_CHAT_ID"))
print("SOURCE_GROUPS:", os.getenv("SOURCE_GROUPS"))

print("ARQUIVOS DO DIRETORIO:")
print(os.listdir("."))

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

print(f"GRUPOS MONITORADOS: {GRUPOS}")

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

        print("TELEGRAM STATUS:", r.status_code)

    except Exception as e:
        print("ERRO TELEGRAM:", e)


async def main():

    print("====================================")
    print("INICIANDO TELETHON")
    print("====================================")

    SESSION_FILE = "session"

    print(
        "SESSION EXISTE:",
        os.path.exists("session.session")
    )

    print(
        "SESSION FILE:",
        os.path.abspath("session.session")
    )

    client = TelegramClient(
        SESSION_FILE,
        API_ID,
        API_HASH
    )

    await client.connect()

    print("CLIENT CONNECTADO")

    autorizado = await client.is_user_authorized()

    print("AUTH:", autorizado)

    if not autorizado:
        print("SESSION INVALIDA")
        return

    print("TELETHON ONLINE")

    @client.on(events.NewMessage(chats=GRUPOS))
    async def handler(event):

        try:

            texto = event.raw_text or ""

            links = extrair_links(texto)

            if links:
                print("LINKS ENCONTRADOS:", links)

            for link in links:

                if link in links_enviados:
                    continue

                if not any(
                    x in link.lower()
                    for x in [
                        "amazon",
                        "mercadolivre",
                        "meli",
                        "shopee",
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

                print("PROMOÇÃO ENVIADA")

        except Exception as e:
            print("ERRO HANDLER:", e)

    print("====================================")
    print("MONITORANDO GRUPOS...")
    print("====================================")

    await client.run_until_disconnected()
