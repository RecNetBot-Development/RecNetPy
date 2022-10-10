from typing import TYPE_CHECKING, Dict, List, Optional

from .base import BaseDataClass
from .invention_version import InventionVersion
from .tag import Tag
from ..misc import date_to_unix
from ..misc.constants import ACCESSIBILITY_DICT

if TYPE_CHECKING:
    from . import Account, Room
    from ..misc.api_responses import InventionResponse, TagResponse
    from ..rest import Response


INVENTION_PERMISSION_DICT: Dict[int, str] = {
    0: "Unassigned",
    10: "Limited One Use Only",
    15: "Disallow Key Lock",
    20: "Use Only",
    40: "Edit and Save",
    60: "Publish",
    80: "Charge",
    100: "Unlimited"
}

class Invention(BaseDataClass['InventionResponse']):
    """
    This class represents an invention.
    """
    replication_id: str
    creator_player_id: int
    name: str
    description: str
    image_name: str
    current_version_number: int
    current_version: InventionVersion
    accessibility: str # 0 = private, 1 = public
    is_published: bool
    is_featured: bool
    modified_at: int
    created_at: int
    first_published_at: int
    creation_room_id: int
    num_players_have_used_in_room: int
    num_downloads: int
    cheer_count: int
    creator_permission: str
    general_permission: str
    is_ag_invention: bool
    is_certified_invention: bool
    price: int
    allow_trial: bool
    hide_from_player: bool
    creator_player: Optional['Account'] = None
    creation_room: Optional['Room'] = None
    tags: Optional[List['Tag']] = None

    def patch_data(self, data: 'InventionResponse') -> None:
        """
        Sets properties corresponding to data for an api invention response.

        :param data: Data from the api.
        """
        self.data = data
        self.replication_id = data['ReplicationId']
        self.creator_player_id = data['CreatorPlayerId']
        self.name = data['Name']
        self.description = data['Description']
        self.image_name = data['ImageName']
        self.current_version_number = data['CurrentVersionNumber']
        self.current_version = InventionVersion(data['CurrentVersion'])
        self.accessibility = ACCESSIBILITY_DICT.get(data['Accessibility'], 'Unknown')
        self.is_published = data['IsPublished']
        self.is_featured = data['IsFeatured']
        self.modified_at = date_to_unix(data['ModifiedAt'])
        self.created_at = date_to_unix(data['CreatedAt'])
        self.first_published_at = date_to_unix(data['FirstPublishedAt'])
        self.creation_room_id = data['CreationRoomId']
        self.num_players_have_used_in_room = data['NumPlayersHaveUsedInRoom']
        self.num_downloads = data['NumDownloads']
        self.cheer_count = data['CheerCount']
        self.creator_permission = INVENTION_PERMISSION_DICT.get(data['CreatorPermission'], 'Unknown')
        self.general_permission = INVENTION_PERMISSION_DICT.get(data['GeneralPermission'], 'Unknown')
        self.is_ag_invention = data['IsAGInvention']
        self.is_certified_invention = data['IsCertifiedInvention']
        self.price = data['Price']
        self.allow_trial = data['AllowTrial']
        self.hide_from_player = data['HideFromPlayer']

    async def get_creator_player(self, force: bool = False) -> 'Account':
        """
        Fetches the creator of this invention. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: An account object.
        """
        if self.creator_player is None or force:
            self.creator_player = await self.client.accounts.fetch(self.creator_player_id)
        return self.creator_player

    async def get_creation_room(self, include: int = 0, force: bool = False) -> 'Room':
        """
        Fetches the room this invention was created in. Returns a
        cached result, if this function has been already called.

        Include param values:
        - +2 = Subrooms
        - +4 = Roles
        - +8 = Tags
        - +32 = Promotional content
        - +64 = Scores
        - +256 = Loading screens

        :param include: An integer that add additional information to the response.
        :param force: If true, fetches new data.
        :return: A room object.
        """
        if self.creation_room is None or force:
            self.creation_room = await self.client.rooms.fetch(self.creation_room_id, include)
        return self.creation_room

    async def get_tags(self, force: bool = False) -> List['Tag']:
        """
        Fetches the tags for this invention. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data
        :return: A list of tag objects.
        """
        if self.tags is None or force:
            data: 'Response[List[TagResponse]]' = await self.rec_net.api.inventions.v1.details.make_request('get', params = {'inventionId': self.id})
            self.tags = Tag.create_from_list(data.data["Tags"])
        return self.tags







    