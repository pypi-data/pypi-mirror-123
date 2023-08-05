from setuptools import setup

name = "types-singledispatch"
description = "Typing stubs for singledispatch"
long_description = '''
## Typing stubs for singledispatch

This is a PEP 561 type stub package for the `singledispatch` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `singledispatch`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/singledispatch. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `9f869723509ac027bae6b6f567b921d6a229e8ec`.
'''.lstrip()

setup(name=name,
      version="3.7.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['singledispatch-stubs'],
      package_data={'singledispatch-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
