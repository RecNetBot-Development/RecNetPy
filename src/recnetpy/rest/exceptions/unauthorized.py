from typing import TYPE_CHECKING

from . import HTTPError

if TYPE_CHECKING:
    from .. import Response

class Unauthorized(Exception):
    """
    An exception raised for 401 HTTP error.
    """

    def __init__(self, resp: 'Response') -> None:
        message = "You aren't authorized to access this rousource. Please verify you entered the correct api key."
        super().__init__(resp, message)