import asyncio
import csv
import sys

from aiohttp.client import ClientSession

from config import settings
from skyhub.utils.telegram_erros import send_message

from .controllers import BlingController, SkyhubController
from .loggin_config import *
from .models.produto import Produto


async def main():
    async with ClientSession() as session:
        headers_skyhub = {
            "X-User-Email": settings.user_email,
            "X-Api-Key": settings.api_key,
            "x-accountmanager-key": settings.erp,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        skyhub_controller = SkyhubController(
            credentials=headers_skyhub,
            base_url=settings.url_skyhub,
            request=session,
        )

        bling_controller = BlingController(
            credentials={"apikey": settings.bling_key},
            base_url=settings.url_bling,
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
                produto_bling = await bling_controller.get_produto(str(row[0]))

                if produto_skyhub:
                    print(f"{index:<6} {produto_skyhub}")
                    if produto_skyhub.price != row[1] or produto_skyhub.qty != row[2]:
                        await skyhub_controller.atualiza_produto(produto_estoque)

                if produto_bling:
                    print(f"{index:<6} {produto_bling}")
                    if produto_bling.price != row[1] or produto_bling.qty != row[2]:
                        await bling_controller.atualiza_produto(produto_estoque)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        # teste()

    except KeyboardInterrupt:
        sys.exit()

    # except Exception as e:
    #     send_message(e)
