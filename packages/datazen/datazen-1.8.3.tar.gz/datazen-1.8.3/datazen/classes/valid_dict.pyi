import logging
from cerberus import Validator as Validator
from collections import UserDict
from typing import Any

class ValidDict(UserDict):
    name: Any
    validator: Any
    valid: Any
    logger: Any
    def __init__(self, name: str, data: dict, schema: Validator, logger: logging.Logger = ...) -> None: ...
