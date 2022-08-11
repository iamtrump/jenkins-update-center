from setuptools import setup

setup(name="jenkuc",
  version="0.1.1",
  description="Simple Jenkins update center implementation",
  url="https://github.com/iamtrump/jenkins-update-center",
  author="Mikhail Mironov",
  author_email="mikhailmironov@mikhailmironov.ru",
  license="MIT",
  packages=["jenkuc"],
  install_requires=["pycryptodome"],
  zip_safe=False)
