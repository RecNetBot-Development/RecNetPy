from .rest import RouteManager
from .managers import AccountManager, EventManager, ImageManager, InventionManager, RoomManager

class Client:
    """
    The main interface used for interacting and accessing RecNet data.
    """

    #: All request are routed through this manager. It responsible for managing data.
    rec_net: RouteManager
    #: Use this property to request account data. It serves as a factory for all account objects.
    accounts: AccountManager
    #: Use this property to request event data. It serves as a factory for all event objects.
    events: EventManager
    #: Use this property to request image data. It serves as a factory for all image objects.
    images: ImageManager
    #: Use this property to request invention data. It serves as a factory for all invention objects.
    inventions: InventionManager
    #: Use this property to request room data. It serves as a factory for all room objects.
    rooms: RoomManager

    def __init__(self, api_key: str = None) -> None:
        self.rec_net = RouteManager(api_key)
        self.accounts = AccountManager(self)
        self.events = EventManager(self)
        self.images = ImageManager(self)
        self.inventions = InventionManager(self)
        self.rooms = RoomManager(self)

    async def close(self) -> None:
        """
        This function closes the underlying connection to the server,
        and closes the thread pool. Its recommended to call this function
        at the end of the program.
        """
        await self.rec_net.stop()