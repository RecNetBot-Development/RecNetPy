from typing import Dict, Optional

from src.dataclasses import invention_version

from . import BaseDataClass, Account, Room, InventionVersion
from ..misc import date_to_unix
from ..misc.api_responses import InventionResponse
from ..misc.constants import ACCESSIBILITY_DICT

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

class Invention(BaseDataClass[InventionResponse]):
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
    creator_permission: int
    general_permission: int
    is_ag_invention: bool
    is_certified_invention: bool
    price: int
    allow_trial: bool
    hide_from_player: bool
    creator_player: Optional[Account]
    creation_room: Optional[Room]

    def patch_data(self, data: InventionResponse) -> None:
        """
        Sets properties corresponding to data for an api room response.

        @param data: Data from the api.
        """
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