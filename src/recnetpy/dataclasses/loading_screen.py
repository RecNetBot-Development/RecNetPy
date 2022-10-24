from typing import TYPE_CHECKING, Optional, List, TypedDict

from ..misc import VariableClass

if TYPE_CHECKING:
    from ..misc.api_responses import LoadScreenResponse    

class LoadScreen(VariableClass['LoadScreenResponse']):
    """
    This class represents the data for a room loading screen.
    """

    #: This is the file name of the load screen image.
    image_name: str
    #: This is the title text that appears on the load screen.
    title: Optional[str]
    #: This is the subtitle of the load scree.
    subtitle: Optional[str]

    def __init__(self, data: 'LoadScreenResponse'):
        self.image_name = data['ImageName']
        self.title = data['Title']
        self.subtitle = data['Subtitle']