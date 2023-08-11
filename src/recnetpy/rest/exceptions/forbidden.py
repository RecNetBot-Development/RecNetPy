from typing import TYPE_CHECKING

from . import HTTPError

if TYPE_CHECKING:
    from .. import Response

class Forbidden(HTTPError):
    """
    An exception raised for 403 HTTP error.
    """

    def __init__(self, resp: 'Response') -> None:
        message = "You do not have permission to access this resource!"
        super().__init__(resp, message)
