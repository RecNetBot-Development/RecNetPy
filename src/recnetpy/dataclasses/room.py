from typing import TYPE_CHECKING, List, Optional, Dict

from .base import BaseDataClass
from .subroom import SubRoom
from .role import Role
from .tag import Tag
from .promo_external_content import PromoExternalContent
from .score import Score
from .loading_screen import LoadScreen
from ..misc import bitmask_decode, date_to_unix
from ..misc.constants import ACCESSIBILITY_DICT

if TYPE_CHECKING:
    from . import Account, Image, Event
    from ..misc.api_responses import RoomResponse, AccountResponse
    from ..rest import Response


WARNING_MASK_LIST: List[str] = ["Custom", "Spooky/scary themes", "Mature themes", "Bright/flashing lights", "Intense motion", "Gore/violence"]

class Room(BaseDataClass['RoomResponse']):
    """
    This class represents a player created room.
    """
    id: int
    is_dorm: int
    max_player_calculation_mode: int
    max_players: int
    cloning_allowed: bool
    disable_mic_auto_mute: bool
    disable_room_comments: bool
    encrypted_voice_chat: bool
    voice_moderated: bool
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
    creator_account: Optional['Account'] = None
    subrooms: Optional[List['SubRoom']] = None
    roles: Optional[List['Role']] = None
    tags: Optional[List['Tag']] = None
    promo_images: Optional[List[str]] = None
    promo_external_content: Optional[List['PromoExternalContent']] = None
    scores: Optional[List['Score']] = None
    load_screens: Optional[List['LoadScreen']] = None
    images: Optional[List['Image']] = None
    events: Optional[List['Event']] = None


    def patch_data(self, data: 'RoomResponse') -> None:
        """
        Sets properties corresponding to data for an api room response.

        :param data: Data from the api.
        """
        self.id = data["RoomId"]
        self.is_dorm = data["IsDorm"]
        self.max_player_calculation_mode = data["MaxPlayerCalculationMode"]
        self.max_players = data["MaxPlayers"]
        self.cloning_allowed = data["CloningAllowed"]
        self.disable_mic_auto_mute = data["DisableMicAutoMute"]
        self.disable_room_comments = data["DisableRoomComments"]
        self.encrypted_voice_chat = data["EncryptVoiceChat"]
        self.voice_moderated = data["ToxmodEnabled"]
        self.load_screen_locked = data["LoadScreenLocked"]
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

    async def get_images(self, take: int = 16, skip: int = 0, sort: int = 0, force: bool = False) -> List['Image']:
        """
        Fetches a list of images taken in this room. Returns a
        cached result, if this function has been already called.

        :param take: The number of results to return.
        :param skip: The number of results to skip.
        :param sort: An integer that describes how the results are to be sorted 
        :param force: If true, fetches new data.
        :return: A list of images.
        """
        if self.images is None or force:
            self.images = await self.client.images.in_room(self.id, take = take, skip = skip, sort = sort)
        return self.images

    async def get_events(self, take: int = 16, skip: int = 0, force: bool = False) -> List['Event']:
        """
        Fetches a list of events happening in this room. Returns a
        cached result, if this function has been already called.

        :param take: The number of results to return.
        :param skip: The number of results to skip.
        :param force: If true, fetches new data.
        :return: A list of events.
        """
        if self.events is None or force:
            self.events = await self.client.events.in_room(self.id, take = take, skip = skip)
        return self.events

    async def get_creator_player(self, force: bool = False) -> 'Account':
        """
        Fetches the creator of the room. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: An account object.
        """
        if self.creator_account is None or force:
            self.creator_account = await self.client.accounts.fetch(self.creator_account_id)
        return self.creator_account

    async def resolve_role_owners(self) -> Optional[List['Role']]:
        """
        Resolves the role owner for this room. This function
        will make an api call every time its used. It should only be used when 
        updating the role account attribute.

        :return: A list of role objects, or None if roles is None 
        """
        if self.roles is None: return None
        roles = self.roles
        accounts: Dict[int, Account] = {}
        for role in roles:
            account = self.client.accounts.create_dataclass(role.account_id)
            role.account = account
            accounts[role.account_id] = account
        data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.account.bulk.make_request('post', body = {"id": accounts.keys()})
        for data_response in data.data: accounts.get(data_response['accountId']).patch_data(data_response)
        return self.roles

