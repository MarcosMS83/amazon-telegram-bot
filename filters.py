def produto_valido(produto):

    try:

        preco = float(
            produto["preco"]
        )

        # evita produtos muito baratos
        if preco < 20:
            return False

        return True

    except:

        return False
