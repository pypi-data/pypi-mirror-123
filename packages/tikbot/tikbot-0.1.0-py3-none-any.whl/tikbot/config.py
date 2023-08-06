import attr
import os
from typing import List, Optional, Union

from tikbot.apiros import ApiRos


def _get_default_directory() -> str:
    ret = os.environ.get("TIKBOT_HOME") or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "tikbot"
    )
    return os.path.realpath(ret)


@attr.dataclass
class Router:
    name: str = ""
    ip: str = ""
    port: int = 8728
    username: str = ""
    password: str = ""
    secure: bool = False
    _api: Optional[ApiRos] = None

    @classmethod
    def defaults(cls):
        return [cls()]

    @property
    def api(self) -> ApiRos:
        if self._api:
            return self._api
        self._api = ApiRos(
            dst=self.ip,
            port=self.port,
            secure=self.secure,
            hide=True,
        )
        self._api.login(self.username, self.password)
        return self._api


@attr.dataclass
class Config:
    directory: str = attr.ib(factory=_get_default_directory)
    token: str = ""
    chats: List[Union[str, int]] = attr.ib(factory=list)
    routers: List[Router] = attr.ib(factory=Router.defaults)

    def __attrs_post_init__(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
            with open(os.path.join(self.directory, "README"), "w") as f:
                f.write("This directory is mantained by the tikbot")
