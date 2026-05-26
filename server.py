from flask import Flask
import threading
import asyncio
import os

# =====================================================
# IMPORT BOT
# =====================================================

try:

    from bot import loop_bot

    print(
        "BOT IMPORTADO COM SUCESSO"
    )

except Exception as e:

    print(
        "ERRO IMPORT BOT:",
        e
    )

    loop_bot = None

# =====================================================
# FLASK
# =====================================================

app = Flask(__name__)

# =====================================================
# HOME
# =====================================================

@app.route("/")

def home():

    return {
        "status": "online"
    }

# =====================================================
# THREAD BOT
# =====================================================

def iniciar_bot():

    print(
        "INICIANDO BOT..."
    )

    if loop_bot is None:

        print(
            "BOT NÃO INICIADO"
        )

        return

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    try:

        loop.run_until_complete(
            loop_bot()
        )

    except Exception as e:

        print(
            "ERRO BOT:",
            e
        )

# =====================================================
# START THREAD
# =====================================================

threading.Thread(

    target=iniciar_bot,

    daemon=True

).start()

print(
    "THREAD CRIADA"
)

# =====================================================
# START FLASK
# =====================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    print(
        f"PORTA: {port}"
    )

    app.run(

        host="0.0.0.0",

        port=port

    )
