import logging
from typing import Literal, Union

from aiohttp import ClientSession

from bling_v2.logging_config import *
from bling_v2.models import Produto

logger = logging.getLogger(__name__)
logger.addHandler(f_handler)


class BlingController:
    def __init__(
        self, credentials: dict, base_url: str, request: ClientSession
    ) -> None:
        self.credentials = credentials
        self.base_url = base_url
        self.request = request

    async def get_produto(self, sku: str) -> Union[Produto, Literal[False]]:
        apikey = self.credentials.get("apikey", "")
        url = f"{self.base_url}/{sku}/json?apikey={apikey}&estoque=S"
        response = await self.request.request(method="GET", url=url)
        response_json = await response.json()
        retorno = response_json.get("retorno")
        status = response.status

        if "erros" in retorno:
            logger.warning(f"O produto {sku} não foi encontrado!")
            return False

        if status == 200:
            produtos = retorno.get("produtos")
            produtoJson = produtos[0].get("produto")

            codigo = produtoJson.get("codigo")
            preco = produtoJson.get("preco")
            estoque_atual = produtoJson.get("estoqueAtual")
            produto = Produto(codigo, preco or 0, estoque_atual or 0)

            return produto
        return False

    async def atualiza_produto(self, produto: Produto) -> bool:
        xml = produto.toXML()
        apikey = self.credentials.get("apikey", "")
        data = {"apikey": apikey, "xml": xml}

        url = f"{self.base_url}/{produto.sku}/json?estoque=S"
        response = await self.request.request(method="POST", url=url, data=data)
        status = response.status

        print(f"Bling {response.status:>4}", end=" ")

        if status == 200:
            logger.info(f"O produto '{produto.sku}' foi atualizado.")
            return True

        elif status == 429:
            response = await self.atualiza_produto(produto)

        else:
            logger.warning(f"O produto '{produto.sku}' não pode ser atualizado.")
            return False
        return False
