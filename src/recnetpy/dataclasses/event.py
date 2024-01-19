from typing import TYPE_CHECKING, Dict, Optional, List

from .base import BaseDataClass
from .event_response import EventInteraction
from ..misc import date_to_unix, list_chunks
from ..misc.constants import ACCESSIBILITY_DICT

if TYPE_CHECKING:
    from . import Account, Room, Image
    from ..misc.api_responses import EventResponse, EventResponseResponse, AccountResponse
    from ..rest import Response 


BROADCAST_PERMISSION_DICT: Dict[int, str] = {
    0: None,
    256: "Room Owners",
    2147483647: "All"
}

class Event(BaseDataClass['EventResponse']):
    """
    This class represents a RecNet event.
    """
    
    #: This is an event's unique identifier.
    id: int
    #: This is the id of the player who created the event.
    creator_player_id: int
    #: This is the file name of the event thumbnail.
    image_name: Optional[str]
    #: This is the id of the room where the event is taking place.
    room_id: int
    #: This is the id of the subroom where the event ts taking place.
    subroom_id: Optional[int]
    #: This is the id of the club that the event is being hosted by.
    club: Optional[int]
    #: This is the name of the event.
    name: str
    #: This is the description of the event.
    description: str
    #: This is the date the event will start represented as an Unix integer.
    start_time: int
    #: This is the date the event will end represented as an Unix integer.
    end_time: int
    #: This is the number of people attending the event.
    attendee_count: int
    #: This is the visibility of the event which has the possible values of ``['Private', 'Public', 'Unlisted']``.
    accessibility: str
    #: This is true if the event supports broadcasting, false if it doesn't.
    is_multi_instance: bool
    #: This is true if the event has cross-instance chat enabled, false if it doesn't. 
    support_multi_instance_room_chat: bool
    #: This defines who has broadcasting permissions which has the possible values of ``[None, 'Room Owners', 'All']``
    default_broadcast_permissions: str
    #: This defines who can request to broadcast which has the possible values of ``[None, 'Room Owners', 'All']``
    can_request_broadcast_permissions: str
    #: This is an account object which represents who created the event.
    creator_player: Optional['Account'] = None
    #: This is a room object which represents the room where the event is taking place.
    room: Optional['Room'] = None
    #: This is a list of event interaction objects which represents the event responses.
    responses: Optional[List['EventInteraction']] = None
    #: This is a list of image objects that represent images taken during the event.
    images: Optional[List['Image']] = None

    def patch_data(self, data: 'EventResponse') -> None:
        """
        Sets properties corresponding to data for an api event response.

        :param data: Data from the api.
        """
        self.data = data
        self.id = data['PlayerEventId']
        self.creator_player_id = data['CreatorPlayerId']
        self.image_name = data['ImageName']
        self.room_id = data['RoomId']
        #self.subroom_id = data['SubRoomId']
        self.club = data['ClubId']
        self.name = data['Name']
        self.description = data['Description']
        self.start_time = date_to_unix(data['StartTime'], new=False)
        self.end_time = date_to_unix(data['EndTime'], new=False)
        self.attendee_count = data['AttendeeCount']
        #self.accessibility = ACCESSIBILITY_DICT.get(data['Accessibility'], "Unknown")
        #self.is_multi_instance = data['IsMultiInstance']
        #self.support_multi_instance_room_chat = data['SupportMultiInstanceRoomChat']
        #self.default_broadcast_permissions = BROADCAST_PERMISSION_DICT.get(data['DefaultBroadcastPermissions'], "Unknown")
        #self.can_request_broadcast_permissions = BROADCAST_PERMISSION_DICT.get(data['CanRequestBroadcastPermissions'], "Unkown")

    async def get_images(self, take: int = 16, skip: int = 0, force: bool = False) -> List['Image']:
        """
        Fetches a list of images during this event. Returns a
        cached result, if this function has been already called.

        :param take: The number of results to return.
        :param skip: The number of results to skip.
        :param force: If true, fetches new data.
        :return: A list of images.
        """
        if self.images is None or force:
            self.images = await self.client.images.during_event(self.id, take = take, skip = skip)
        return self.images

    async def get_creator_player(self, force: bool = False) -> 'Account':
        """
        Fetches the creator of this event. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: An account object.
        """
        if self.creator_player is None or force:
            self.creator_player = await self.client.accounts.fetch(self.creator_player_id)
        return self.creator_player

    async def get_room(self, include: int = 0, force: bool = False) -> Optional['Room']:
        """
        Fetches the room this event is happening in. Returns a
        cached result, if this function has been already called.
        If the room is private, nothing will be returned.

        | Include param values:

        ===== ===================
        Value Resolve
        ===== ===================
        2     Subrooms
        4     Roles
        8     Tags
        32    Promotional content
        64    Scores
        256   Loading screens
        ===== ===================

        :param include: An integer that add additional information to the response.
        :param force: If true, fetches new data.
        :return: A room object.
        """
        if self.room is None or force:
            self.room = await self.client.rooms.fetch(self.room_id, include = include)
        return self.room

    async def get_responses(self, force: bool = False) -> List['EventInteraction']:
        """
        Fetches the event responses for this event. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data
        :return: A list of event interaction objects.
        """
        if self.responses is None or force:
            data: Response[List['EventResponseResponse']] = await self.rec_net.events(self.id).responses.make_request('get')
            self.responses = EventInteraction.create_from_list(data.data)
        return self.responses

    async def resolve_responders(self, force: bool = False) -> List['EventInteraction']:
        """
        Resolves the players who responded to the event. This function
        will make an api call every time its used. It should only be used when 
        updating the response player attribute.

        :param force: Forces new responses to be fetched.
        :return: A list of event interation objects. 
        """
        
        if self.responses is None or force:
            responses = await self.get_responses(force)
            players: Dict[int, Account] = {}
            for response in responses:
                player = self.client.accounts.create_dataclass(response.player_id)
                response.player = player
                players[response.player_id] = player

            player_ids = list(players.keys())
            data: List[AccountResponse] = []

            # 750 == roughly 9750 bytes of payload
            # limit of 10240 bytes in API
            if len(player_ids) > 750:
                player_chunks = list_chunks(player_ids, 750)
                for i in player_chunks:
                    response: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.bulk.make_request('post', body = {"id": i})
                    data += response.data
            else:
                # Fits in a single payload
                response: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.bulk.make_request('post', body = {"id": player_ids})
                data = response.data

            for data_response in data: players.get(data_response['accountId']).patch_data(data_response)
        return self.responses