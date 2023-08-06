import shutil
import yaml
import os

from types import MappingProxyType
from typing import Optional, Any, cast
from pathlib import Path


def _load_default_cfg() -> MappingProxyType[str, Any]:
    with open(Path(__file__).parent / "default-cfg.yml") as file:
        return MappingProxyType(yaml.load(file, Loader=yaml.CLoader))


DEFAULT_CFG = _load_default_cfg()
_cfg_path = None
_cfg_data = None


def valid_cfg(cfg: dict[str, Any]) -> bool:
    return True


def _find_cfg_path() -> Path:

    if (path := os.environ.get("WCD_CFG", None)) is not None:
        return Path(path)

    if (cfg_home := os.environ.get("XDG_CONFIG_HOME")) is not None:
        return Path(cfg_home) / "wcd/cfg.yml"

    return Path(os.path.expanduser("~/.config/wcd/cfg.yml"))


def load_cfg(path: Optional[Path]=None) -> dict[str, Any]:

    global _cfg_path
    path = path or _cfg_path
    if path is None:
       path = _cfg_path = _find_cfg_path()

    if not path.parent.exists():
        os.makedirs(path.parent, exist_ok=True)
    if not path.exists():
        shutil.copyfile(Path(__file__).parent / "default-cfg.yml", path)
        return DEFAULT_CFG.copy()

    with open(path) as file:
        cfg = yaml.load(file, Loader=yaml.CLoader)
    if not valid_cfg(cfg):
        raise NotImplementedError()

    return DEFAULT_CFG | cfg


def get_cfg() -> dict[str, Any]:
    global _cfg_data
    if _cfg_data is None:
        _cfg_data = load_cfg()
    return _cfg_data


def save_cfg(path: Optional[Path]=None) -> None:

    if path is _cfg_data is None:
        raise RuntimeError("Tried saving a config without loading it first")

    with open(cast(Path, path or _cfg_path), "w") as file:
        yaml.dump(_cfg_data, file, Dumper=yaml.CDumper)
    
