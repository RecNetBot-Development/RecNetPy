from typing import List, Optional

from . import BaseDataClass, Account, SubRoom, Role, Tag, PromoExternalContent, Score, LoadScreen
from ..misc import bitmask_decode, date_to_unix
from ..misc.api_responses import RoomResponse
from ..misc.constants import ACCESSIBILITY_DICT

WARNING_MASK_LIST: List[str] = ["Custom", "Spooky/scary themes", "Mature themes", "Bright/flashing lights", "Intense motion", "Gore/violence"]

class Room(BaseDataClass[RoomResponse]):
    """
    This class represents a player created room.
    """
    is_dorm: int
    max_player_calculation_mode: int
    max_players: int
    cloning_allowed: bool
    disable_mic_auto_mute: bool
    disable_room_comments: bool
    encrypted_voice_chat: bool
    load_screen_locked: bool
    version: int
    name: str
    description: str
    image_name: Optional[str]
    warnings: List[str]
    custom_warning: Optional[str]
    creator_account_id: int
    state: int
    accessibility: str
    supports_level_voting: bool
    is_rro: bool
    supports_screens: bool
    supports_walk_vr: bool
    supports_teleport_vr: bool
    supports_vr_low: bool
    supports_quest_two: bool
    supports_mobile: bool
    supports_juniors: bool
    min_level: int
    created_at: int
    cheer_count: int
    favorite_count: int
    visitor_count: int
    visit_count: int
    creator_account: Optional[Account]
    subrooms: Optional[List[SubRoom]]
    roles: Optional[List[Role]]
    tags: Optional[List[Tag]]
    promo_images: Optional[List[str]]
    promo_external_content: Optional[List[PromoExternalContent]]
    scores: Optional[List[Score]]
    load_screens: Optional[List[LoadScreen]]

    def patch_data(self, data: RoomResponse) -> None:
        """
        Sets properties corresponding to data for an api room response.

        @param data: Data from the api.
        """
        self.is_dorm = data["IsDorm"]
        self.max_player_calculation_mode = data["MaxPlayerCalculationMode"]
        self.max_players = data["MaxPlayers"]
        self.cloning_allowed = data["CloningAllowed"]
        self.disable_mic_auto_mute = data["DisableMicAutoMute"]
        self.disable_room_comments = data["DisableRoomComments"]
        self.encrypted_voice_chat = data["EncryptVoiceChat"]
        self.load_screen_locked = data["LoadScreenLocked"]
        self.version = data["Version"]
        self.name = data["Name"]
        self.description = data["Description"]
        self.image_name = data["ImageName"]
        self.warnings = bitmask_decode(data["WarningMask"], WARNING_MASK_LIST)
        self.custom_warning = data["CustomWarning"]
        self.creator_account_id = data["CreatorAccountId"]
        self.state = data["State"]
        self.accessibility = ACCESSIBILITY_DICT.get(data["Accessibility"], "Unknown")
        self.supports_level_voting = data["SupportsLevelVoting"]
        self.is_rro = data["IsRRO"]
        self.supports_screens = data["SupportsScreens"]
        self.supports_walk_vr = data["SupportsWalkVR"]
        self.supports_teleport_vr = data["SupportsTeleportVR"]
        self.supports_vr_low = data["SupportsVRLow"]
        self.supports_quest_two = data["SupportsQuest2"]
        self.supports_mobile = data["SupportsMobile"]
        self.supports_juniors = data["SupportsJuniors"]
        self.min_level = data["MinLevel"]
        self.created_at = date_to_unix(data["CreatedAt"])
        self.cheer_count = data["Stats"]["CheerCount"]
        self.favorite_count = data["Stats"]["FavoriteCount"]
        self.visitor_count = data["Stats"]["VisitorCount"]
        self.visit_count = data["Stats"]["VisitCount"]
        self.subrooms = SubRoom.create_from_list(data.get("SubRooms"))
        self.roles = Role.create_from_list(data.get("Roles"))
        self.tags = Tag.create_from_list(data.get("Tags"))
        self.promo_images = data.get("PromoImages")
        self.promo_external_content = PromoExternalContent.create_from_list(data.get("PromoExternalContent"))
        self.scores = Score.create_from_list(data.get("Scores"))
        self.load_screens = LoadScreen.create_from_list(data.get("LoadScreens"))        
