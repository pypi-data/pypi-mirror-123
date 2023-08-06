import logging
from datazen.environment.base import TaskResult as TaskResult
from datazen.environment.task import TaskEnvironment as TaskEnvironment, get_path as get_path
from typing import List

class CommandEnvironment(TaskEnvironment):
    def __init__(self) -> None: ...
    def valid_command(self, entry: dict, _: str, __: dict = ..., deps_changed: List[str] = ..., logger: logging.Logger = ...) -> TaskResult: ...
