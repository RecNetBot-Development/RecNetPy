from typing import TYPE_CHECKING

from . import HTTPError

if TYPE_CHECKING:
    from .. import Response

class BadRequest(HTTPError):
    """
    An exception for a 400 HTTP error.
    """

    def __init__(self, resp: 'Response'):
        message = "Bad request, make sure your input is valid!"
        super().__init__(resp, message)