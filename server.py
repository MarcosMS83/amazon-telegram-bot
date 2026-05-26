from flask import Flask
import threading
import os
import time

import bot

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

        "status": "online",

        "bot": "amazon telegram bot"

    }

# =====================================================
# START BOT
# =====================================================

def run_bot():

    print(
        "INICIANDO LOOP BOT..."
    )

    bot.start_bot()

# =====================================================
# THREAD
# =====================================================

thread_bot = threading.Thread(

    target=run_bot,

    daemon=True

)

thread_bot.start()

print(
    "THREAD BOT INICIADA"
)

# =====================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    print(
        f"FLASK PORTA {port}"
    )

    app.run(

        host="0.0.0.0",

        port=port

    )
