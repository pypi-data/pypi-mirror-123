import json


class Produto:
    def __init__(self, sku: str, preco: float, qtd: int) -> None:
        self.sku = sku
        self.price = float(preco) if preco is not None else 0
        self.qty = float(qtd) if qtd is not None else 0

    def toJson(self) -> str:
        productJSON = {"product": {"price": self.price, "qty": self.qty}}
        return json.dumps(productJSON)

    def toXML(self) -> str:
        XML = f"""
                <produto>
                    <codigo>{self.sku}</codigo>
                    <vlr_unit>{self.price}</vlr_unit>
                    <estoque>{self.qty}</estoque>
                </produto>
                """
        return XML

    def __str__(self) -> str:
        return f"Sku: {self.sku} preço: {self.price} quantidade: {self.qty}"
