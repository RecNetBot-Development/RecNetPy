class HTTPError(Exception):
    """
    This class represents an error or problem with a request.
    """
    status: int
    url: str
    data: any


    def __init__(self, status: int, url: str, data: any) -> None:
        self.status = status
        self.url = url
        self.data = data
        error_message = f"The request to {url} has failed with code {status}. The following data has been returned: \n {data}"
        super().__init__(error_message)