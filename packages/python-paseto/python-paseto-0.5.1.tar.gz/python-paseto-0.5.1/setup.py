# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paseto', 'paseto.crypto', 'paseto.paserk', 'paseto.protocol']

package_data = \
{'': ['*']}

install_requires = \
['pysodium>=0.7.10,<0.8.0']

setup_kwargs = {
    'name': 'python-paseto',
    'version': '0.5.1',
    'description': 'Platform-Agnostic Security Tokens for Python',
    'long_description': '# python-paseto\nPlatform-Agnostic Security Tokens for Python\n\n[![Build Status](https://travis-ci.com/purificant/python-paseto.svg?branch=main)](https://travis-ci.com/purificant/python-paseto)\n[![test-workflow](https://github.com/purificant/python-paseto/actions/workflows/test.yaml/badge.svg)](https://github.com/purificant/python-paseto/actions/workflows/test.yaml)\n[![PyPI version](https://badge.fury.io/py/python-paseto.svg)](https://badge.fury.io/py/python-paseto)\n[![Coverage Status](https://coveralls.io/repos/github/purificant/python-paseto/badge.svg?branch=main)](https://coveralls.io/github/purificant/python-paseto?branch=main)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/purificant/python-paseto.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/purificant/python-paseto/context:python)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n# Installation\n\n```bash\npip install python-paseto\n```\n\n### Check installation\n```python\npython -m paseto\n```\n`libsodium` is required, this will check if it is installed on your system. On Ubuntu 20.04 you can get it with `sudo apt install libsodium23`.\n\n# Low level API\nImplements PASETO Version2 and Version4 protocols supporting `v2.public`, `v2.local`, `v4.public` and `v4.local` messages.\nEvery protocol version provides access to encrypt() / decrypt() and sign() / verify() functions.\n\nLow level API is focuses on solid, high quality, production ready primitives\nas specified directly in the [PASETO](https://tools.ietf.org/html/draft-paragon-paseto-rfc-00) \nprotocol.\nSee [paseto-spec](https://github.com/paseto-standard/paseto-spec) for protocol details.\n\n# Example use with Version2\n```python\nfrom paseto.protocol.version2 import encrypt, decrypt\n\nmessage = b"foo"  # your data\nkey = b"0" * 32  # encryption key\n\ntoken = encrypt(message, key)\nplain_text = decrypt(token, key)\n\nassert plain_text == message\nprint(f"token={token}")\nprint(f"plain_text={plain_text}")\nprint(f"message={message}")\n```\n### With optional footer\n```python\nfrom paseto.protocol.version2 import encrypt, decrypt\n\nmessage = b"foo"  # your data\nkey = b"0" * 32  # encryption key\noptional_footer = b"sample_footer"  # authenticated but not encrypted metadata\n\ntoken = encrypt(message, key, optional_footer)\nplain_text = decrypt(token, key, optional_footer)\n\nassert plain_text == message\nprint(f"token={token}")\nprint(f"plain_text={plain_text}")\nprint(f"message={message}")\n```\n\n# Example use with Version4\n```python\nfrom paseto.protocol.version4 import create_symmetric_key, decrypt, encrypt\n\nmessage = b"this is a secret message"  # your data\nkey = create_symmetric_key()  # encryption key\n\ntoken = encrypt(message, key)\nplain_text = decrypt(token, key)\n\nassert plain_text == message\nprint(f"token={token}")\nprint(f"plain_text={plain_text}")\nprint(f"message={message}")\n```\n\n### Message signing\n```python\nfrom paseto.protocol.version4 import create_asymmetric_key, sign, verify\n\nmessage = b"this is a public message"  # your data\npublic_key, secret_key = create_asymmetric_key()  # signing / verifying keys\n\ntoken = sign(message, secret_key)\nverified_message = verify(token, public_key)\n\nassert verified_message == message\nprint(f"token={token}")\nprint(f"verified_message={verified_message}")\nprint(f"message={message}")\n```\n\n# High level API\nIn the future a high level API will provide developer friendly access to low level API\nand support easy integration into other projects.\n\n# Development\nTypical dev workflow operations are automated in [Makefile](https://github.com/purificant/python-paseto/blob/main/Makefile),\nincluding testing, linting, code quality checks, benchmarks and dev environment setup.\n\n# Contributing\nThis library is under active development and maintenance. For any feedback, questions,\ncomments or if you would like to request a feature, please raise an issue!\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/purificant/python-paseto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
