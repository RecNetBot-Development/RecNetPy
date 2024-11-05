from typing import TYPE_CHECKING, Optional, Dict

from ..misc import VariableClass

if TYPE_CHECKING:
    from . import Account
    from ..misc.api_responses import RoleResponse

ROLE_DICT: Dict[int, str] = {
    0: None,
    1: "Banned",
    10: "Host",
    20: "Moderator",
    25: "Contributor",
    30: "Co-Owner",
    31: "Temporary Co-Owner",
    255: "Owner"
}

class Role(VariableClass['RoleResponse']):
    """
    This class represents a room's player roles.
    """
    #: This is the id of the role which has the possible values of ``{0: 'None', 10: 'Host', 20: 'Moderator', 30: 'Co-Owner', 31: 'Temporary Co-Owner', 255: 'Owner'}``.
    id: int
    #: This is the id of the player who owns this role.
    account_id: int
    #: This is the name of the role the player owns which has the possible values of ``['None', 'Host', 'Moderator', 'Co-Owner', 'Temporary Co-Owner', Owner']``
    name: str
    #: This is the id of the account who updated the player's role.
    last_changed_by_account_id: Optional[int]
    #: This is the role the player was invited to take.
    invited_role: str
    #: This is an account object which represents the role owner.
    account: Optional['Account']
    #: This is an account object which represents player that updated this role.
    last_changed_by_account: Optional['Account']

    def __init__(self, data: 'RoleResponse') -> None:
        self.id = data["Role"]
        self.account_id = data["AccountId"]
        self.name = ROLE_DICT.get(data["Role"], "Unknown")
        self.last_changed_by_account_id = data["LastChangedByAccountId"]
        self.invited_role = ROLE_DICT.get(data["InvitedRole"])