import logging

from aiohttp import ClientSession

from skyhub.loggin_config import *
from skyhub.models.produto import Produto

logger = logging.getLogger(__name__)
logger.addHandler(f_handler)


class BlingController:
    def __init__(
        self, credentials: dict, base_url: str, request: ClientSession
    ) -> None:
        self.credentials = credentials
        self.base_url = base_url
        self.request = request

    async def get_produto(self, sku: str) -> Produto:
        url = f"{self.base_url}/{sku}/json?estoque=S"
        response = await self.request.request(
            method="GET", url=url, params=self.credentials
        )
        response_json = await response.json()
        retorno = response_json.get("retorno")

        if "erros" in retorno:
            logger.warning(f"O produto {sku} não foi encontrado!")
            return False

        if response.status == 200:
            produtos = retorno.get("produtos")
            produtoJson = produtos[0].get("produto")

            codigo = produtoJson.get("codigo")
            preco = produtoJson.get("preco")
            estoque_atual = produtoJson.get("estoqueAtual")

            return Produto(codigo, preco, estoque_atual)

    async def atualiza_produto(self, produto: Produto) -> bool:
        xml = produto.toXML()
        apikey = self.credentials.get("apikey", "")
        data = {"apikey": apikey, "xml": xml}

        url = f"{self.base_url}/{produto.sku}/json?estoque=S"
        response = await self.request.request(method="POST", url=url, data=data)
        print(f"Bling {response.status:>10}", end="")

        if response.status == 201:
            logger.info(f"O produto '{produto.sku}' foi atualizado.")
            return True

        else:
            logger.warning(f"O produto '{produto.sku}' não pode ser atualizado.")
            return False
