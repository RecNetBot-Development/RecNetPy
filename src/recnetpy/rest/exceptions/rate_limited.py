from datetime import timedelta
from typing import TYPE_CHECKING

from . import HTTPError

if TYPE_CHECKING:
    from .. import Response

class RateLimited(HTTPError):
    """
    This exception is raised when the a rate limit is encountered. Raised for a 403 with a retry-after header.
    """

    def __init__(self, resp: 'Response') -> None:
        time_out = resp.headers.get("retry_after")
        t = timedelta(time_out)
        message = f"You're currently being rate limited. Time out expires in {t}."
        super().__init__(resp, message)