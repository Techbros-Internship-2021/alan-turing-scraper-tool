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


from marketplace_scraper.scrapper.handler import _shopee_handler, _blibli_handler, _bukalapak_handler, _tokopedia_handler
from marketplace_scraper.scrapper.driver import _get_driver


class Vendor: BLIBLI, TOKOPEDIA, SHOPEE, BUKALAPAK = 0, 1, 2, 3


class Scrapper(object):
    def __init__(self):
        self._driver = _get_driver()

    def crawl(self, vendor, **query):
        if vendor == Vendor.BLIBLI:
            return _blibli_handler(self._driver, **query)
        elif vendor == Vendor.TOKOPEDIA:
            return _tokopedia_handler(self._driver, **query)
        elif vendor == Vendor.SHOPEE:
            return _shopee_handler(self._driver, **query)
        elif vendor == Vendor.BUKALAPAK:
            return _bukalapak_handler(self._driver, **query)
        else:
            TypeError("Unknown Vendor")
