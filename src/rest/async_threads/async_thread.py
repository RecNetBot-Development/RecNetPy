from asyncio import Queue, Task, create_task
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .thread_task import ThreadTask

class AsyncThread:
    """
    This class represents a thread to be contained in an
    AsyncThreadPool.
    """
    queue: Queue['ThreadTask'] #Might throw an error
    task: Task
  
    def __init__(self, queue: Queue, start: bool = True) -> None:
        self.queue = queue
        if start: self.start() #Auto start the thread by default.

    def start(self) -> None:
        """
        Creates the underlying asyncio task for the thread, 
        and executes the run method in that task.
        """
        self.task = create_task(self.run())

    async def stop(self) -> None:
        """
        Attempts to cancel the underlying asyncio task.
        """
        self.task.cancel()
        try:
            await self.task
        except:
            pass
  
    async def run(self) -> None:
        """
        Retrieves a ThreadTask from the queue, and
        executes it. Blocks when the queue is empty.  
        """
        while True:
            task = await self.queue.get()
            await task.execute()
            self.queue.task_done()