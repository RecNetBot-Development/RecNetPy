from typing import TYPE_CHECKING, List, Optional

from . import BaseManager
from ..dataclasses import Room
from ..misc import stringify_bulk

if TYPE_CHECKING:
    from ..misc.api_responses import RoomResponse, RoomSearchResponse
    from ..rest import Response

class RoomManager(BaseManager['Room', 'RoomResponse']):
    async def get(self, name: str, include: int = 0) -> 'Room':
        """
        Gets room data by their name, and returns it as an room object.
        Returns nothing if the room doesn't exist or is private.

        Include param values:
        - +2 = Subrooms
        - +4 = Roles
        - +8 = Tags
        - +32 = Promotional content
        - +64 = Scores
        - +256 = Loading screens

        @param name: The name of the room.
        @param include: An integer that add additional information to the response.
        @return: An room object representing the data or nothing if not found. 
        """
        data: 'Response[RoomResponse]' = await self.rec_net.rooms.rooms.make_request('get', params = {'name': name, 'include': include})
        if data.data: return self.create_dataclass(data.data['RoomId'], data.data)
        return None

    async def fetch(self, id: int, include: int = 0) -> 'Room':
        """
        Gets room data by their id, and returns it as an room object.

        Include param values:
        - +2 = Subrooms
        - +4 = Roles
        - +8 = Tags
        - +32 = Promotional content
        - +64 = Scores
        - +256 = Loading screens

        @param id: The id of the room.
        @param include: An integer that add additional information to the response.
        @return: An room object representing the data. 
        """
        data: 'Response[RoomResponse]' = await self.rec_net.rooms.rooms(id).make_request('get', params = {'include': include})
        return self.create_dataclass(data.data['RoomId'], data.data)

    async def get_many(self, names: List[str]) -> List['Room']:
        """
        Gets a list of rooms by a list of names, and returns 
        a list of rooms object.
        Room that couldn't be found or are private will be silently ignored.

        @param names: A list of room names.
        @return: A list of room objects. 
        """
        bulk = stringify_bulk(names)
        data: 'Response[List[RoomResponse]]' = await self.rec_net.rooms.rooms.bulk.make_request('post', body = {'name': bulk})
        return self.create_from_data_list(data.data)

    async def fetch_many(self, ids: List[int]) -> List['Room']:
        """
        Gets a list of rooms by a list of ids, and returns 
        a list of room objects.
        Room that couldn't be found or are private will be silently ignored.

        @param ids: A list of ids.
        @return: A list of room objects. 
        """
        data: 'Response[List[RoomResponse]]' = await self.rec_net.rooms.rooms.bulk.make_request('post', body = {'id': ids})
        return self.create_from_data_list(data.data)

    async def search(self, query: str, take: int = 16, skip: int = 0) -> List['Room']:
        """
        Searches RecNet for rooms based on a query, and returns
        a list of room objects.
        If no room is found, an empty list will be returned.

        @param query: A search query string.
        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @return: A list of room objects.
        """
        params = {
            'query': str(query),
            'take': take,
            'skip': skip
        }          
        data: 'Response[RoomSearchResponse]' = await self.rec_net.rooms.rooms.search.make_request('get', params = params)
        return self.create_from_data_list(data.data['Results'])

    async def created_by(self, id: int) -> List['Room']:
        """
        Gets a list of rooms created by a player.
        If no room or the respective account is found, an empty list will be returned.

        @param id: An account id.
        @return: A list of room objects.
        """
        data: 'Response[List[RoomResponse]]' = await self.rec_net.rooms.rooms.createdby(id).make_request('get')
        return self.create_from_data_list(data.data)

    async def owned_by(self, id: int) -> List['Room']:
        """
        Gets a list of rooms owned by a player.
        If no room or the respective account is found, an empty list will be returned.

        @param id: An account id.
        @return: A list of room objects.
        """
        data: 'Response[List[RoomResponse]]' = await self.rec_net.rooms.rooms.ownedby(id).make_request('get')
        return self.create_from_data_list(data.data)

    async def hot(self, take: int = 16, skip: int = 0) -> List[Room]:
        """
        Gets a list of the most popular rooms on RecNet.

        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @return: A list of room objects.
        """
        params = {
            'take': take,
            'skip': skip
        }  
        data: 'Response[RoomSearchResponse]' = await self.rec_net.rooms.rooms.hot.make_request('get', params = params)
        return self.create_from_data_list(data.data['Results'])

    def create_dataclass(self, id: int, data: Optional['RoomResponse'] = None) -> 'Room':
        """
        Creates an room object:

        @param id: An room id.
        @param data: An room api response.
        @return: Returns an room object.
        """
        return Room(self.client, id, data)

    def create_from_data_list(self, data: List['RoomResponse']) -> List['Room']:
        """
        Creates a list of room objects based on a list of data.

        @param data: A list of an room api responses.
        @return: A list of room objects.
        """
        room_list: List['Room'] = []
        for room_data in data:
            room_obj = Room(self.client, room_data['RoomId'], room_data)
            room_list.append(room_obj)
        return room_list