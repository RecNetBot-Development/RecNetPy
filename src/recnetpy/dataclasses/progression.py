from typing import TYPE_CHECKING

from ..misc import VariableClass

if TYPE_CHECKING:
    from ..misc.api_responses import ProgressionResponse

class Progression(VariableClass['ProgressionResponse']):
    """
    This class represents a players current level.
    """
    player_id: int
    level: int
    xp: int

    def __init__(self, data: 'ProgressionResponse'):
        self.player_id = data['PlayerId']
        self.level = data['Level']
        self.xp = data['XP']