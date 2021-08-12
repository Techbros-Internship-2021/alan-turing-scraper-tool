# Copyright 2021 Techbros GmbH. All Rights Reserved.
# 
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by:
# - Your Name <your email>
# =========================================================================

import typer
import platform

import pandas as pd
import marketplace_scraper as mks

from marketplace_scraper import __version__
from marketplace_scraper import Scrapper


app = typer.Typer()


@app.command()
def scrapper(output: str, product: str):
    query = {'product': product}

    scr = Scrapper()
    blibli_data = scr.crawl(mks.MARKETPLACE_BLIBLI, **query)
    tokopedia_data = scr.crawl(mks.MARKETPLACE_TOKOPEDIA, **query)
    shopee_data = scr.crawl(mks.MARKETPLACE_SHOPEE, **query)
    bukalapak_data = scr.crawl(mks.MARKETPLACE_BUKALAPAK, **query)

    all_data = [blibli_data, tokopedia_data, shopee_data, bukalapak_data]
    all_data = pd.concat(all_data)
    all_data.to_csv(output, index=False)
    print("File is saved in: {}".format(output))


@app.command()
def version():
    typer.echo("SIPLah Analytics Info: Version: {}, Python: {}, Platform: {}".format(__version__,
                                                                                     platform.python_version,
                                                                                     platform.system()
                                                                                     ))


if __name__ == '__main__':
    app()
