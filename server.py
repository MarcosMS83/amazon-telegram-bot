import os
import asyncio
import threading

from flask import Flask

from bot import main

app = Flask(__name__)

@app.route("/")
def home():
    return "BOT ONLINE"


def iniciar_bot():

    print("INICIANDO BOT...")

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    print("LOOP BOT INICIADO")

    try:

        loop.run_until_complete(
            main()
        )

    except Exception as e:

        print("ERRO BOT:")
        print(type(e).__name__)
        print(str(e))


if __name__ == "__main__":

    print("THREAD CRIADA")

    bot_thread = threading.Thread(
        target=iniciar_bot,
        daemon=True
    )

    bot_thread.start()

    PORT = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    print(f"PORTA: {PORT}")

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        use_reloader=False
    )
