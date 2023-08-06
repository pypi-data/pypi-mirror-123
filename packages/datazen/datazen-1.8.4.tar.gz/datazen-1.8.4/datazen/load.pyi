import logging
from datazen import GLOBAL_KEY as GLOBAL_KEY
from datazen.parsing import set_file_hash as set_file_hash
from datazen.paths import advance_dict_by_path as advance_dict_by_path, get_file_name as get_file_name, get_path_list as get_path_list, walk_with_excludes as walk_with_excludes
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Tuple

LOG: Any

class LoadedFiles(NamedTuple):
    files: Optional[List[str]]
    file_data: Optional[Dict[str, dict]]

DEFAULT_LOADS: Any

def data_added(key: Any, value: Any, data: dict = ...) -> Iterator[dict]: ...
def meld_and_resolve(full_path: str, existing_data: dict, variables: dict, globals_added: bool = ..., expect_overwrite: bool = ..., is_template: bool = ...) -> bool: ...
def load_dir(path: str, existing_data: dict, variables: dict = ..., loads: LoadedFiles = ..., expect_overwrite: bool = ..., are_templates: bool = ..., logger: logging.Logger = ...) -> dict: ...
def load_dir_only(path: str, expect_overwrite: bool = ..., are_templates: bool = ..., logger: logging.Logger = ...) -> dict: ...
def load_files(file_paths: List[str], root: str, meld_data: Tuple[dict, dict, bool], hashes: Dict[str, dict] = ..., expect_overwrite: bool = ..., are_templates: bool = ...) -> List[str]: ...
