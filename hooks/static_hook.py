from typing import Any
    

class StaticHook:
    _data = dict()
    
    @classmethod
    def add_data(cls, **kwargs) -> None:
        cls._data = cls._data | kwargs
    
    @classmethod
    def read_data(cls) -> dict[Any, Any]:
        return cls._data

    @classmethod
    def clear_data(cls) -> None:
        cls._data = dict()
