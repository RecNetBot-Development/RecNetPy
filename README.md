# RecNetPy
> **RecNetPy** is an API wrapper built in Python for pulling data from [RecNet](https://rec.net/). **RecNetPy** aims to be easy to use yet powerful. It's the same wrapper used to power [RecNetBot](https://github.com/RecNetBot-Development/RecNetBot)!.

[![NPM Version][pip-image]][pip-url]
[![Downloads Stats][pip-downloads]][pip-url]
[![Join The Discord][discord]][discord-url]

![](img/header.png)

## Installation

All platforms via [pip](https://pypi.org/project/pip/):

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
import recnetpy
from asyncio import get_event_loop

async def main():
    RecNet = recnetpy.Client()
    user = await RecNet.accounts.get("ColinXYZ")
    bio = await user.get_bio()
    print(bio)
    await RecNet.close()

loop = get_event_loop()
loop.run_until_complete(main())
```

_For more examples and usage, please refer to the [``examples``](https://github.com/RecNetBot-Development/RecNetPy/tree/main/examples)._

## Development setup

To install a local build run the following command.

```sh
pip install .
```

## Meta

_Distributed under the MIT license. See ``LICENSE`` for more information._


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
