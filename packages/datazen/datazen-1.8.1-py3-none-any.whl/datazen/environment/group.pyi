import logging
from datazen.environment.base import TaskResult as TaskResult
from datazen.environment.task import TaskEnvironment as TaskEnvironment
from typing import List

class GroupEnvironment(TaskEnvironment):
    def __init__(self) -> None: ...
    def valid_group(self, entry: dict, _: str, dep_data: dict = ..., deps_changed: List[str] = ..., logger: logging.Logger = ...) -> TaskResult: ...
