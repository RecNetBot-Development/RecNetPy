from typing import List, Optional, Union

from . import BaseDataClass, Account, Room, Event
from ..misc import date_to_unix
from ..misc.api_responses import ImageResponse
from ..misc.constants import ACCESSIBILITY_DICT

class Image(BaseDataClass[ImageResponse]):
    """
    This class represenst a RecNet image.
    """
    type: int
    accessibility: str
    accessibility_locked: bool
    image_name: str
    description: Optional[str]
    player_id: int
    tagged_player_ids: List[int]
    room_id: int
    player_event_id: Optional[int]
    created_at: int
    cheer_count: int
    comment_count: int
    player: Optional[Account]
    tagged_players: Optional[List[Account]]
    room: Optional[Room]
    player_event: Optional[Event]

    def patch_data(self, data: ImageResponse) -> None:
        """
        Sets properties corresponding to data for an api event response.

        @param data: Data from the api.
        """
        self.type = data['Type']
        self.accessibility = ACCESSIBILITY_DICT.get(data['Accessibility'], "Unknown")
        self.accessibility_locked = data['AccessibilityLocked']
        self.image_name = data['ImageName']
        self.description = data['Description']
        self.player_id = data['PlayerId']
        self.tagged_player_ids = data['TaggedPlayerIds']
        self.room_id = data['RoomId']
        self.player_event_id = data['PlayerEventId']
        self.created_at = date_to_unix(data['CreatedAt'])
        self.cheer_count = data['CheerCount']
        self.comment_count = data['CommentCount']
