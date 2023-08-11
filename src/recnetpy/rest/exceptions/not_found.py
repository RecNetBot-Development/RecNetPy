from typing import TYPE_CHECKING

from . import HTTPError

if TYPE_CHECKING:
    from .. import Response

class NotFound(HTTPError):
    """
    An exception for a 404 HTTP error.
    """

    def __init__(self, resp: 'Response'):
        message = "The data you were looking for can't be found! It either doesn't exist or is private."
        super().__init__(resp, message)