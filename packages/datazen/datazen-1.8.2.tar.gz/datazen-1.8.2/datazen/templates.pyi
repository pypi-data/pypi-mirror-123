import jinja2
from datazen.load import DEFAULT_LOADS as DEFAULT_LOADS, LoadedFiles as LoadedFiles
from datazen.parsing import set_file_hash as set_file_hash
from datazen.paths import get_file_ext as get_file_ext, get_file_name as get_file_name
from typing import Dict, List

def update_cache_primitives(dir_path: str, loads: LoadedFiles) -> None: ...
def load(template_dirs: List[str], loads: LoadedFiles = ...) -> Dict[str, jinja2.Template]: ...
