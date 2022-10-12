import json
from textwrap import indent
from threading import RLock
from typing import Dict, List, Union


class MultiValueHashMap():
    def __init__(self, map:Dict={}) -> None:
        self.internal_map = map
        self.lock = RLock()

    def add(self, key, value) -> bool:
        with self.lock as lo:
            if self.internal_map.get(key) is None:
                self.internal_map[key] = [value]
                return False
            else:
                self.internal_map[key].append(value)
                return True

    def set(self, key, value) -> None:
        with self.lock as lo:
            if type(value) is list:
                self.internal_map[key] = value
            else:
                self.internal_map[key] = [value]

    def get(self, key) -> Union[List, None]:
        with self.lock as lo:
            return self.internal_map.get(key)

    def get_default(self, key, default=[]) -> List:
        with self.lock as lo:
            value = self.internal_map.get(key)
            if value is None:
                return []
            else:
                return value

    def clear(self) -> None:
        with self.lock as lo:
            self.internal_map.clear()

    def to_json(self, pretty: bool = False) -> str:
        indent = 4 if pretty else None
        with self.lock as lo:
            return json.dumps(self.internal_map, default=lambda x: x.__dict__(), indent=indent)

    def from_json(json_string: str) -> 'MultiValueHashMap':
        m = json.loads(json_string)
        if m is not None:
            return MultiValueHashMap(m)
        else:
            return MultiValueHashMap()
