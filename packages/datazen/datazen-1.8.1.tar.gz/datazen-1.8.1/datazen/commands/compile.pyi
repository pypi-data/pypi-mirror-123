import logging
from datazen.compile import str_compile as str_compile
from datazen.environment.integrated import Environment as Environment
from datazen.parsing import get_file_ext as get_file_ext
from typing import Any, List

LOG: Any

def cmd_compile(config_dirs: List[str], schema_dirs: List[str], variable_dirs: List[str], output_file_path: str, logger: logging.Logger = ...) -> bool: ...
