import json


class Produto:
    def __init__(self, sku: str, preco: float, qtd: int) -> None:
        self.sku = sku
        self.price = float(preco) if preco != "" else 0.0
        self.qty = int(qtd) if qtd != "" else 0

    def toJson(self) -> str:
        productJSON = {"product": {"price": self.price, "qty": self.qty}}
        return json.dumps(productJSON)

    def __str__(self) -> str:
        return f"Sku: {self.sku} preço: {self.price} quantidade: {self.qty}"
