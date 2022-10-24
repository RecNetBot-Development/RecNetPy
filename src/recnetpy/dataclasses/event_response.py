from typing import TYPE_CHECKING, Dict, Optional

from ..misc import date_to_unix, VariableClass

if TYPE_CHECKING:
    from . import Account
    from ..misc.api_responses import EventResponseResponse

RESPONSE_TYPE_DICT: Dict[int, str] = {
    -1: None,
    0: 'Attending',
    1: 'May Attend',
    2: 'Not Attending',
    3: 'Pending'
}

class EventInteraction(VariableClass['EventResponseResponse']):
    """
    This class represents a user's interaction with an event.
    """

    #: This is the id of the event the player is responding to.
    player_event_id: int
    #: This is the id of the interacting player.
    player_id: int
    #: This is the date the interation happened as an Unix integer.
    created_at: int
    #: This is the type of interation which as the possible values of ``[None, 'Attending', 'May Attend', 'Not Attending', 'Pending']``
    type: str
    #: This an account object that represents the interacting player.
    player: Optional['Account']

    def __init__(self, data: 'EventResponseResponse') -> None:
        self.player_event_id = data['PlayerEventId']
        self.player_id = data['PlayerId']
        self.created_at = date_to_unix(data['CreatedAt'])
        self.type = RESPONSE_TYPE_DICT.get(data['Type'], "Unknown")