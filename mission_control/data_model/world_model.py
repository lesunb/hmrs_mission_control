
from enum import Enum
from typing import Callable, List

from matplotlib.collections import Collection


class InvalidWorldModelSymbolError(Exception):
    def __init__(self, label, domain_qualifiers, context):
        m = ''
        if context:
            m += f'error in {context}\n'
        m += f'{label} is not a valid {domain_qualifiers}'
        self.message = m
        super().__init__(m)


def enum_map(enum: Enum):
    return {e.value: e for e in enum}

class WorldModelDomain:
    """
    Get validated constants while building requests
    """
    def __init__(self, name):
        self.name = name
        self._register = {}

    def register(self, fnc: Callable, *domain_qualifiers: List[str]):
        """ register a custom function """
        self._register['.'.join(domain_qualifiers)] = fnc

    def register_enum(self, enum: Enum, *domain_qualifiers: List[str]):
        """ register an enum. Query check if label is a value of one of items """
        _map = enum_map(enum)
        self._register['.'.join(domain_qualifiers)] = _map.get

    def register_collection(self, col: Collection, *domain_qualifiers: List[str]):
        """ register a collection of elements. Query check if label is in the registred collection """
        self._register['.'.join(domain_qualifiers)] = lambda value: value if value in col else None
        
    def query(self, label: str, domain_qualifiers: List[str]):
        if not self._register['.'.join(domain_qualifiers)]:
            raise f'no symbol with qualifiers {domain_qualifiers}'
        try:
            fnc = self._register['.'.join(domain_qualifiers)]
            return fnc(label)
        except KeyError:
            return None

    def get(self, label: str, *domain_qualifiers: List[str], context: str =None):
        result = self.query(label, domain_qualifiers)
        if not result:
            self._raise_not_found(label, domain_qualifiers, context)

        return result
    
    def _raise_not_found(self, label, domain_qualifiers, context):
        raise InvalidWorldModelSymbolError(label, domain_qualifiers, context)