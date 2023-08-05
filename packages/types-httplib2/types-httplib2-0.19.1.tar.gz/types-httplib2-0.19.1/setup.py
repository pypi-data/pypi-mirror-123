from setuptools import setup

name = "types-httplib2"
description = "Typing stubs for httplib2"
long_description = '''
## Typing stubs for httplib2

This is a PEP 561 type stub package for the `httplib2` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `httplib2`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/httplib2. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `9f869723509ac027bae6b6f567b921d6a229e8ec`.
'''.lstrip()

setup(name=name,
      version="0.19.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['httplib2-stubs'],
      package_data={'httplib2-stubs': ['__init__.pyi', 'auth.pyi', 'certs.pyi', 'error.pyi', 'iri2uri.pyi', 'socks.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
