import logging
from pprint import pprint

import requests

from skyhub.loggin_config import *
from skyhub.models.produto import Produto

logger = logging.getLogger(__name__)
logger.addHandler(f_handler)


class BlingController:
    def __init__(self, credentials: dict, base_url: str, request: requests) -> None:
        self.credentials = credentials
        self.base_url = base_url
        self.request = request

    def get_produto(self, sku: str) -> Produto:
        url = f"{self.base_url}/{sku}/json?estoque=S"
        response = self.request.get(url, params=self.credentials)
        retorno = response.json().get("retorno")

        if "erros" in retorno:
            logger.warning(f"O produto {sku} não foi encontrado!")
            return False

        if response.status_code == 200:
            produtos = retorno.get("produtos")
            produtoJson = produtos[0].get("produto")

            codigo = produtoJson.get("codigo")
            preco = produtoJson.get("preco")
            estoque_atual = produtoJson.get("estoqueAtual")

            return Produto(codigo, preco, estoque_atual)

    def atualiza_produto(self, produto: Produto) -> bool:
        XML = f"""
<produto>
    <codigo>{produto.sku}</codigo>
    <vlr_unit>{produto.price}</vlr_unit>
    <estoque>{produto.qty}</estoque>
</produto>
        """
        apikey = self.credentials.get("apikey", "")

        url = f"{self.base_url}/{produto.sku}/json?estoque=S"
        data = {"apikey": apikey, "xml": XML}
        response = self.request.post(url, data=data)

        if response.status_code == 201:
            logger.info(f"O produto '{produto.sku}' foi atualizado.")
            return True

        else:
            print(response.status_code)
            logger.warning(f"O produto '{produto.sku}' não pode ser atualizado.")
            return False
