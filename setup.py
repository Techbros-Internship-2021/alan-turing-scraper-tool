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

from setuptools import setup
from setuptools import find_packages

import os.path

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(name='marketplace-scraper',
      version='0.0.1',
      description='Scraper tool for some popular indonesian marketplaces',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Okta, Daffa, Ridwan, Jonas',
      author_email='okta.suryani@techbros.io, daffabarin@gmail.com, ridhwanashir@gmail.com, guterres19dedeus@gmail.com',
      url='https://github.com/Techbros-Internship-2021/alan-turing-scraper-tool',
      license='Proprietary',
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Intended Audience :: Education",
          "Intended Audience :: Information Technology",
          "Intended Audience :: Science/Research",
          "License :: Other/Proprietary License",
          "Topic :: Scientific/Engineering",
          "Topic :: Software Development",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
      ],
      include_package_data=True,
      install_requires=['numpy',
                        'pandas',
                        'tqdm',
                        'selenium',
                        'bs4',
                        'typer'],
      packages=find_packages(),
      entry_points={"console_scripts": ["marketplace_scraper=marketplace_scraper.__main__:app"]},
      )
