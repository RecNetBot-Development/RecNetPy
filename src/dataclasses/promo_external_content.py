from ..misc import VariableClass
from ..misc.api_responses import PromoExternalContentResponse

class PromoExternalContent(VariableClass[PromoExternalContentResponse]):
    """
    This class represent a room's promotional youtube videos.
    """
    type: int
    reference: str

    def __init__(self, data: PromoExternalContentResponse) -> None:
        self.type = data['Type']
        self.type = data['Reference']