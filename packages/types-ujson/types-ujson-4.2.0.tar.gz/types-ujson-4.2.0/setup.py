from setuptools import setup

name = "types-ujson"
description = "Typing stubs for ujson"
long_description = '''
## Typing stubs for ujson

This is a PEP 561 type stub package for the `ujson` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `ujson`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/ujson. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `bb24e77404af84b0ff32020ad6c356c659bc6fe5`.
'''.lstrip()

setup(name=name,
      version="4.2.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['ujson-stubs'],
      package_data={'ujson-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
