from typing import TYPE_CHECKING, Optional

from ..misc import VariableClass, date_to_unix
from ..misc.constants import ACCESSIBILITY_DICT

if TYPE_CHECKING:
    from ..misc.api_responses import SubRoomResponse

class SubRoom(VariableClass['SubRoomResponse']):
    """
    This class represents a room's subroom.
    """
    supports_join_in_progress: bool
    use_level_based_matchmaking: bool
    use_age_based_matchmaking: bool
    use_rec_royale_matchmaking: bool
    subroom_id: int
    room_id: int
    unity_scene_id: str
    name: str
    is_sandbox: bool
    max_players: int
    accessibility: str
    data_blob: Optional[str]
    data_saved_at: Optional[int]

    def __init__(self, data: 'SubRoomResponse'):
        self.supports_join_in_progress = data['SupportsJoinInProgress']
        self.use_level_based_matchmaking = data['UseLevelBasedMatchmaking']
        self.use_age_based_matchmaking = data['UseAgeBasedMatchmaking']
        self.use_rec_royale_matchmaking = data['UseRecRoyaleMatchmaking']
        self.subroom_id = data['SubRoomId']
        self.room_id = data['RoomId']
        self.unity_scene_id = data['UnitySceneId']
        self.name = data['Name']
        self.data_blob = data.get("DataBlob", None)
        self.data_saved_at = date_to_unix(data['DataSavedAt']) if 'DataSavedAt' in data else None
        self.is_sandbox = data['IsSandbox']
        self.max_players = data['MaxPlayers']
        self.accessibility = ACCESSIBILITY_DICT.get(data['Accessibility'])
