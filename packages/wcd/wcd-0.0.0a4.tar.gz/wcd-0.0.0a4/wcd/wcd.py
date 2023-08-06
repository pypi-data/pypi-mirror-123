import asyncio as aio
import logging
import coloredlogs
import os

from pathlib import Path
from typing import Awaitable, Callable, TypeVar

from .event import ConnectionMode, DaemonEvent, fire_event
from .funcs import wp_cycler
from .cfg import get_cfg, save_cfg


LOGGER = logging.getLogger(__name__)
coloredlogs.install(level=logging.INFO)


async def _read_int(r: aio.StreamReader) -> int:
    return int.from_bytes(await r.readexactly(4), byteorder="big")


T = TypeVar("T")
U = TypeVar("U")


async def _on_done_waiting(aw: Awaitable[T], cb: Callable[[T], U]) -> U:
    return cb(await aw)


async def _handle_client(r: aio.StreamReader, w: aio.StreamWriter) -> None:

    conn_mode = await _read_int(r)
    peer_name = w.get_extra_info("peername") or "UNIX_CLIENT"

    if conn_mode == ConnectionMode.ONE_SHOT:
        result = await fire_event((etype := await _read_int(r)), r, w)
        LOGGER.info(f"Handled '{DaemonEvent(etype).name}', as requested by '{peer_name}'. Ran {len(result)} handlers.")
        return

    if conn_mode == ConnectionMode.KEEP_CONNECTED:
        # If the client disconnects, this errors out and quits.
        while True: 
            # No need to await here, we can listen for commands
            # while these event handlers are running as bg tasks
            aw = fire_event((etype := await _read_int(r)), r, w)
            aio.create_task(_on_done_waiting(aw, lambda result: LOGGER.info(
                f"Handled '{DaemonEvent(etype).name}', as requested by '{peer_name}'. Ran {len(result)} handlers.")))


async def on_client_connected(r: aio.StreamReader, w: aio.StreamWriter) -> None:

    peer_name = w.get_extra_info("peername") or "UNIX_CLIENT"
    LOGGER.info(f"'{peer_name}' connected")

    try:
        await _handle_client(r, w)
    except (aio.IncompleteReadError, IndexError):
        pass

    w.close()
    await w.wait_closed()

    LOGGER.info(f"'{peer_name}' disconnected")


async def wcd():

    if "TMPDIR" not in os.environ:
        os.environ["TMPDIR"] = "/tmp"
        LOGGER.info("Setting missing variable '$TMPDIR' to '/tmp'")

    path = Path(os.path.expandvars(get_cfg()["socket_path"]))
    os.makedirs(path.parent, exist_ok=True)

    server = await aio.start_unix_server(on_client_connected, path=path)
    aio.create_task(wp_cycler())

    async with server:
        LOGGER.info("Started serving")
        await server.serve_forever()


def main() -> None:
    try:
        aio.run(wcd())
    except KeyboardInterrupt:
        LOGGER.info("Received 'KeyboardInterrupt'. Quitting...")


if __name__ == "__main__":
    main()

