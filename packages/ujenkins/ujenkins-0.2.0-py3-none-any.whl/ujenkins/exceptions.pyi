from typing import Any

class JenkinsError(Exception):
    message: Any
    status: Any
    def __init__(self, message: Any | None = ..., status: Any | None = ...) -> None: ...

class JenkinsNotFoundError(JenkinsError): ...
