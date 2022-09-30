from typing import List, Optional

from . import BaseManager
from ..dataclasses import Event
from ..misc.api_responses import EventResponse
from ..rest import Response


class EventManager(BaseManager[Event, EventResponse]):
    async def fetch(self, id: int) -> Event:
        """
        Gets event data by their id, and returns it as an event object.

        @param id: The id of the event.
        @return: An event object representing the data. 
        """
        data: Response[EventResponse] = await self.rec_net.api.playerevents.v1(id).make_request('get')
        return self.create_dataclass(id, data.data)

    async def fetch_many(self, ids: List[int]) -> List[Event]:
        """
        Gets a list of events by a list of event ids, and returns 
        a list of event object.

        @param ids: A list of ids.
        @return: A list of event objects. 
        """
        data: Response[List[EventResponse]] = await self.rec_net.api.playerevents.v1.bulk.make_request('post', body = {'id': ids})
        return self.create_from_data_list(data.data)

    async def search(self, query: str, take: int = 16, skip: int = 0, sort: int = 0) -> List[Event]:
        """
        Searches RecNet for events based on a query, and returns
        a list of event objects.

        @param query: A search query string.
        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @param sort: An integer that describes how the results are to be sorted.
        @return: A list of event objects.
        """
        params = {
            'query': query,
            'take': take,
            'skip': skip,
            'sort': sort
        }
        data: Response[List[EventResponse]] = await self.rec_net.api.playerevents.v1.search.make_request('get', params=params)
        return self.create_from_data_list(data.data)

    async def from_account(self, id: int, take: int = 16, skip: int = 0) -> List[Event]:
        """
        Gets a list of events created by a player.

        @param id: An account id.
        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @return: A list of event objects.
        """
        params = {
            'take': take,
            'skip': skip,
        }
        data: Response[List[EventResponse]] = await self.rec_net.api.playerevents.v1.creator(id).make_request('get', params=params)
        return self.create_from_data_list(data.data)

    async def in_room(self, id: int, take: int = 16, skip: int = 0) -> List[Event]:
        """
        Gets a list of events happening in a room.

        @param query: A room id.
        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @return: A list of event objects.
        """
        params = {
            'take': take,
            'skip': skip,
        }
        data: Response[List[EventResponse]] = await self.rec_net.api.playerevents.v1.room(id).make_request('get', params=params)
        return self.create_from_data_list(data.data)

    async def get_events(self, take: int = 16, skip: int = 0, sort: int = 0) -> List[Event]:
        """
        Gets a list of events currently happening.

        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @param sort: An integer that describes how the results are to be sorted.
        @return: A list of event objects.
        """
        params = {
            'take': take,
            'skip': skip,
            'sort': sort
        }
        data: Response[List[EventResponse]] = await self.rec_net.api.playerevents.v1.make_request('get', params=params)
        return self.create_from_data_list(data.data)

    def create_dataclass(self, id: int, data: Optional[EventResponse] = None) -> Event:
        """
        Creates an event object:

        @param id: An event id.
        @param data: An event api response.
        @return: Returns an event object.
        """
        return Event(self.client, id, data)

    def create_from_data_list(self, data: List[EventResponse]) -> List[Event]:
        """
        Creates a list of event objects based on a list of data.

        @param data: A list of an event api responses.
        @return: A list of event objects.
        """
        event_list: List[Event] = []
        for event_data in data:
            event_obj = Event(self.client, event_data['PlayerEventId'], event_data)
            event_list.append(event_obj)
        return event_list
