import feedparser
import requests
import re

from bs4 import BeautifulSoup

# =====================================================
# TAG AFILIADA
# =====================================================

TAG = "promodudia-20"

# =====================================================
# RSS PROMOBIT
# =====================================================

RSS_URL = (
    "https://www.promobit.com.br/feed/"
)

# =====================================================
# BUSCAR PROMOÇÕES
# =====================================================

def buscar_promocoes_amazon():

    produtos = []

    feed = feedparser.parse(
        RSS_URL
    )

    print(
        f"PROMOÇÕES RSS: {len(feed.entries)}"
    )

    for entry in feed.entries[:20]:

        try:

            titulo = entry.title

            link_post = entry.link

            # =========================================
            # ABRE POST
            # =========================================

            response = requests.get(

                link_post,

                timeout=20,

                headers={
                    "User-Agent":
                    "Mozilla/5.0"
                }

            )

            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )

            # =========================================
            # PROCURA AMAZON
            # =========================================

            links = soup.find_all(
                "a",
                href=True
            )

            amazon_link = None

            for a in links:

                href = a["href"]

                if (
                    "amazon.com.br" in href
                    or "amzn.to" in href
                ):

                    amazon_link = href
                    break

            if not amazon_link:
                continue

            # =========================================
            # EXTRAI ASIN
            # =========================================

            asin_match = re.search(

                r'/dp/([A-Z0-9]{10})',

                amazon_link

            )

            if asin_match:

                asin = asin_match.group(1)

                amazon_link = (
                    f"https://www.amazon.com.br/dp/{asin}"
                    f"?tag={TAG}"
                )

            # =========================================
            # IMAGEM
            # =========================================

            imagem = None

            img = soup.find("img")

            if img:

                imagem = img.get("src")

            # =========================================
            # PREÇO
            # =========================================

            preco = "0"

            preco_match = re.search(

                r'R\\$\\s?[\\d\\.,]+',

                soup.get_text()

            )

            if preco_match:

                preco = (
                    preco_match.group(0)
                    .replace("R$", "")
                    .strip()
                )

            produtos.append({

                "titulo": titulo,

                "preco": preco,

                "imagem": imagem,

                "link": amazon_link,

                "origem": "Promobit"

            })

            print(
                "PROMOÇÃO:",
                titulo
            )

        except Exception as e:

            print(
                "ERRO PROMO:",
                e
            )

    print(
        f"TOTAL AMAZON: {len(produtos)}"
    )

    return produtos
