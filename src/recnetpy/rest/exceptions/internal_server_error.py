from typing import TYPE_CHECKING

from . import HTTPError

if TYPE_CHECKING:
    from .. import Response

class InternalServerError(HTTPError):
    """
    An exception for a 500 HTTP error.
    """

    def __init__(self, resp: 'Response'):
        message = "Something went wrong within Rec Room's servers. Make sure your input is valid!"
        super().__init__(resp, message)