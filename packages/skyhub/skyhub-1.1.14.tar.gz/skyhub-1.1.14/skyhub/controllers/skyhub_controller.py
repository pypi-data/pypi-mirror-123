import logging

import requests

from skyhub.loggin_config import *
from skyhub.models.produto import Produto

logger = logging.getLogger(__name__)
logger.addHandler(f_handler)


class SkyhubController:
    def __init__(self, credentials: dict, base_url: str, request: requests) -> None:
        self.credentials = credentials
        self.base_url = base_url
        self.request = request

    def get_produto(self, sku: str) -> Produto:
        url = f"{self.base_url}/{sku}"
        response = self.request.get(url, headers=self.credentials)

        if response.status_code == 200:
            produto = response.json()
            qty = produto["qty"]  # Quantidade
            price = produto["price"]  # Preço
            return Produto(sku, price, qty)

        elif response.status_code == 404:
            logger.warning(f"O produto {sku} não foi encontrado!")
            return False

        return response

    def atualiza_produto(self, produto: Produto) -> bool:
        produtoJSON = produto.toJson()
        url = f"{self.base_url}/{produto.sku}"
        response = self.request.put(url, data=produtoJSON, headers=self.credentials)

        print(response.status_code)
        if response.status_code == 204:
            logger.info(f"O produto '{produto.sku}' foi atualizado.")
            return True

        else:
            print(response.text)
            logger.warning(f"O produto '{produto.sku}' não pode ser atualizado.")
            return False
