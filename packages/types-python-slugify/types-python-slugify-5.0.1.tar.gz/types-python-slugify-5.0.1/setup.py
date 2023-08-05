from setuptools import setup

name = "types-python-slugify"
description = "Typing stubs for python-slugify"
long_description = '''
## Typing stubs for python-slugify

This is a PEP 561 type stub package for the `python-slugify` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `python-slugify`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/python-slugify. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `9f869723509ac027bae6b6f567b921d6a229e8ec`.
'''.lstrip()

setup(name=name,
      version="5.0.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['slugify-stubs'],
      package_data={'slugify-stubs': ['__init__.pyi', 'slugify.pyi', 'special.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
