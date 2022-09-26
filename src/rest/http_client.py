from typing import Dict
from aiohttp import ClientSession
from asyncio import Lock
from .response import Response

class HTTPClient():
    __locks: Dict[str, Lock]
    __session: aiohttp.ClientSession

    def __init__(self) -> None:
        self.__locks = {}
        self.__session = ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    async def push(self, Request):
        lock = self.__locks.get(Request.bucket)
        if lock is None:
            lock = Lock()
            self.__locks[Request.bucket] = lock
        async with lock:
            return await self.execute(Request)

    async def execute(self, Request):
        kwargs = {}
        if Request.body is not None: kwargs["data"] = Request.body
        if Request.params is not None: kwargs["params"] = Request.params

        async with self.__session.request(Request.method, Request.url, **kwargs) as res:
            ResponseData = await Response.parse_response(res)
            return ResponseData
        
    async def close(self):
        await self.__session.close()
