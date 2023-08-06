import asyncio as aio
import random
import os

from mimetypes import guess_type
from typing import Iterator, Sequence, Any, Optional

from .cfg import get_cfg


def _is_img(file_type: Optional[str]) -> bool:
    return file_type is not None and file_type.startswith("image/")


def _load_wallpapers() -> Iterator[str]:
    for entry in os.scandir(get_cfg()["wallpapers_directory"]):
        if entry.is_file() and _is_img(guess_type(entry.path)[0]):
            yield entry.name


class WallpaperCache:

    def __init__(self, max_history: int=30, randomize: bool=True) -> None:

        self._wallpapers: list[str] = list(_load_wallpapers())
        self.randomize: bool = randomize
        if randomize:
            self.shuffle()
        self._index: int = 0
        self._curr_wp: str = self._wallpapers[self._index]

        self._history: list[str] = []
        self.max_history: int = max_history

    @property
    def wallpapers(self) -> tuple[str, ...]:
        return tuple(self._wallpapers)

    def refresh(self) -> None:
        self._wallpapers = list(_load_wallpapers())

    def shuffle(self) -> None:
        random.shuffle(self._wallpapers)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_wp

    @property
    def curr_wp(self) -> str:
        return self._curr_wp

    @curr_wp.setter
    def curr_wp(self, value: str) -> None:
        self._history.append(self.curr_wp)
        if len(self._history) > self.max_history:
            self._history.pop(0)
        self._curr_wp = value

    @property
    def next_wp(self) -> str:
        self._index += 1
        if self._index == len(self._wallpapers):
            self._index = 0
            if (self.randomize):
                self.shuffle()
        self.curr_wp = self._wallpapers[self._index]
        return self.curr_wp

    @property
    def prev_wp(self) -> str:
        self._curr_wp = self._history.pop()
        self._index -= 1
        if self._index < 0:
            self._index = len(self._wallpapers) - 1
        return self.curr_wp


WALLPAPER_CACHE = WallpaperCache(
    max_history=get_cfg()["max_history"],
    randomize=get_cfg()["randomize_wallpapers"])

