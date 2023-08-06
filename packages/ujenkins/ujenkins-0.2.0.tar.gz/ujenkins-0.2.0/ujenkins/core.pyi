from typing import Any, NamedTuple
from ujenkins.endpoints import Builds as Builds, Nodes as Nodes, System as System
from ujenkins.exceptions import JenkinsError as JenkinsError, JenkinsNotFoundError as JenkinsNotFoundError

class Response(NamedTuple):
    status: Any
    headers: Any
    body: Any

class Jenkins:
    builds: Any
    nodes: Any
    system: Any
    def __init__(self) -> None: ...
