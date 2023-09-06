from typing import TYPE_CHECKING, List, Optional
from ..misc import stringify_bulk
from . import BaseManager
from ..dataclasses import Account

if TYPE_CHECKING:
    from ..misc.api_responses import AccountResponse
    from ..rest import Response

class AccountManager(BaseManager['Account', 'AccountResponse']):
    """
    This is a factory object for creating account objects. Its the
    main interface for fetching account related data.
    """
    async def get(self, name: str) -> Optional['Account']:
        """
        Gets user data by their username, and returns it as an account object.
        Returns nothing if the account doesn't exist.

        Authorization required.

        :param name: The username of the RecNet user.
        :return: An account object representing the data or nothing if not found. 
        """
        data: 'Response[AccountResponse]' = await self.rec_net.accounts.make_request('get', params = {'username': str(name)})
        if data.success and data.data: return self.create_dataclass(data.data['accountId'], data.data)
        return None

    async def fetch(self, id: int) -> Optional['Account']:
        """
        Gets user data by their id, and returns it as an account object.
        Returns nothing if an account with the specified id doesn't exist.

        Authorization required.

        :param id: The id of the RecNet user.
        :return: An account object representing the data or nothing if not found. 
        """
        data: 'Response[AccountResponse]' = await self.rec_net.accounts(id).make_request('get')
        if data.success and data.data: return self.create_dataclass(id, data.data)
        return None
    
    async def get_many(self, names: List[str]) -> List['Account']:
        """
        Gets a list of users by a list of usernames, and returns 
        a list of account object.
        Accounts that couldn't be found will be silently ignored.

        Authorization required.

        :param names: A list of username.
        :return: A list of account objects. 
        """
        bulk = stringify_bulk(names)
        data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.bulk.make_request('post', body = {'name': bulk})
        if data.success: return self.create_from_data_list(data.data)
        return []

    async def fetch_many(self, ids: List[int]) -> List['Account']:
        """
        Gets a list of users by a list of ids, and returns 
        a list of account object.
        Accounts that couldn't be found will be silently ignored.

        Authorization required.

        :param ids: A list of ids.
        :return: A list of account objects. 
        """
        data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.bulk.make_request('post', body = {'id': ids})
        if data.success: return self.create_from_data_list(data.data)
        return []

    async def search(self, query: str) -> List['Account']:
        """
        Searches RecNet for users based on a query, and returns
        a list of account objects.
        If no account is found, an empty list will be returned.

        Authorization required.

        :param query: A search query string.
        :return: A list of account objects.
        """
        data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.search.make_request('get', params = {'name': str(query)})
        if data.success: return self.create_from_data_list(data.data)
        return []

    def create_dataclass(self, id: int, data: Optional['AccountResponse'] = None) -> 'Account':
        """
        Creates an account object:

        :param id: An account id.
        :param data: An account api response.
        :return: Returns an account object.
        """
        return Account(self.client, id, data)

    def create_from_data_list(self, data: List['AccountResponse']) -> List['Account']:
        """
        Creates a list of account objects based on a list of data.

        :param data: A list of an account api responses.
        :return: A list of account objects.
        """
        account_list: List['Account'] = []
        for account_data in data:
            account_obj = Account(self.client, account_data['accountId'], account_data)
            account_list.append(account_obj)
        return account_list


