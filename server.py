from flask import Flask
import threading
import os

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

    bot.start_bot()

# =====================================================

threading.Thread(
    target=run_bot,
    daemon=True
).start()

# =====================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(

        host="0.0.0.0",

        port=port

    )
