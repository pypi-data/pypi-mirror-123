from asyncio import run, sleep
from logging import getLogger
from multiprocessing import Process as BaseProcess
from multiprocessing import Value
from typing import Optional
from uuid import uuid4

logger = getLogger(__name__)


class Process(BaseProcess):
    def __init__(
        self,
        name: str,
        *,
        period: Optional[float] = 1.0,
        **kwargs,
    ):
        self.name = name
        self.period = period
        self.is_active = Value("b", 1)

        super().__init__(name=name, args=(self.is_active,), kwargs=kwargs)

    def start(self):
        super().start()

    def stop(self):
        self.is_active.value = 0
        self.join()

    def run(self):
        try:
            run(self._run())
        except BaseException:
            logger.exception(f"Exception in process {self.name} loop.")

    async def _run(self):
        # Getting multiprocess parameters.
        self.is_active = self._args[0]

        for name, value in self._kwargs.items():
            setattr(self, name, value)

        # Start.
        await self._on_start()
        logger.debug(f"Process id {self.pid}, name {self.name} started.")

        # Running.
        await self._loop()

        # Stop.
        await self._on_stop()
        logger.debug(f"Process id {self.pid}, name {self.name} stopped.")

    async def _loop(self):
        while self.is_active.value:
            try:
                await self._activity()
            except BaseException:
                logger.exception(
                    f"Exception while running process id {self.pid}, name {self.name}.",
                )

            await sleep(self.period)

    async def _on_start(self):
        pass

    async def _on_stop(self):
        pass

    async def _activity(self):
        pass


class WorkerProcess(Process):
    def __init__(
        self,
        function: callable,
        *,
        name: Optional[str] = None,
        period: Optional[float] = None,
    ):
        if name is None:
            name = f"worker {format(uuid4().hex)}"

        if period is None:
            period = 1.0

        super().__init__(name=name, period=period)
        self.function = function

    async def _activity(self):
        await self.function()
