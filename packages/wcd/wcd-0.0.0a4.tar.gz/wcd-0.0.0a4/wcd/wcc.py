import asyncio as aio
import argparse as ap
import sys
import os

from pathlib import Path
from typing import Optional

from .cfg import get_cfg
from .event import ConnectionMode, DaemonEvent


def get_args() -> ap.Namespace:

    parser = ap.ArgumentParser(description="Send commands to a wcd instance, through a unix socket.")

    parser.add_argument("command", choices=[e.name.lower() for e in DaemonEvent],
        help="A command to be sent to the wcd server")
    parser.add_argument("-s", "--socket", default=None, type=Path, 
        help="The path to the unix socket over which to communicate with the server. If this option"
        " is not supplied, wcc will look for this path inside wcd's config file.")

    return parser.parse_args()


# tbf this didnt need to be async, but ive never used synchronous unix sockets
async def wcc(command: str, socket: Optional[Path]) -> None:

    if "TMPDIR" not in os.environ:
        os.environ["TMPDIR"] = "/tmp"
    socket_path = socket or os.path.expandvars(get_cfg()["socket_path"])

    try:
        r, w = await aio.open_unix_connection(socket_path)
    except ConnectionRefusedError:
        print(f"Couldn't connect to a wcd over '{socket_path}'")
        return

    w.write(ConnectionMode.ONE_SHOT.to_bytes(4, byteorder="big"))
    w.write(DaemonEvent[command.upper()].to_bytes(4, byteorder="big"))
    await w.drain()

    print((await r.read()).decode("utf-8"))


def main() -> None:
    aio.run(wcc(**vars(get_args())))


if __name__ == "__main__":
    main()

