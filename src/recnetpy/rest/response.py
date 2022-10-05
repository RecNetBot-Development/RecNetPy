from typing import Generic, TypeVar

RT = TypeVar('RT')

class Response(Generic[RT]):
    """
    A small data class to hold the status and
    data from an http request.
    """
    status: int
    success: bool
    data: RT

    def __init__(self, status: int, success: bool, data: RT) -> None:
        self.status = status
        self.success = success
        self.data = data