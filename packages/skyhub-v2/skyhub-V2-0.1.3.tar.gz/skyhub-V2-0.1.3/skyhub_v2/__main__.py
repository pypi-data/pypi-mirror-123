import asyncio
import csv
import sys

from aiohttp.client import ClientSession

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

        skyhub_controller = SkyhubController(
            credentials=headers_skyhub,
            base_url=settings.settings.skyhub.url,
            request=session,
        )

        with open(settings.file_path, "r", encoding="utf-8") as f:
            csv_file = csv.reader(f, delimiter=";")

            for index, row in enumerate(csv_file):
                if index == 0 or row[1] == "" or row[2] == "":
                    continue

                produto_estoque = Produto(
                    row[0], row[1].replace(",", "."), row[2].replace(",", ".")
                )

                produto_skyhub = await skyhub_controller.get_produto(str(row[0]))

                if produto_skyhub:
                    print(f"{index:<6} {produto_skyhub}")
                    if produto_skyhub.price != row[1] or produto_skyhub.qty != row[2]:
                        await skyhub_controller.atualiza_produto(produto_estoque)


if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())

    except KeyboardInterrupt:
        pass

    except Exception as e:
        send_message(f"Skyhub: {e}")

