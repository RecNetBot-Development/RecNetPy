from typing import TYPE_CHECKING, Dict

from ..misc import VariableClass

if TYPE_CHECKING:
    from ..misc.api_responses import PromoExternalContentResponse

ROOM_PROMO_EXTERNAL_CONTENT_TYPE: Dict[int, str] = {
    0: "YouTube"
}

class PromoExternalContent(VariableClass['PromoExternalContentResponse']):
    """
    This class represent a room's promotional youtube videos.
    """

    #: This is the type of content which is only YouTube right now.
    type: str
    #: This is a part of a url that refers to the location of the content. Usally the last part of a YouTube video.
    reference: str

    def __init__(self, data: 'PromoExternalContentResponse') -> None:
        self.type = ROOM_PROMO_EXTERNAL_CONTENT_TYPE.get(data['Type'], "Unknown")
        self.reference = data['Reference']