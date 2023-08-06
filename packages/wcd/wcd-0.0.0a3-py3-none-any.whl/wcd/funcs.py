import asyncio as aio

from .cfg import get_cfg
from .event import DaemonEvent, register_event
from .wp_cache import WALLPAPER_CACHE


async def _set_wallpaper(wp: str) -> None:
    cmd = get_cfg()["wallpaper_cmd"]
    fdr = get_cfg()["wallpapers_directory"]
    await aio.create_subprocess_shell(f'{cmd} "{fdr}/{wp}"')


@register_event(DaemonEvent.LIST)
async def list_wallpapers(r: aio.StreamReader, w: aio.StreamWriter) -> None:
    w.writelines(bytes(wp, "utf-8") + b'\n' for wp in WALLPAPER_CACHE.wallpapers)
    await w.drain()


@register_event(DaemonEvent.SET)
async def set_wallpaper(r: aio.StreamReader, w: aio.StreamWriter) -> None:
    if (wp := str(await r.readline(), "utf-8")) not in WALLPAPER_CACHE.wallpapers:
        w.write(f"Name '{wp}' does not exist in '{get_cfg()['wallpapers_directory']}'\n".encode("utf-8"))
        await w.drain()
    else:
        await _set_wallpaper(wp)


@register_event(DaemonEvent.GET)
async def get_wallpaper(r: aio.StreamReader, w: aio.StreamWriter) -> None:
    w.write(WALLPAPER_CACHE.curr_wp.encode("utf-8") + b"\n")
    await w.drain()


@register_event(DaemonEvent.NEXT)
async def next_wallpaper(r: aio.StreamReader, w: aio.StreamWriter) -> None:
    wp = WALLPAPER_CACHE.next_wp
    await _set_wallpaper(wp)
    w.write(wp.encode("utf-8") + b"\n")
    await w.drain()


@register_event(DaemonEvent.PREV)
async def prev_wallpaper(r: aio.StreamReader, w: aio.StreamWriter) -> None:
    try:
        wp = WALLPAPER_CACHE.prev_wp
    except IndexError:
        w.write(b"Reached end of history\n")
        await w.drain()
        return
    await _set_wallpaper(wp)
    w.write(wp.encode("utf-8") + b"\n")
    await w.drain()


@register_event(DaemonEvent.TOGGLE_CYCLE)
async def toggle_auto_next(r: aio.StreamReader, w: aio.StreamWriter) -> None:

    if _cycler_event is None:
        w.write(b"Wallpaper cycler is not running yet.")
        await w.drain()
        return

    if _cycler_event.is_set():
        _cycler_event.clear()
        w.write(b"Paused\n")
        await w.drain()
    else:
        _cycler_event.set()
        w.write(b"Resumed\n")
        await w.drain()


@register_event(DaemonEvent.TOGGLE_RANDOM)
async def toggle_random_wallpaper(r: aio.StreamReader, w: aio.StreamWriter) -> None:
    WALLPAPER_CACHE.randomize = not WALLPAPER_CACHE.randomize
    w.write(b"Randomizing\n" if WALLPAPER_CACHE.randomize else b"Not randomizing\n")
    await w.drain()


@register_event(DaemonEvent.SHUFFLE)
async def shuffle_wallpaper_cache(r: aio.StreamReader, w: aio.StreamWriter) -> None:
    WALLPAPER_CACHE.shuffle()


@register_event(DaemonEvent.REFRESH)
async def refresh_wallpaper_cache(r: aio.StreamReader, w: aio.StreamWriter) -> None:
    WALLPAPER_CACHE.refresh()


_cycler_event: aio.Event = None

async def wp_cycler():

    global _cycler_event
    _cycler_event = aio.Event()
    if (wait_time := get_cfg()["time_auto_next"]) > 0:
        _cycler_event.set()

    for wp in WALLPAPER_CACHE:
        await _cycler_event.wait()
        await _set_wallpaper(wp)
        await aio.sleep(wait_time)

