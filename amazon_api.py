import requests
from bs4 import BeautifulSoup

# =====================================================
# TAG AFILIADA
# =====================================================

TAG = "promodudia-20"

# =====================================================
# BUSCAR PROMOÇÕES AMAZON
# =====================================================

def buscar_promocoes_amazon():

    produtos = []

    headers = {

        "User-Agent":
        "Mozilla/5.0"

    }

    urls = [

        "https://www.amazon.com.br/deals",

        "https://www.amazon.com.br/gp/goldbox"

    ]

    for url in urls:

        try:

            response = requests.get(

                url,

                headers=headers,

                timeout=20

            )

            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )

            produtos_html = soup.select(
                "div[data-asin]"
            )

            for item in produtos_html[:10]:

                try:

                    asin = item.get(
                        "data-asin"
                    )

                    if not asin:
                        continue

                    titulo_tag = item.select_one(
                        "span"
                    )

                    titulo = (
                        titulo_tag.text.strip()
                        if titulo_tag
                        else "Produto Amazon"
                    )

                    imagem_tag = item.select_one(
                        "img"
                    )

                    imagem = (
                        imagem_tag.get("src")
                        if imagem_tag
                        else None
                    )

                    preco = "0"

                    texto = item.get_text()

                    import re

                    preco_match = re.search(

                        r'R\\$\\s?[\\d\\.,]+',

                        texto

                    )

                    if preco_match:

                        preco = (
                            preco_match.group(0)
                            .replace("R$", "")
                            .strip()
                        )

                    link = (
                        f"https://www.amazon.com.br/dp/{asin}"
                        f"?tag={TAG}"
                    )

                    produtos.append({

                        "titulo": titulo,

                        "preco": preco,

                        "imagem": imagem,

                        "link": link,

                        "origem": "Amazon"

                    })

                except:
                    pass

        except Exception as e:

            print(
                "ERRO AMAZON:",
                e
            )

    return produtos
