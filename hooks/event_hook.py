from typing import Any


class EventHook:
    def __init__(self) -> None:
        self._data = {}
        self._has_changes = False
    
    def set_data(self, **kwargs) -> None:
        self._data = self._data | kwargs
        self._has_changes = True

    def read_data(self) -> dict[Any, Any]:
        self._has_changes = False
        return self._data

    def check_changes(self) -> bool:
        return self._has_changes
