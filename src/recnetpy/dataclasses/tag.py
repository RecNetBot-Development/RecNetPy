from typing import TYPE_CHECKING
from ..misc import VariableClass

if TYPE_CHECKING:
    from ..misc.api_responses import TagResponse

class Tag(VariableClass['TagResponse']):
    """
    This class represents a room and invention tag.
    """

    #: This is the name of the tag.
    tag: str
    #: This is the type of tag assignment. 
    type: int

    def __init__(self, data: 'TagResponse') -> None:
        self.tag = data['Tag']
        self.type = data['Type']