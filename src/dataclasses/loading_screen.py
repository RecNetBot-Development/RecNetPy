from typing import Optional, List, TypedDict

from ..misc import VariableClass
from ..misc.api_responses import LoadScreenResponse

class LoadScreen(VariableClass[LoadScreenResponse]):
    """
    This class represents the data for a room loading screen.
    """
    image_name: str
    title: Optional[str]
    subtitle: Optional[str]

    def __init__(self, data: LoadScreenResponse):
        self.image_name = data['ImageName']
        self.title = data['Title']
        self.subtitle = data['Subtitle']

