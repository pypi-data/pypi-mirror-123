import re
from datazen.parsing import merge as merge
from datazen.paths import advance_dict_by_path as advance_dict_by_path, format_resolve_delims as format_resolve_delims, unflatten_dict as unflatten_dict
from typing import Dict, List, NamedTuple, Tuple

KW_OPEN: str
KW_CLOSE: str
KW_PATTERN: str

def target_is_literal(name: str) -> bool: ...

class ParseResult(NamedTuple):
    pattern: re.Pattern
    keys: List[str]

def parse_target(name: str) -> ParseResult: ...
def parse_targets(targets: List[dict]) -> Tuple[Dict[str, dict], Dict[str, dict]]: ...
MatchData = Dict[str, str]

class TargetMatch(NamedTuple):
    found: bool
    substitutions: MatchData

def match_target(name: str, pattern: re.Pattern, keys: List[str]) -> TargetMatch: ...
def resolve_target_list(target_list: list, match_data: MatchData) -> list: ...
def resolve_dep_data(entry: dict, data: dict) -> dict: ...
def resolve_target_data(target_data: dict, match_data: MatchData) -> dict: ...
