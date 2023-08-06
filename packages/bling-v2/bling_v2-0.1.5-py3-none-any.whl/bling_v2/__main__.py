import asyncio
import csv
import sys

from aiohttp.client import ClientSession

from bling_v2.utils.telegram import send_message
from config import settings

from .controllers import BlingController
from .logging_config import *
from .models.produto import Produto


async def main():
    async with ClientSession() as session:
        bling_controller = BlingController(
            credentials={"apikey": settings.secrets.bling.key},
            base_url=settings.settings.bling.url,
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

                produto_bling = await bling_controller.get_produto(str(row[0]))

                if produto_bling:
                    print(f"{index:<6} {produto_bling}")
                    if produto_bling.price != row[1] or produto_bling.qty != row[2]:
                        await bling_controller.atualiza_produto(produto_estoque)


if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())

    except KeyboardInterrupt:
        pass

    except Exception as e:
        send_message(f"Bling: {e}")
