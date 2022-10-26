Getting Started
===============

.. _getting_started:

Installation
############

All platforms via `pip <https://pypi.org/project/pip/>`_:

.. code-block:: PowerShell

    $ pip install -U recnetpy

Quickstart
##########

Creating an instance of RecNetPy:

.. code-block:: Python

    import recnetpy

    RecNet = recnetpy.Client()

An example that showcases how to fetch an account by username and acquire its bio:

.. code-block:: Python

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

.. note:: 
    For more examples and usage, please refer to the :doc:`examples`.

Development Setup
#################

To install a local build run the following command.

.. code-block:: PowerShell

    $ pip install .

Contributing
############

1. Fork it (<https://github.com/RecNetBot-Development/RecNetPy/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

