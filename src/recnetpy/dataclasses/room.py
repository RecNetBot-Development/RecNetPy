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

ROOM_MODERATION_STATE: Dict[int, str] = {
    0: "Active",
    11: "Junior Pending",
    100: "Moderation Pending",
    101: "Moderation Closed",
    102: "Moderation Banned",
    255: "Marked For Delete"
}

MAX_PLAYER_CALCULATION_MODE: Dict[int, str] = {
    0: "All Subrooms",
    1: "Only Entry Subrooms"
}

WARNING_MASK_LIST: List[str] = ["Spooky/scary themes", "Mature themes", "Bright/flashing lights", "Intense motion", "Gore/violence", "Custom"]

class Room(BaseDataClass['RoomResponse']):
    """
    This class represents a player created room.
    """

    #: This is a room's unique identifier.
    id: int
    #: If true this room is a player's dorm.
    is_dorm: int
    #: Determines how the max number of players is calculated which has the possible values ``['All Subrooms', 'Only Entry Subrooms']``. 
    max_player_calculation_mode: str
    #: This is the max number of players allowed to join the room.
    max_players: int
    #: If true players can clone this room.
    cloning_allowed: bool
    #: If true mic auto mute is disabled.
    disable_mic_auto_mute: bool
    #: If true room comments are disabled.
    disable_room_comments: bool
    #: If true voice chat is encrypted
    encrypted_voice_chat: bool
    #: If true the room uses voice moderation.
    voice_moderated: bool
    #: If true the load screen is locked.
    load_screen_locked: bool
    #: This is the name of the room.
    name: str
    #: This is the room's description.
    description: str
    #: This is the file name of the rooms thumbnail.
    image_name: Optional[str]
    #: This is a list of warnings for the room that can have any of these possible valuess ``["Custom", "Spooky/scary themes", "Mature themes", "Bright/flashing lights", "Intense motion", "Gore/violence"]``
    warnings: List[str]
    #: This is a custom warning for the room.
    custom_warning: Optional[str]
    #: This is the id of the player who created the room.
    creator_account_id: int
    #: This is the current state of the room which has the possible values of ``['Active', 'Junior Pending', 'Moderation Pending', 'Moderation Closed', 'Moderation Banned', 'Marked For Delete']``.
    state: str 
    #: This is the visibilty of the room which has the possible value of ``['Private', 'Public', 'Unlisted']``.
    accessibility: str
    #: If true players can vote on the next level.
    supports_level_voting: bool
    #: If true the room was published by coach.
    is_rro: bool
    #: If true screen mode players can join the room.
    supports_screens: bool
    #: If true walk vr players can join the room.
    supports_walk_vr: bool
    #: If true teleport vr players can join the room.
    supports_teleport_vr: bool
    #: If true vr low players can join the room.
    supports_vr_low: bool
    #: If true Quest 2 players can join the room.
    supports_quest_two: bool
    #: If true mobile players can join the room.
    supports_mobile: bool
    #: If true junior players can join the room.
    supports_juniors: bool
    #: This is the minimum level requried to join the room.
    min_level: int
    #: This is the date the room was created represented as an Unix integer.
    created_at: int
    #: This is the number of players that cheered the room.
    cheer_count: int
    #: This is the number of players who have the room favorited.
    favorite_count: int
    #: This is the number of unique visits the room has.
    visitor_count: int
    #: This in the number of times players have joined the room.
    visit_count: int
    #: This is an account object which represents the player who created the room.
    creator_account: Optional['Account'] = None
    #: This a list of subroom objects which represents the room's subrooms.
    subrooms: Optional[List['SubRoom']] = None
    #: This a list of role objects which represents the room's player roles.
    roles: Optional[List['Role']] = None
    #: This a list of tag objects which represents the room's tags.
    tags: Optional[List['Tag']] = None
    #: This is a list of file names for a room's promotional images. 
    promo_images: Optional[List[str]] = None
    #: This is a list of promotional content objects that represent's a rooms promo content.
    promo_external_content: Optional[List['PromoExternalContent']] = None
    #: This is a list of score objects that represents a room's ranking.
    scores: Optional[List['Score']] = None
    #: This is a list of load screen objects that represents a room's loading screens.
    load_screens: Optional[List['LoadScreen']] = None
    #: This is a list of images that were taken in the room.
    images: Optional[List['Image']] = None
    #: This is a list of events that are happening in the room.
    events: Optional[List['Event']] = None


    def patch_data(self, data: 'RoomResponse') -> None:
        """
        Sets properties corresponding to data for an api room response.

        :param data: Data from the api.
        """
        self.data = data
        self.id = data["RoomId"]
        self.is_dorm = data["IsDorm"]
        self.max_player_calculation_mode = MAX_PLAYER_CALCULATION_MODE.get(data["MaxPlayerCalculationMode"], "Unknown")
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
        self.state = ROOM_MODERATION_STATE.get(data["State"], "Unknown")
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

        # Search for deleted accounts
        deleted = []
        for i in self.roles:
            if not hasattr(i.account, "username"):
                deleted.append(i)

        # Eradicate them
        for i in deleted:
            self.roles.remove(i)

        return self.roles

