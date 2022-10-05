from typing import TYPE_CHECKING, Dict

from asyncio import Lock
from aiohttp import ClientSession

from .async_threads import AsyncThreadPool
from .exceptions import HTTPError, BadRequest, InternalServerError

if TYPE_CHECKING:
    from .request import Request
    from .response import Response

class HTTPClient:
    """
    This class is responsible for managing the
    client session, and adding requests to the
    thread pool.
    """
    locks: Dict[str, Lock]
    session: ClientSession
    thread_pool: AsyncThreadPool

    def __init__(self) -> None:
        self.locks = {}
        self.session = ClientSession()
        self.thread_pool = AsyncThreadPool(200) #Allows ONLY 200 connections to be processed at any given time.

    async def push(self, request: 'Request') -> 'Response':
        """
        Creates a lock unique to the request, and 
        adds the request to the thread pool to be
        executed.

        @param request: The request object to be executed.
        @return: Returns a response object. 
        """
        lock = self.locks.get(request.bucket)
        if lock is None:
            lock = Lock()
            self.locks[request.bucket] = lock
        async with lock:
            await self.thread_pool.submit(request)
            result = await request.get_result()
            if result.success or result.status == 404: return result
            match result.status:
                case 400:
                    raise BadRequest
                case 500:
                    raise InternalServerError
                case _:
                    raise HTTPError(result.status, request.url, result.data)
      
    async def stop(self) -> None:
        """
        Stops the thread pool, and closes the
        underlying client connection.
        """
        await self.thread_pool.stop()
        await self.session.close()
