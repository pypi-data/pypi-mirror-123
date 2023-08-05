from setuptools import setup

name = "types-certifi"
description = "Typing stubs for certifi"
long_description = '''
## Typing stubs for certifi

This is a PEP 561 type stub package for the `certifi` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `certifi`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/certifi. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `9f869723509ac027bae6b6f567b921d6a229e8ec`.
'''.lstrip()

setup(name=name,
      version="2021.10.8.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['certifi-stubs'],
      package_data={'certifi-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
