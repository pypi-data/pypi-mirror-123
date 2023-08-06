import json


class Produto:
    def __init__(
        self, sku: str, preco: float, promotional_price: float, qtd: int
    ) -> None:
        self.sku = sku
        self.price = float(preco) if preco is not None else 0
        self.promotional_price = (
            float(promotional_price) if promotional_price is not None else 0
        )
        self.qty = float(qtd) if qtd is not None else 0

    def toJson(self) -> str:
        productJSON = {
            "product": {
                "price": self.price,
                "qty": self.qty,
                "promotional_price": self.promotional_price,
            }
        }
        return json.dumps(productJSON)

    def __str__(self) -> str:
        return f"Sku: {self.sku} preço: {self.price} quantidade: {self.qty}"
