from typing import TYPE_CHECKING, Optional

from ..misc import VariableClass

if TYPE_CHECKING:
    from ..misc.api_responses import ScoreResponse


class Score(VariableClass['ScoreResponse']):
    """
    This class represents a room's score on a particular 
    platform. Not much is understood about what the score
    means.
    """

    #: This is the id of the room the tag belongs to.
    room_id: int
    #: This is possibly the type of the platform for the score.
    visit_type: int
    #: This is the scores value.
    score: int
    #: This is a backup score.
    backup_score: Optional[int]

    def __init__(self, data: 'ScoreResponse') -> None:
        self.room_id = data['RoomId']
        self.visit_type = data['VisitType']
        self.score = data['Score']
        self.backup_score = data['BackupScore']