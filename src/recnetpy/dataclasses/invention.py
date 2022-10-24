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
    #: This is the id of the player who created the invention.
    creator_player_id: int
    #: This is the name of the invention. 
    name: str
    #: This is the description of the invention.
    description: str
    #: This is the file name of the invention thumbnail.
    image_name: str
    #: This is an integer that represents the current version of the invention.
    current_version_number: int
    #: This is an invention version object that represents the current version of the invention.
    current_version: InventionVersion
    #: This is the visibilty of the invention which has the possible value of ``['Private', 'Public', 'Unlisted']``.
    accessibility: str
    #: If true the invention has been published to the store. 
    is_published: bool
    #: If true the invention has been featured.
    is_featured: bool
    #: This is the date the invention was last modified represented as an Unix integer.
    modified_at: int
    #: This is the date the invention was created represented as an Unix integer.
    created_at: int
    #: This is the date the invention was first published to the store represented as an Unix integer.
    first_published_at: int
    #: This is the id of the room the invention was created in.
    creation_room_id: int
    #: This is the number of players who have used the invention in one of their rooms.
    num_players_have_used_in_room: int
    #: This is the number of players who have downloaded the invention.
    num_downloads: int
    #: This is the number of cheers the invention has recieved.
    cheer_count: int
    #: This the permission level of the creator which has the possible values of ``['Unassigned', 'Limited One Use Only', 'Disallow Key Lock', 'Use Only', 'Edit and Save', 'Publish', 'Charge', 'Unlimited']``.
    creator_permission: str
    #: This the general permission level of the invention which has the possible values of ``['Unassigned', 'Limited One Use Only', 'Disallow Key Lock', 'Use Only', 'Edit and Save', 'Publish', 'Charge', 'Unlimited']``.
    general_permission: str
    #: If true this is an invention that is from RecRoomInc.
    is_ag_invention: bool
    #: If true this invention has been certified.
    is_certified_invention: bool
    #: This is the number of tokens required to purchace the invention.
    price: int
    #: If true this invention allows a trial use.
    allow_trial: bool
    #: If true this invention is hidden from the player.
    hide_from_player: bool
    #: This is an account object that represents the player who created the invention.
    creator_player: Optional['Account'] = None
    #: This is a room object that represents the room the invention was created in.
    creation_room: Optional['Room'] = None
    #: This is a list of tag objects that represent the tags of the invention.
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







    