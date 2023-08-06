import logging
import time

from aiohttp import ClientSession

from skyhub_v2.logging_config import *
from skyhub_v2.models import Produto

logger = logging.getLogger(__name__)
logger.addHandler(f_handler)


class SkyhubController:
    def __init__(
        self, credentials: dict, base_url: str, request: ClientSession
    ) -> None:
        self.credentials = credentials
        self.base_url = base_url
        self.request = request

    async def get_produto(self, sku: str) -> Produto:
        url = f"{self.base_url}/{sku}"
        response = await self.request.request(
            method="GET", url=url, headers=self.credentials
        )
        produto = await response.json()

        if response.status == 200:
            qty = produto.get("qty", 0)
            price = produto.get("price", 0)
            return Produto(sku, price, qty)

        elif response.status == 429:
            time.sleep(1)
            await self.get_produto(sku)

        elif response.status == 404:
            logger.warning(f"O produto {sku} não foi encontrado!")
            return False

        return False

    async def atualiza_produto(self, produto: Produto) -> bool:
        produtoJSON = produto.toJson()
        url = f"{self.base_url}/{produto.sku}"

        response = await self.request.request(
            method="PUT", url=url, data=produtoJSON, headers=self.credentials
        )
        print(f"SkyHub {response.status}", end=" ")

        if response.status == 204:
            logger.info(f"O produto '{produto.sku}' foi atualizado.")
            return True

        if response.status == 429:
            response = await self.request.request(
                method="PUT", url=url, data=produtoJSON, headers=self.credentials
            )

        else:
            logger.warning(f"O produto '{produto.sku}' não pode ser atualizado.")
            return False
