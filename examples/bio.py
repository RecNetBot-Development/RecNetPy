"""
An example that showcases how to fetch an account by username and acquire its bio.
"""

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