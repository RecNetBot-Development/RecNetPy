from typing import Generic, TypeVar, Dict

RT = TypeVar('RT')

class Response(Generic[RT]):
    """
    A small data class to hold the status and
    data from an http request.
    """
    url: str
    status: int
    success: bool
    headers: dict
    data: RT

    def __init__(self, url: str, status: int, success: bool, headers: Dict, data: RT) -> None:
        self.url = url
        self.status = status
        self.success = success
        self.headers = headers
        self.data = data