import csv
import sys

import requests

from config import settings
from skyhub.utils.telegram_erros import send_message

from .controllers import BlingController, SkyhubController
from .loggin_config import *
from .models.produto import Produto


def main():
    headers_skyhub = {
        "X-User-Email": settings.user_email,
        "X-Api-Key": settings.api_key,
        "x-accountmanager-key": settings.erp,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    with open(settings.file_path, "r", encoding="utf-8") as f:
        csv_file = csv.reader(f, delimiter=";")

        for index, row in enumerate(csv_file):
            if index == 0:
                continue

            produto_estoque = Produto(row[0], row[1].replace(",", "."), row[2].replace(",", "."))

            skyhub_controller = SkyhubController(
                credentials=headers_skyhub,
                base_url=settings.url_skyhub,
                request=requests,
            )

            bling_controller = BlingController(
                credentials={"apikey": settings.bling_key},
                base_url=settings.url_bling,
                request=requests,
            )

            produto_skyhub = skyhub_controller.get_produto(str(row[0]))
            produto_bling = bling_controller.get_produto(str(row[0]))

            if produto_skyhub:
                print(produto_skyhub)
                if produto_skyhub.price != row[1] or produto_skyhub.qty != row[2]:
                    skyhub_controller.atualiza_produto(produto_estoque)

            if produto_bling:
                print(produto_bling)
                if produto_bling.price != row[1] or produto_bling.qty != row[2]:
                    bling_controller.atualiza_produto(produto_estoque)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
        send_message(e)
