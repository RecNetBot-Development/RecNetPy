from asyncio import get_event_loop

from src import Client

async def main():
    RecNet = Client()
    user = await RecNet.accounts.get("ColinXYZ")
    bio = await user.get_bio()
    print(bio)
    await RecNet.close()

loop = get_event_loop()
loop.run_until_complete(main())