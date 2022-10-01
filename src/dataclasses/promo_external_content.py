from typing import TYPE_CHECKING

from ..misc import VariableClass

if TYPE_CHECKING:
    from ..misc.api_responses import PromoExternalContentResponse

class PromoExternalContent(VariableClass['PromoExternalContentResponse']):
    """
    This class represent a room's promotional youtube videos.
    """
    type: int
    reference: str

    def __init__(self, data: 'PromoExternalContentResponse') -> None:
        self.type = data['Type']
        self.reference = data['Reference']