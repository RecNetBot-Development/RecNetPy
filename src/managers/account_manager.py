from . import BaseManager
from .. import Client
from ..dataclasses import Account
from ..misc.api_responses import AccountResponse

class AccountManager(BaseManager[Account, AccountResponse]):
    def __init__(self, client: Client) -> None:
        super().__init__(client)
        self.dataclass = Account