# Copyright 2021 Techbros GmbH. All Rights Reserved.
# 
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by:
# - Your Name <your email>
# =========================================================================

from selenium import webdriver


def _get_chrome_option():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
        )
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options


def _get_driver():
    driver = webdriver.Chrome('chromedriver', options=_get_chrome_option())

