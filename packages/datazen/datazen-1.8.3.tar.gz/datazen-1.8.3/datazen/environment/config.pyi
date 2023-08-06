import logging
from datazen import ROOT_NAMESPACE as ROOT_NAMESPACE
from datazen.enums import DataType as DataType
from datazen.environment.schema import SchemaEnvironment as SchemaEnvironment
from datazen.environment.variable import VariableEnvironment as VariableEnvironment
from datazen.load import DEFAULT_LOADS as DEFAULT_LOADS, LoadedFiles as LoadedFiles
from typing import List

class ConfigEnvironment(VariableEnvironment, SchemaEnvironment):
    configs_valid: bool
    def __init__(self) -> None: ...
    def load_configs(self, cfg_loads: LoadedFiles = ..., var_loads: LoadedFiles = ..., sch_loads: LoadedFiles = ..., sch_types_loads: LoadedFiles = ..., name: str = ..., logger: logging.Logger = ...) -> dict: ...
    def add_config_dirs(self, dir_paths: List[str], rel_path: str = ..., name: str = ..., allow_dup: bool = ...) -> int: ...
