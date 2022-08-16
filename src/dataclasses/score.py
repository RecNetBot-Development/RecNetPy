from typing import Optional

from . import Room
from ..misc import VariableClass
from ..misc.api_responses import ScoreResponse

class Score(VariableClass[ScoreResponse]):
    """
    This class represents a room's score on a particular 
    platform. Not much is understood about what the score
    means.
    """
    room_id: int
    visit_type: int
    score: int
    backup_score: Optional[int]
    room: Room

    def __init__(self, data: ScoreResponse) -> None:
        self.room_id = data['RoomId']
        self.visit_type = data['VisitType']
        self.score = data['Score']
        self.backup_score = data['BackupScore']