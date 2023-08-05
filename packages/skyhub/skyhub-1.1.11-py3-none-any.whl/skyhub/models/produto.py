import json


class Produto:
    def __init__(self, sku: str, preco: float, qtd: int) -> None:
        self.sku = sku
        self.price = float(preco)
        self.qty = int(qtd)

    def toJson(self) -> str:
        productJSON = {"product": {"price": self.price, "qty": self.qty}}
        return json.dumps(productJSON)

    def __str__(self) -> str:
        return f"Sku: {self.sku} preço: {self.price} quantidade: {self.qty}"
