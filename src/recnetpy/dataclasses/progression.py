from typing import TYPE_CHECKING

from ..misc import VariableClass

if TYPE_CHECKING:
    from ..misc.api_responses import ProgressionResponse

class Progression(VariableClass['ProgressionResponse']):
    """
    This class represents a players current level.
    """

    #: This is the id for the player who's level this object represents.
    player_id: int
    #: This is the current level of the player:
    level: int
    #: This is how much xp the player has gained since they last leveled up.
    xp: int

    def __init__(self, data: 'ProgressionResponse'):
        self.player_id = data['PlayerId']
        self.level = data['Level']
        self.xp = data['XP']