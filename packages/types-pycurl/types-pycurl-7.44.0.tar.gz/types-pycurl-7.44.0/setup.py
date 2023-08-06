from setuptools import setup

name = "types-pycurl"
description = "Typing stubs for pycurl"
long_description = '''
## Typing stubs for pycurl

This is a PEP 561 type stub package for the `pycurl` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pycurl`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pycurl. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `bb24e77404af84b0ff32020ad6c356c659bc6fe5`.
'''.lstrip()

setup(name=name,
      version="7.44.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['pycurl-stubs'],
      package_data={'pycurl-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
