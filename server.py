from flask import Flask
import threading
import asyncio
import os

from bot import loop_bot

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

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

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
# FLASK
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
