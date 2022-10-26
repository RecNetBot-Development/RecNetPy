# RecNetPy
> **RecNetPy** is an API wrapper built in Python for pulling data from [RecNet](https://rec.net/). **RecNetPy** aims to be easy to use yet powerful. It's the same wrapper used to power [RecNetBot](https://github.com/RecNetBot-Development/RecNetBot)!.

[![NPM Version][pip-image]][pip-url]
[![Downloads Stats][pip-downloads]][pip-url]
[![Join The Discord][discord]][discord-url]
[![Documentation Status][readthedocs]][readthedocs-url]

## Installation

All platforms via [pip][pip-url]:

```sh
pip install -U recnetpy
```

## Quickstart

Creating an instance of RecNetPy:
```py
import recnetpy

RecNet = recnetpy.Client()
```

An example that showcases how to fetch an account by username and acquire its bio:
```py
import recnetpy  # Import the module
import asyncio

async def main():
    # Create a new RecNetPy client instance
    RecNet = recnetpy.Client()
    
    # Fetch the user from the AccountManager with the "get" method
    user = await RecNet.accounts.get("ColinXYZ")
    
    # Fetch the bio from the Account dataclass
    bio = await user.get_bio()
    
    # Print and close the client
    print(bio)
    await RecNet.close()

asyncio.run(main())
```

_For more examples and usage, please refer to the [``examples``][examples-url]. More documentation can be found [Here][documentation]._

## Development setup

To install a local build run the following command.

```sh
pip install .
```

## Meta

_Distributed under the MIT license. See [``LICENSE``][license] for more information._


## Contributing

1. Fork it (<https://github.com/RecNetBot-Development/RecNetPy/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[pip-image]: https://img.shields.io/pypi/v/recnetpy?style=flat-square
[pip-url]: https://pypi.org/project/recnetpy/
[pip-downloads]: https://img.shields.io/pypi/dm/recnetpy?style=flat-square
[discord]: https://img.shields.io/discord/745219512529584195?style=flat-square
[discord-url]: https://discord.gg/GPVdhMa2zK
[documentation]: https://recnetpy.readthedocs.io/en/latest/index.html
[readthedocs]: https://readthedocs.org/projects/recnetpy/badge/?version=latest
[readthedocs-url]: https://recnetpy.readthedocs.io/en/latest/?badge=latest
[pip-url]: https://pypi.org/project/pip/
[examples-url]: https://github.com/RecNetBot-Development/RecNetPy/tree/main/examples
[license]: https://github.com/RecNetBot-Development/RecNetPy/blob/main/LICENSE