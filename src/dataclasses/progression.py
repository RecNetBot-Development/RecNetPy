from . import Account
from ..misc import VariableClass
from ..misc.api_responses import ProgressionResponse

class Progression(VariableClass[ProgressionResponse]):
    """
    This class represents a players current level.
    """
    player_id: int
    level: int
    xp: int
    player: Account

    def __init__(self, data: ProgressionResponse):
        self.player_id = data['PlayerId']
        self.level = data['Level']
        self.xp = data['XP']