import jinja2
import logging
from datazen.environment.integrated import Environment as Environment
from datazen.parsing import load_stream as load_stream
from typing import Any, List

LOG: Any

def str_render(template: jinja2.Template, config_data_path: str, logger: logging.Logger = ...) -> str: ...
def cmd_render(template_dirs: List[str], template_name: str, config_data_path: str, output_file_path: str, logger: logging.Logger = ...) -> bool: ...
