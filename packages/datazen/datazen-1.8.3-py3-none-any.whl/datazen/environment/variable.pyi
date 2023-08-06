from datazen import ROOT_NAMESPACE as ROOT_NAMESPACE
from datazen.enums import DataType as DataType
from datazen.environment.base import BaseEnvironment as BaseEnvironment
from datazen.load import DEFAULT_LOADS as DEFAULT_LOADS, LoadedFiles as LoadedFiles
from typing import List

class VariableEnvironment(BaseEnvironment):
    def load_variables(self, var_loads: LoadedFiles = ..., name: str = ...) -> dict: ...
    def add_variable_dirs(self, dir_paths: List[str], rel_path: str = ..., name: str = ..., allow_dup: bool = ...) -> int: ...
