from flask import Flask
import threading
import asyncio
import os
import time

# =====================================================
# APP
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
# LOOP TESTE
# =====================================================

async def teste_loop():

    while True:

        print(
            "BOT LOOP ATIVO"
        )

        await asyncio.sleep(30)

# =====================================================
# THREAD
# =====================================================

def iniciar_bot():

    print(
        "INICIANDO THREAD BOT"
    )

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(
        teste_loop()
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
        f"PORTA {port}"
    )

    app.run(

        host="0.0.0.0",

        port=port

    )
