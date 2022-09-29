from typing import List

from asyncio import Queue, gather

from .async_thread import AsyncThread
from .thread_task import ThreadTask

class AsyncThreadPool:
    """
    This class creates and manages AsyncThreads in
    a pool.
    """
    max_threads: int
    active_threads: List[AsyncThread]
    queue: Queue[ThreadTask]
  
    def __init__(self, max_threads: int, start: bool = True):
        self.max_threads = max_threads
        self.queue = Queue()
        self.active_threads = []
        if start: self.start() #Auto start the thread by default.

    def start(self) -> None:
        """
        Initializes the max number of specified threads.
        """
        for _ in range(self.max_threads): self.active_threads.append(AsyncThread(self.queue))

    async def submit(self, task: ThreadTask) -> None:
        """
        Adds a task to be executed, and locks the task's lock. 
        """
        await task.lock.acquire() #Can't be done at initialization.
        self.queue.put_nowait(task)

    async def stop(self) -> None:
        """
        Waits for the queue to become empty, and cancels
        all active threads.
        """
        if self.queue.qsize() > 0: 
            await self.queue.join() #Blocks indefinitely if qsize is zero. 
        for thread in self.active_threads: thread.stop()
        await gather(*[thread.task for thread in self.active_threads], return_exceptions = True)