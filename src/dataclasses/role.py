from typing import TYPE_CHECKING, Optional, Dict

from ..misc import VariableClass

if TYPE_CHECKING:
    from . import Account
    from ..misc.api_responses import RoleResponse

ROLE_DICT: Dict[int, str] = {
    0: "None",
    10: "Member",
    20: "Moderator",
    30: "Co-Owner",
    255: "Owner"
}

class Role(VariableClass['RoleResponse']):
    """
    This class represents a room's player roles.
    """
    account_id: int
    role: str
    last_changed_by_account_id: Optional[int]
    invited_role: str
    account: Optional['Account']
    last_changed_by_account: Optional['Account']

    def __init__(self, data: 'RoleResponse') -> None:
        self.account_id = data["AccountId"]
        self.role = ROLE_DICT.get(data["Role"], "Unknown")
        self.last_changed_by_account_id = data["LastChangedByAccountId"]
        self.invited_role = ROLE_DICT.get(data["InvitedRole"])