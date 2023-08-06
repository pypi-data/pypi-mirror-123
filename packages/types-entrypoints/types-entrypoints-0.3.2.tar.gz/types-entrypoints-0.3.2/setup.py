from setuptools import setup

name = "types-entrypoints"
description = "Typing stubs for entrypoints"
long_description = '''
## Typing stubs for entrypoints

This is a PEP 561 type stub package for the `entrypoints` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `entrypoints`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/entrypoints. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `f30b5ae363937553bd7183119fba8377ad78de8d`.
'''.lstrip()

setup(name=name,
      version="0.3.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['entrypoints-stubs'],
      package_data={'entrypoints-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
