from typing import TYPE_CHECKING, Dict
from math import floor

from asyncio import Lock, get_running_loop, AbstractEventLoop, sleep
from aiohttp import ClientSession, TCPConnector

from .exceptions import *

if TYPE_CHECKING:
    from .request import Request
    from .response import Response
    
#10,000/hr = 166/min
RATE_LIMIT = 166
TICK_INTERVAL = 60

def verify_status(resp: 'Response'):
    match resp.status:
        case 200:
            ...
        case 400:
            raise BadRequest(resp)
        case 401:
            raise Unauthorized(resp)
        case 403:
            if resp.headers.get("retry-after"):
                raise RateLimited(resp)
            raise Forbidden(resp)
        case 404:
            #raise NotFound(resp)
            ...
        case 500:
            raise InternalServerError(resp)
        case _:
            raise HTTPError(resp)


class HTTPClient:
    """
    This class is responsible for managing the
    client session, and adding requests to the
    thread pool.
    """
    session: ClientSession
    api_key: str
    rate_limit: int
    remaining_limit: int
    next_tick: float
    tick_offset: float
    __loop: AbstractEventLoop
    __sleep: Lock
    

    def __init__(self, api_key: str) -> None:
        connector = TCPConnector(limit=100)
        self.session = ClientSession(connector=connector)
        self.__sleep = Lock()
        self.__loop = get_running_loop()
        self.api_key = api_key
        self.rate_limit = RATE_LIMIT
        self.tick_offset = self.__loop.time() % 1
        self.reset_limit()

    def reset_limit(self):
        self.next_tick = floor(self.__loop.time() + TICK_INTERVAL) + self.tick_offset
        self.remaining_limit = self.rate_limit
        
    async def push(self, request: 'Request') -> 'Response':
        """
        Creates a lock unique to the request, and 
        adds the request to the thread pool to be
        executed.

        @param request: The request object to be executed.
        @return: Returns a response object. 
        """
        async with self.__sleep:
            t = self.__loop.time()
            if t >= self.next_tick: self.reset_limit()
            if self.remaining_limit <= 0:
                await sleep(self.next_tick - t)
                self.reset_limit()
            request.send()
            self.remaining_limit -= 1
        resp = await request.get_result()
        verify_status(resp)
        return resp


      
    async def stop(self) -> None:
        """
        Stops the thread pool, and closes the
        underlying client connection.
        """
        await self.session.close()
