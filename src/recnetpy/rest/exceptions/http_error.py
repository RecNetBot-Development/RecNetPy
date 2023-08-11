from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import Response

class HTTPError(Exception):
    """
    This class represents an error or problem with a request.
    """

    def __init__(self, resp: 'Response', msg: str = "No Info.") -> None:
        error_message = f"Info: {msg}\n" \
                        f"URL: {resp.url}\n" \
                        f"Status: {resp.status}\n" \
                        f"Data: \n{resp.data}"
        super().__init__(error_message)