from setuptools import setup
from setuptools import find_packages

import os.path

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(name='your project name',
      version='0.0.1',
      description='your project description',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Techbros GmbH',
      author_email='youremail',
      url='your project repo url',
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
