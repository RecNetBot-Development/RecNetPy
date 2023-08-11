from typing import Dict, Optional, Union, List, Generic, TypeVar
from aiohttp import ClientSession, ClientResponse
from asyncio import Future

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

RT = TypeVar('RT')

class Request(Generic[RT]):
    """
    This class encapsulates a request to be executed inside of a
    thread pool.
    """
    client: ClientSession
    url: str
    method: str
    attempts: int
    params: Optional[Dict]
    body: Optional[Dict]
    headers: Optional[Dict]
    result: Optional[Response]
    __future: Optional[Future]

    def __init__(self, client: ClientSession, method: str, url: str, params: Optional[Dict] = None, body: Optional[Dict] = None, headers: Optional[Dict] = None) -> None:
        super().__init__()
        self.client = client
        self.method = method
        self.url = url
        self.params = params
        self.body = body
        self.headers = headers
        self.response = None
        self.__future = None

    def send(self) -> Response:
        """
        This function is to be executed within a thread. It makes a
        request, and parses the response into a custom response object.

        @return: A response object containing the fetched data.
        """
        self.attempts = 0
        self.__future = self.make_request()

    async def make_request(self) -> Response:
        """
        This functions attempts to make a request. If an error is 
        encountered the request will be attempted again up to three
        times. Successful attempts will return the requested data as
        a response object.

        @return: A response object containing the fetched data.
        """
        try:
            async with self.client.request(self.method, self.url, data = self.body, params = self.params, headers = self.headers) as response:
                data = await parse_response(response)
                return Response(self.url, response.status, response.ok, response.headers, data)
        except Exception as e:
            self.attempts += 1
            if self.attempts <= 3: return await self.make_request()
            raise e
        
    async def get_result(self):
        """
        It returns the result of the execution. Blocks if 
        the tasks underlying lock isn't freed, or returns
        immediately. May cause unexpected behaviour if not
        submitted to a pool.

        @return: Returns the value returned from the run method.
        """
        if self.__future:
            self.result = await self.__future
            self.__future = None
        return self.result