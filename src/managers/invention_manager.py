from typing import List, Optional

from . import BaseManager
from ..dataclasses import Invention
from ..misc.api_responses import InventionResponse
from ..rest import Response

class InventionManager(BaseManager[Invention, InventionResponse]):
    async def fetch(self, id: int) -> Invention:
        """
        Gets invention data by their id, and returns it as an invention object.

        @param id: The id of the invention.
        @return: An invention object representing the data. 
        """
        data: Response[InventionResponse] = await self.rec_net.api.inventions.v1.make_request('get', params = {'inventionId': id})
        return self.create_dataclass(id, data.data)

    async def search(self, query: str) -> List[Invention]:
        """
        Searches RecNet for inventions based on a query, and returns
        a list of invention objects.

        @param query: A search query string.
        @return: A list of invention objects.
        """
        data: Response[List[InventionResponse]] = await self.rec_net.api.inventions.v2.search.make_request('get', params = {'value': query})
        return self.create_from_data_list(data.data)

    async def featured(self) -> List[Invention]:
        """
        Gets a list of the featured inventions on RecNet.

        @return: A list of invention objects.
        """
        data: Response[List[InventionResponse]] = await self.rec_net.api.inventions.v1.featured.make_request('get')
        return self.create_from_data_list(data.data)

    async def top_today(self) -> List[Invention]:
        """
        Gets a list of the top inventions on RecNet for today.

        @return: A list of invention objects.
        """
        data: Response[List[InventionResponse]] = await self.rec_net.api.inventions.v1.toptoday.make_request('get')
        return self.create_from_data_list(data.data)

    def create_dataclass(self, id: int, data: Optional[InventionResponse] = None) -> Invention:
        """
        Creates an invention object:

        @param id: An invention id.
        @param data: An invention api response.
        @return: Returns an invention object.
        """
        return Invention(self.client, id, data)

    def create_from_data_list(self, data: List[InventionResponse]) -> List[Invention]:
        """
        Creates a list of invention objects based on a list of data.

        @param data: A list of an invention api responses.
        @return: A list of invention objects.
        """
        invention_list: List[Invention] = []
        for invention_data in data:
            invention_obj = Invention(self.client, invention_data['InventionId'], invention_data)
            invention_list.append(invention_obj)
        return invention_list