import os
import re
import asyncio
import requests

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("BOT INICIANDO")
print("=" * 50)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

STRING_SESSION = os.getenv("TELEGRAM_STRING_SESSION")

SOURCE_GROUPS = os.getenv("SOURCE_GROUPS", "")

GRUPOS = [
    int(x.strip())
    for x in SOURCE_GROUPS.split(",")
    if x.strip()
]

print("API_ID:", API_ID)
print("API_HASH:", bool(API_HASH))
print("BOT_TOKEN:", bool(BOT_TOKEN))
print("CHAT_ID:", CHAT_ID)
print("STRING_SESSION:", bool(STRING_SESSION))
print("GRUPOS:", GRUPOS)

links_enviados = set()


def extrair_links(texto):
    return re.findall(r"https?://[^\s]+", texto)


def enviar_telegram(texto):

    try:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        resposta = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": texto,
                "disable_web_page_preview": False
            },
            timeout=20
        )

        print("STATUS TELEGRAM:", resposta.status_code)

    except Exception as e:

        print("ERRO TELEGRAM:")
        print(type(e).__name__)
        print(str(e))


async def main():

    print("=" * 50)
    print("INICIANDO TELETHON")
    print("=" * 50)

    try:

        print("CRIANDO CLIENT")

        client = TelegramClient(
            StringSession(STRING_SESSION),
            API_ID,
            API_HASH
        )

        print("CLIENT CRIADO")

    except Exception as e:

        print("=" * 50)
        print("ERRO CRIANDO CLIENT")
        print(type(e).__name__)
        print(str(e))
        print("=" * 50)

        return

    try:

        print("ANTES CONNECT")

        await asyncio.wait_for(
            client.connect(),
            timeout=30
        )

        print("DEPOIS CONNECT")

    except Exception as e:

        print("=" * 50)
        print("ERRO CONNECT")
        print(type(e).__name__)
        print(str(e))
        print("=" * 50)

        return

    try:

        print("VERIFICANDO AUTH")

        autorizado = await client.is_user_authorized()

        print("AUTH:", autorizado)

    except Exception as e:

        print("=" * 50)
        print("ERRO AUTH")
        print(type(e).__name__)
        print(str(e))
        print("=" * 50)

        return

    if not autorizado:

        print("=" * 50)
        print("SESSAO INVALIDA")
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
                print("LINKS ENCONTRADOS:", links)

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

                print("PROMOÇÃO ENVIADA:", link)

        except Exception as e:

            print("ERRO HANDLER")
            print(type(e).__name__)
            print(str(e))

    await client.run_until_disconnected()
