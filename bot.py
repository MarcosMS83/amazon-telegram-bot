import asyncio

# =====================================================
# LOOP BOT
# =====================================================

async def loop_bot():

    print(
        "LOOP BOT INICIADO"
    )

    while True:

        print(
            "BOT RODANDO..."
        )

        await asyncio.sleep(30)
