from typing import Dict, Optional

from . import BaseDataClass, Account, Room
from ..misc import date_to_unix
from ..misc.api_responses import EventResponse
from ..misc.constants import ACCESSIBILITY_DICT

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
    creator_player: Optional[Account]
    room: Optional[Room]

    def patch_data(self, data: EventResponse) -> None:
        """
        Sets properties corresponding to data for an api event response.

        @param data: Data from the api.
        """
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