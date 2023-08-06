import asyncio
import csv
from sys import platform
from typing import Dict

import pandas as pd
from aiohttp.client import ClientSession
from pandas.core.frame import DataFrame

from config import settings
from skyhub_v2.utils.telegram import send_message

from .controllers import SkyhubController
from .logging_config import *
from .models import Produto


async def main():
    async with ClientSession() as session:
        headers_skyhub = {
            "X-User-Email": settings.settings.skyhub.email,
            "X-Api-Key": settings.secrets.skyhub.key,
            "x-accountmanager-key": settings.secrets.skyhub.erp,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        skyhub: SkyhubController = SkyhubController(
            credentials=headers_skyhub,
            base_url=settings.settings.skyhub.url,
            request=session,
        )

        df: Dict[str, DataFrame] = pd.read_excel(settings.file_path)

        for index, row in enumerate(df.values):
            produto_estoque = Produto(
                row[0],
                row[1],
                row[3],
                row[2],
            )

            if (
                index == 0
                or produto_estoque.price == ""
                or produto_estoque.qty == ""
                or produto_estoque.promotional_price == ""
            ):
                continue

            produto_skyhub = await skyhub.get_produto(str(row[0]))

            if produto_skyhub:
                if (
                    produto_skyhub.price != produto_estoque.price
                    or produto_skyhub.qty != produto_estoque.qty
                ):
                    await skyhub.atualiza_produto(produto_estoque)
                    print(f"{index:<6} {produto_skyhub}")
                    pass


if __name__ == "__main__":
    try:
        if platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())

    except KeyboardInterrupt:
        pass

    except Exception as e:
        send_message(f"Skyhub: {e}")
