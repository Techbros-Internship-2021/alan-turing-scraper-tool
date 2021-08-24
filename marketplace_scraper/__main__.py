# Copyright 2021 Techbros GmbH. All Rights Reserved.
# 
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by:
# - Okta Fajar Suryani <okta.suryani@techbros.io>
# - Daffa Barin <daffabarin@gmail.com>
# - Ridhwan Nashir <ridhwanashir@gmail.com>
# - Jonas de Deus Guterres <guterres19dedeus@gmail.com>
# =========================================================================

import typer
import platform
import json

import pandas as pd
import marketplace_scraper as mks

from marketplace_scraper import __version__
from marketplace_scraper import Scrapper


app = typer.Typer()


@app.command()
def scrapper(output: str, query_data: str):
    with open(query_data, "r") as read_file:
        query = json.load(read_file)

    scr = Scrapper()
    # blibli_data = scr.crawl(mks.MARKETPLACE_BLIBLI, **query)
    # tokopedia_data = scr.crawl(mks.MARKETPLACE_TOKOPEDIA, **query)
    # shopee_data = scr.crawl(mks.MARKETPLACE_SHOPEE, **query)
    bukalapak_data = scr.crawl(mks.MARKETPLACE_BUKALAPAK, **query)

    # all_data = [blibli_data, tokopedia_data, shopee_data, bukalapak_data]
    all_data = bukalapak_data
    # all_data = pd.concat(all_data)
    all_data.to_csv(output, index=False)
    print("File is saved in: {}".format(output))

@app.command()
def version():
    typer.echo("Turing Marketplace Scraper Info: Version: {}, Python: {}, Platform: {}".format(__version__,
                                                                                     platform.python_version(),
                                                                                     platform.system()
                                                                                     ))

if __name__ == '__main__':
    app()
