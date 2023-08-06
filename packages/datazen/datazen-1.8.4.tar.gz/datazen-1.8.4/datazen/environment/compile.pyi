import logging
from datazen.compile import get_compile_output as get_compile_output, str_compile as str_compile
from datazen.environment.base import TaskResult as TaskResult
from datazen.environment.task import TaskEnvironment as TaskEnvironment
from datazen.parsing import merge_dicts as merge_dicts
from datazen.paths import advance_dict_by_path as advance_dict_by_path
from datazen.targets import resolve_dep_data as resolve_dep_data
from typing import Any, List

LOG: Any

class CompileEnvironment(TaskEnvironment):
    def __init__(self) -> None: ...
    def valid_compile(self, entry: dict, namespace: str, dep_data: dict = ..., deps_changed: List[str] = ..., logger: logging.Logger = ...) -> TaskResult: ...
