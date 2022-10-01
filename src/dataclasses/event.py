from typing import Dict, Optional, List

from . import BaseDataClass, Account, Room, EventInteraction, Image
from ..misc import date_to_unix
from ..misc.api_responses import EventResponse, EventResponseResponse, AccountResponse
from ..misc.constants import ACCESSIBILITY_DICT
from ..rest import Response 

BROADCAST_PERMISSION_DICT: Dict[int, str] = {
    0: "None",
    256: "Room Owners",
    2147483647: "All"
}

class Event(BaseDataClass[EventResponse]):
    """
    This class represents a RecNet event.
    """
    creator_player_id: int
    image_name: Optional[str]
    room_id: int
    subroom_id: Optional[int]
    club: Optional[int]
    name: str
    description: str
    start_time: int
    end_time: int
    attendee_count: int
    accessibility: str
    is_multi_instance: bool
    support_multi_instance_room_chat: bool
    default_broadcast_permissions: str
    can_request_broadcast_permissions: str
    creator_player: Optional[Account] = None
    room: Optional[Room] = None
    responses: Optional[List[EventInteraction]] = None
    images: Optional[List[Image]] = None

    def patch_data(self, data: EventResponse) -> None:
        """
        Sets properties corresponding to data for an api event response.

        @param data: Data from the api.
        """
        self.data = data
        self.creator_player_id = data['CreatorPlayerId']
        self.image_name = data['ImageName']
        self.room_id = data['RoomId']
        self.subroom_id = data['SubRoomId']
        self.club = data['ClubId']
        self.name = data['Name']
        self.description = data['Description']
        self.start_time = date_to_unix(data['StartTime'])
        self.end_time = date_to_unix(data['EndTime'])
        self.attendee_count = data['AttendeeCount']
        self.accessibility = ACCESSIBILITY_DICT.get(data['Accessibility'], "Unknown")
        self.is_multi_instance = data['IsMultiInstance']
        self.support_multi_instance_room_chat = data['SupportMultiInstanceChat']
        self.default_broadcast_permissions = BROADCAST_PERMISSION_DICT.get(data['DefaultBroadcastPermissions'], "Unknown")
        self.can_request_broadcast_permissions = BROADCAST_PERMISSION_DICT.get(data['CanRequestBroadcastPermissions'], "Unkown")

    async def get_images(self, take: int = 16, skip: int = 0, force: bool = False) -> List[Image]:
        """
        Fetches a list of images during this event. Returns a
        cached result, if this function has been already called.

        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @param force: If true, fetches new data.
        @return: A list of images.
        """
        if self.images in None or force:
            self.images = await self.client.images.during_event(self.id)
        return self.images

    async def get_creator_player(self) -> Account:
        """
        Fetches the creator of this event. Returns a
        cached result, if this function has been already called.

        @return: An account object.
        """
        if self.creator_player is None:
            self.creator_player = await self.client.accounts.fetch(self.creator_player_id)
        return self.creator_player

    async def get_room(self, include: int, force: bool = False) -> Room:
        """
        Fetches the room this event is happening in. Returns a
        cached result, if this function has been already called.

        Include param values:
        - +2 = Subrooms
        - +4 = Roles
        - +8 = Tags
        - +32 = Promotional content
        - +64 = Scores
        - +256 = Loading screens

        @param include: An integer that add additional information to the response.
        @param force: If true, fetches new data.
        @return: A room object.
        """
        if self.room is None or force:
            self.room = await self.client.rooms.fetch(self.room_id)
        return self.room

    async def get_responses(self, force: bool = False) -> List[EventInteraction]:
        """
        Fetches the event responses for this event. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data
        @return: A list of event interaction objects.
        """
        if self.responses is None or force:
            data: Response[List[EventResponseResponse]] =  self.rec_net.api.playerevents.v1(self.id).responses.make_request('get')
            self.responses = EventInteraction.create_from_list(data.data)
        return self.responses

    async def resolve_responders(self, force: bool = False) -> List[EventInteraction]:
        """
        Resolves the players who responded to the event. This function
        will make an api call every time its used. It should only be used when 
        updating the response player attribute.

        @param force: Forces new responses to be fetched.
        @return: A list of event interation objects. 
        """
        responses = await self.get_responses(force)
        players: Dict[int, Account] = []
        for response in responses:
            player = Account(self.client, response.player_id)
            response.player = player
            players[response.player_id] = player
        data: Response[List[AccountResponse]] = await self.rec_net.accounts.account.bulk.make_request('post', body = {id: players.keys})
        for data_response in data.data: players.get(data_response['accountId']).patch_data(data_response)
        return self.responses