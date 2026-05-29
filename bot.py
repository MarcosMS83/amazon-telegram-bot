import os
import re
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
print("STRING_SESSION:", STRING_SESSION is not None)
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
        print("ERRO TELEGRAM:", e)


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

        await client.connect()

        print("CLIENT CONECTADO")

        autorizado = await client.is_user_authorized()

        print("AUTH:", autorizado)

        if not autorizado:
            print("SESSAO INVALIDA")
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

            print("ERRO HANDLER:")
            print(type(e).__name__)
            print(str(e))

    await client.run_until_disconnected()
