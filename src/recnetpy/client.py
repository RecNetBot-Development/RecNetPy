from .rest import RouteManager
from .managers import AccountManager, EventManager, ImageManager, InventionManager, RoomManager

class Client:
    """
    The main interface used for interacting and accessing RecNet data.
    """
    rec_net: RouteManager
    accounts: AccountManager
    events: EventManager
    images: ImageManager
    inventions: InventionManager
    rooms: RoomManager

    def __init__(self) -> None:
        self.rec_net = RouteManager()
        self.accounts = AccountManager(self)
        self.events = EventManager(self)
        self.images = ImageManager(self)
        self.inventions = InventionManager(self)
        self.rooms = RoomManager(self)

    async def close(self) -> None:
        await self.rec_net.stop()