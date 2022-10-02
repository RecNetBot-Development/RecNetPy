from typing import TYPE_CHECKING, List, Optional, Union

from .base import BaseDataClass
from ..misc import date_to_unix
from ..misc.constants import ACCESSIBILITY_DICT

if TYPE_CHECKING:
    from . import Account, Room, Event
    from ..misc.api_responses import ImageResponse
    from ..rest import Response

class Image(BaseDataClass['ImageResponse']):
    """
    This class represents a RecNet image.
    """
    id: int
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
    cheer_player_ids: Optional[List[int]] = None
    cheer_players: Optional[List['Account']] = None
    comment_count: int
    player: Optional['Account']
    tagged_players: Optional[List['Account']]
    room: Optional['Room']
    player_event: Optional['Event']

    def patch_data(self, data: 'ImageResponse') -> None:
        """
        Sets properties corresponding to data for an api event response.

        @param data: Data from the api.
        """
        self.id = data['Id']
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
        
    async def get_cheers(self, force: bool = False) -> List[int]:
        """
        Fetches a list of players' ids who cheered the post. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: A list of account ids.
        """
        
        if self.cheer_player_ids is None or force:
            data: 'Response[List[int]]' = await self.rec_net.api.images.v1(self.id).cheers.make_request('get')
            self.cheer_player_ids = data.data
            
        return self.cheer_player_ids

    
