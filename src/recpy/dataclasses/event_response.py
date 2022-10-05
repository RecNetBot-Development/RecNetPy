from typing import TYPE_CHECKING, Dict, Optional

from ..misc import date_to_unix, VariableClass

if TYPE_CHECKING:
    from . import Account
    from ..misc.api_responses import EventResponseResponse

RESPONSE_TYPE_DICT: Dict[int, str] = {
    0: 'Attending',
    1: 'May Attend',
    2: 'Not Attending'
}

class EventInteraction(VariableClass['EventResponseResponse']):
    """
    This class represents a user's interaction with an event.
    """
    player_event_id: int
    player_id: int
    created_at: int
    type: str
    player: Optional['Account']

    def __init__(self, data: 'EventResponseResponse') -> None:
        self.player_event_id = data['PlayerEventId']
        self.player_id = data['PlayerId']
        self.created_at = date_to_unix(data['CreatedAt'])
        self.type = RESPONSE_TYPE_DICT.get(data['Type'], "Unknown")