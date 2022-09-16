import asyncio
import logging

import uvicorn

from internal.api import app as app_fastapi
from internal.scheduler import app as app_rocketry


class Server(uvicorn.Server):
    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    server = Server(config=uvicorn.Config(app_fastapi, workers=1, loop="asyncio", port=8001))

    api = asyncio.create_task(server.serve())
    scheduler = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([scheduler, api])


if __name__ == "__main__":
    logger = logging.getLogger("rocketry.task")
    logger.addHandler(logging.StreamHandler())

    asyncio.run(main())
