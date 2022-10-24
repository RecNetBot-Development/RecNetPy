from typing import TYPE_CHECKING, Dict
from ..misc import VariableClass

if TYPE_CHECKING:
    from ..misc.api_responses import TagResponse

TAG_TYPE: Dict[int, str] = {
    0: "General",
    1: "Auto",
    2: "AG Only",
    3: "Banned"
}

class Tag(VariableClass['TagResponse']):
    """
    This class represents a room and invention tag.
    """

    #: This is the name of the tag.
    tag: str
    #: This is the type of tag assignment which has the possible value of ``['General', 'Auto', 'AG Only', 'Banned']``. 
    type: str

    def __init__(self, data: 'TagResponse') -> None:
        self.tag = data['Tag']
        self.type = TAG_TYPE.get(data['Type'], "Unknown")