import os
import asyncio
import threading

from flask import Flask

from bot import main

# =====================================================
# FLASK
# =====================================================

app = Flask(__name__)

@app.route("/")

def home():

    return "BOT ONLINE"

# =====================================================
# BOT THREAD
# =====================================================

def iniciar_bot():

    print(
        "INICIANDO BOT..."
    )

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(
        loop
    )

    try:

        print(
            "LOOP BOT INICIADO"
        )

        loop.run_until_complete(
            main()
        )

    except Exception as e:

        print(
            f"ERRO BOT: "
            f"{e}"
        )

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print(
        "THREAD CRIADA"
    )

    bot_thread = threading.Thread(
        target=iniciar_bot
    )

    bot_thread.start()

    PORT = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    print(
        f"PORTA: "
        f"{PORT}"
    )

    app.run(

        host="0.0.0.0",

        port=PORT,

        debug=False,

        use_reloader=False

    )
