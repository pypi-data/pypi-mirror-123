from setuptools import setup, find_packages

setup(name="mess_client_october17.10.2021",
      version="0.0.2",
      description="mess_client_projoctober",
      author="Andrey Yanke",
      author_email="ayanke@bk.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
