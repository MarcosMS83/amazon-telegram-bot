import random


def buscar_promocoes_amazon():

    produtos = []

    exemplos = [

        {
            "titulo": "Echo Dot 5ª Geração",
            "preco": "299.90",
            "imagem": "https://m.media-amazon.com/images/I/714Rq4k05UL._AC_SL1000_.jpg",
            "link": "https://www.amazon.com.br/dp/B09B8V1LZ3?tag=promodudia-20",
            "origem": "Amazon"
        },

        {
            "titulo": "Fire TV Stick",
            "preco": "239.90",
            "imagem": "https://m.media-amazon.com/images/I/51KKR5uGn6L._AC_SL1000_.jpg",
            "link": "https://www.amazon.com.br/dp/B08C1W5N87?tag=promodudia-20",
            "origem": "Amazon"
        },

        {
            "titulo": "Kindle 11ª Geração",
            "preco": "499.90",
            "imagem": "https://m.media-amazon.com/images/I/61L1ItFgFHL._AC_SL1000_.jpg",
            "link": "https://www.amazon.com.br/dp/B09SWW583J?tag=promodudia-20",
            "origem": "Amazon"
        }

    ]

    produtos.extend(
        exemplos
    )

    random.shuffle(
        produtos
    )

    return produtos
