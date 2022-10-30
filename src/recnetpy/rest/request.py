from typing import TypeVar, Dict, Optional, Union, List
from aiohttp import ClientSession, ClientResponse
from .async_threads import ThreadTask
from .response import Response

async def parse_response(resp: ClientResponse) -> Union[str, Dict, List]:
    """
    Parses client response data. 

    @param resp: A client response from a request.
    @return: Json data parsed in to a dictionary or list. Returns as string by default.
    """
    if resp.content_type == 'application/json':
        return await resp.json()
    return await resp.text()

class Request(ThreadTask[Response]):
    """
    This class encapsulates a request to be executed inside of a
    thread pool.
    """
    client: ClientSession
    url: str
    method: str
    params: Optional[Dict]
    body: Optional[Dict]
    headers: Optional[Dict]

    def __init__(self, client: ClientSession, method: str, url: str, params: Optional[Dict] = None, body: Optional[Dict] = None, headers: Optional[Dict] = None) -> None:
        super().__init__()
        self.client = client
        self.method = method
        self.url = url
        self.params = params
        self.body = body
        self.headers = headers

    async def run(self) -> Response:
        """
        This function is to be executed within a thread. It makes a
        request, and parses the response into a custom response object.

        @return: A response object containing the fetched data.
        """
        async with self.client.request(self.method, self.url, data = self.body, params = self.params, headers = self.headers) as response:
            data = await parse_response(response)
            return Response(response.status, response.ok, data)

    @property
    def bucket(self) -> str:
        """
        Represents the request and its componets as astring.

        @return: The request as a string. 
        """
        return f"{self.url}:{self.params}:{self.body}"