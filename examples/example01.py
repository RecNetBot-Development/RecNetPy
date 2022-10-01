from ..src import Client

async def main():
    RecNet = Client()
    user = await RecNet.accounts.get("ColinXYZ")
    bio = await user.get_bio()
    print(bio)