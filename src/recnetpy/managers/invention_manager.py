from typing import TYPE_CHECKING, List, Optional

from . import BaseManager
from ..dataclasses import Invention

if TYPE_CHECKING:
    from ..misc.api_responses import InventionResponse
    from ..rest import Response

class InventionManager(BaseManager['Invention', 'InventionResponse']):
    """
    This is a factory object for creating invention objects. Its the
    main interface for fetching invention related data.
    """
    async def fetch(self, id: int) -> Optional['Invention']:
        """
        Gets invention data by their id, and returns it as an invention object.
        Returns nothing if the invention doesn't exist or is private.

        Authorization required.

        :param id: The id of the invention.
        :return: An invention object representing the data or nothing if not found. 
        """
        data: 'Response[InventionResponse]' = await self.rec_net.apim.inventions.v1.make_request('get', params = {'inventionId': id})
        if data.success: return self.create_dataclass(id, data.data)
        return None


    async def search(self, query: str, take: int = 16) -> List['Invention']:
        """
        Searches RecNet for inventions based on a query, and returns
        a list of invention objects.
        If no invention is found, an empty list will be returned.

        Authorization required.

        :param query: A search query string.
        :return: A list of invention objects.
        """
        params = {
            'value': str(query),
            'take': take
        }
        data: Response[List[InventionResponse]] = await self.rec_net.apim.inventions.v2.search.make_request('get', params = params)
        return self.create_from_data_list(data.data)

    async def featured(self, take: int = 16, skip: int = 0) -> List['Invention']:
        """
        Gets a list of the featured inventions on RecNet.

        Authorization required.

        :param take: The number of results to return.
        :param skip: The number of results to skip.
        :return: A list of invention objects.
        """
        params = {
            'take': take,
            'skip': skip
        }  
        data: 'Response[List[InventionResponse]]' = await self.rec_net.apim.inventions.v1.featured.make_request('get', params = params)
        return self.create_from_data_list(data.data)

    async def top_today(self) -> List['Invention']:
        """
        Gets a list of the top inventions on RecNet for today.

        Authorization required.

        :return: A list of invention objects.
        """
        data: 'Response[List[InventionResponse]]' = await self.rec_net.apim.inventions.v1.toptoday.make_request('get')
        return self.create_from_data_list(data.data)

    def create_dataclass(self, id: int, data: Optional['InventionResponse'] = None) -> 'Invention':
        """
        Creates an invention object:

        :param id: An invention id.
        :param data: An invention api response.
        :return: Returns an invention object.
        """
        return Invention(self.client, id, data)

    def create_from_data_list(self, data: List['InventionResponse']) -> List['Invention']:
        """
        Creates a list of invention objects based on a list of data.

        :param data: A list of an invention api responses.
        :return: A list of invention objects.
        """
        invention_list: List['Invention'] = []
        for invention_data in data:
            invention_obj = Invention(self.client, invention_data['InventionId'], invention_data)
            invention_list.append(invention_obj)
        return invention_list