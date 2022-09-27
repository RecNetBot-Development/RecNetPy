from typing import TypeVar, Optional, Generic
from abc import ABC, abstractmethod

from asyncio import Lock

RT = TypeVar('RT')

class ThreadTask(ABC, Generic[RT]):
    """
    This class represents a task to be executed inside an AsyncThread. 
    It is ONLY to be inherited, and the function run is required to be defined.
    The ThreadTask.lock must be acquired before submitting it to a thread.
    """

    lock: Lock
    result: Optional[RT]
  
    def __init__(self):
        self.lock = Lock()
        self.result = None

    async def execute(self) -> None:
        """
        Called inside an AsyncThread. It executes the run method, 
        and frees the tasks lock. The data returned by the run
        method is set to the result property.
        """
        try:
            self.result = await self.run()
        finally:
            self.lock.release()

    async def get_result(self) -> Optional[RT]:
        """
        It returns the result of the execution. Blocks if 
        the tasks underlying lock isn't freed, or returns
        immediately. May cause unexpected behaviour if not
        submitted to a pool.

        @return: Returns the value returned from the run method.
        """
        if self.lock.locked():
            await self.lock.acquire()
        return self.result

    @abstractmethod
    async def run() -> RT:
        """
        This is the function to be executed within the
        thread. This function must be defined in the 
        inheriting class.
        """
        pass