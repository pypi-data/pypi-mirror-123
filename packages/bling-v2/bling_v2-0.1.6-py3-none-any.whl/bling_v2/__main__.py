import asyncio
import sys
from typing import Literal, Union, Dict

import pandas as pd
from aiohttp.client import ClientSession
from pandas.core.frame import DataFrame

from bling_v2.utils.telegram import send_message
from config import settings

from .controllers import BlingController
from .logging_config import *
from .models.produto import Produto


async def main() -> None:
    async with ClientSession() as session:
        bling: BlingController = BlingController(
            credentials={"apikey": settings.secrets.bling.key},
            base_url=settings.settings.bling.url,
            request=session,
        )

        df: Dict[str, DataFrame] = pd.read_excel(settings.file_path)

        for index, row in enumerate(df.values):
            produto_estoque: Produto = Produto(row[0], row[1], row[2])

            if index == 0 or produto_estoque.price == "" or produto_estoque.qty == "":
                continue

            produto_bling: Union[Produto, Literal[False]] = await bling.get_produto(
                produto_estoque.sku
            )

            if produto_bling:
                print(f"{index:<6} {produto_bling}")
                if (
                    produto_bling.price != produto_estoque.price
                    or produto_bling.qty != produto_estoque.qty
                ):
                    await bling.atualiza_produto(produto_estoque)
                    pass


if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())

    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
        send_message(f"Bling: {e}")
