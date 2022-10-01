from typing import TYPE_CHECKING, List, Optional

from . import BaseManager
from ..dataclasses import Account

if TYPE_CHECKING:
    from ..misc.api_responses import AccountResponse
    from ..rest import Response

class AccountManager(BaseManager['Account', 'AccountResponse']):
    async def get(self, name: str) -> 'Account':
        """
        Gets user data by their username, and returns it as an account object.

        @param name: The username of the RecNet user.
        @return: An account object representing the data. 
        """
        data: 'Response[AccountResponse]' = await self.rec_net.accounts.account.make_request('get', params = {'username': name})
        return self.create_dataclass(data.data['accountId'], data.data)

    async def fetch(self, id: int) -> 'Account':
        """
        Gets user data by their id, and returns it as an account object.

        @param id: The id of the RecNet user.
        @return: An account object representing the data. 
        """
        data: 'Response[AccountResponse]' = await self.rec_net.accounts.account(id).make_request('get')
        return self.create_dataclass(id, data.data)

    async def get_many(self, names: List[str]) -> List['Account']:
        """
        Gets a list of users by a list of usernames, and returns 
        a list of account object.

        @param names: A list of username.
        @return: A list of account objects. 
        """
        data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.account.bulk.make_request('post', body = {'name': names})
        return self.create_from_data_list(data.data)

    async def fetch_many(self, ids: List[int]) -> List['Account']:
        """
        Gets a list of users by a list of ids, and returns 
        a list of account object.

        @param ids: A list of ids.
        @return: A list of account objects. 
        """
        data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.account.bulk.make_request('post', body = {'id': ids})
        return self.create_from_data_list(data.data)

    async def search(self, query: str) -> List['Account']:
        """
        Searches RecNet for users based on a query, and returns
        a list of account objects.

        @param query: A search query string.
        @return: A list of account objects.
        """
        data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.account.search.make_request('get', params = {'name': query})
        return self.create_from_data_list(data.data)

    def create_dataclass(self, id: int, data: Optional['AccountResponse'] = None) -> 'Account':
        """
        Creates an account object:

        @param id: An account id.
        @param data: An account api response.
        @return: Returns an account object.
        """
        return Account(self.client, id, data)

    def create_from_data_list(self, data: List['AccountResponse']) -> List['Account']:
        """
        Creates a list of account objects based on a list of data.

        @param data: A list of an account api responses.
        @return: A list of account objects.
        """
        account_list: List['Account'] = []
        for account_data in data:
            account_obj = Account(self.client, account_data['accountId'], account_data)
            account_list.append(account_obj)
        return account_list


