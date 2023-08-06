from setuptools import setup

name = "types-pysftp"
description = "Typing stubs for pysftp"
long_description = '''
## Typing stubs for pysftp

This is a PEP 561 type stub package for the `pysftp` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pysftp`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pysftp. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `994b69ef8f18e76689daca3947879c3d7f76173e`.
'''.lstrip()

setup(name=name,
      version="0.2.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-paramiko'],
      packages=['pysftp-stubs'],
      package_data={'pysftp-stubs': ['__init__.pyi', 'exceptions.pyi', 'helpers.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
