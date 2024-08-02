import asyncio
import json
from asyncio import AbstractEventLoop
from typing import NoReturn

from twitchio import Message
from twitchio.ext import commands
from websockets import WebSocketServerProtocol, broadcast, serve

from chat_ws.constants import ACCESS_TOKEN, PORT


class Bot(commands.Bot):
    """Bot responsible for handling all the work."""

    def __init__(self, loop: AbstractEventLoop) -> None:
        """Prepare the bot with the same loop as the one that'll be used to execute it."""
        self.__sockets: set[WebSocketServerProtocol] = set()

        super().__init__(
            token=ACCESS_TOKEN, prefix="!", initial_channels=["thatsrb2dude"], loop=loop
        )

    async def event_ready(self) -> None:
        """Print an info message."""
        print(f"Ready. Logged in as {self.nick}.")

    async def event_message(self, message: Message) -> None:
        """Broadcast the message to all listeners."""
        print(f" {message.author.name}: {message.content}")

        data = {
            "author": message.author.display_name,
            "content": message.content,
            "is_mod": message.author.is_mod,
        }

        broadcast(self.__sockets, json.dumps(data))

        return await super().event_message(message)

    async def __initiate_connection(self, websocket: WebSocketServerProtocol) -> None:
        """Add (and remove) the websocket to the list of active consumers."""
        print("Socket opened")

        self.__sockets.add(websocket)

        try:
            async for _ in websocket:
                pass
        finally:
            self.__sockets.remove(websocket)

    async def execute(self) -> NoReturn:
        """Start the process."""
        async with serve(self.__initiate_connection, "", PORT):
            await self.start()


def main() -> None:
    """The main entry point."""
    loop = asyncio.get_event_loop()
    bot = Bot(loop)
    loop.run_until_complete(bot.execute())


if __name__ == "__main__":
    main()
