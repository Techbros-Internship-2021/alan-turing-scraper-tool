# Copyright 2021 Techbros GmbH. All Rights Reserved.
# 
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by:
# - Okta Fajar Suryani <okta.suryani@techbros.io>
# - Daffa Barin <daffabarin@gmail.com>
# - Ridhwan Nashir <ridhwanashir@gmail.com>
# - Jonas <guterres19dedeus@gmail.com>
# =========================================================================


from marketplace_scraper.scrapper.scrapper import Scrapper, Vendor


MARKETPLACE_BLIBLI = Vendor.BLIBLI
MARKETPLACE_TOKOPEDIA = Vendor.TOKOPEDIA
MARKETPLACE_SHOPEE = Vendor.SHOPEE
MARKETPLACE_BUKALAPAK = Vendor.BUKALAPAK


__all__ = ['Scrapper',
           'MARKETPLACE_BLIBLI',
           'MARKETPLACE_TOKOPEDIA',
           'MARKETPLACE_SHOPEE',
           'MARKETPLACE_BUKALAPAK']