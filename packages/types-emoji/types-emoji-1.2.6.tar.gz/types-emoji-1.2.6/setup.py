from setuptools import setup

name = "types-emoji"
description = "Typing stubs for emoji"
long_description = '''
## Typing stubs for emoji

This is a PEP 561 type stub package for the `emoji` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `emoji`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/emoji. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `994b69ef8f18e76689daca3947879c3d7f76173e`.
'''.lstrip()

setup(name=name,
      version="1.2.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['emoji-stubs'],
      package_data={'emoji-stubs': ['__init__.pyi', 'core.pyi', 'unicode_codes/__init__.pyi', 'unicode_codes/en.pyi', 'unicode_codes/es.pyi', 'unicode_codes/it.pyi', 'unicode_codes/pt.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
