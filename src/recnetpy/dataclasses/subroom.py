from typing import TYPE_CHECKING, Optional

from ..misc import VariableClass, date_to_unix
from ..misc.constants import ACCESSIBILITY_DICT

if TYPE_CHECKING:
    from ..misc.api_responses import SubRoomResponse

class SubRoom(VariableClass['SubRoomResponse']):
    """
    This class represents a room's subroom.
    """

    #: If true players are able to join an in-progress game.
    supports_join_in_progress: bool
    #: If true players are matched with others of similat level.
    use_level_based_matchmaking: bool
    #: If true juniors will be matched with juniors, and vice versa.
    use_age_based_matchmaking: bool
    #: If true the match making algorithm used in RecRoyal will be used.
    use_rec_royale_matchmaking: bool
    #: This is a subrooms unique identifier.
    subroom_id: int
    #: This is the id of the room this subroom belongs to.
    room_id: int
    unity_scene_id: str
    #This is the name of the subroom.
    name: str
    #: If true the room is a sandbox..
    is_sandbox: bool
    #: This is the max number of players allowed to join the rooom.
    max_players: int
    #: This is the visibilty of the image which has the possible value of ``['Private', 'Public', 'Unlisted']``.
    accessibility: str
    #: The blob that contains the data
    data_blob: Optional[str]
    #: The user who saved the last
    data_saved_at: Optional[int]
    #: The latest save description for the subroom
    description: Optional[str]

    def __init__(self, data: 'SubRoomResponse'):
        self.supports_join_in_progress = data['SupportsJoinInProgress']
        self.use_level_based_matchmaking = data['UseLevelBasedMatchmaking']
        self.use_age_based_matchmaking = data['UseAgeBasedMatchmaking']
        self.use_rec_royale_matchmaking = data['UseRecRoyaleMatchmaking']
        self.subroom_id = data['SubRoomId']
        self.room_id = data['RoomId']
        #self.unity_scene_id = data['UnitySceneId']
        self.last_moderated_save_moderation_state = data["LastModeratedSaveModerationState"]
        self.name = data['Name']
        #self.data_blob = data.get("DataBlob", None)
        #self.data_saved_at = saved_at
        #self.data_saved_by = saved_by
        #self.description = description
        self.is_sandbox = data['IsSandbox']
        self.max_players = data['MaxPlayers']
        self.accessibility = ACCESSIBILITY_DICT.get(data['Accessibility'])
