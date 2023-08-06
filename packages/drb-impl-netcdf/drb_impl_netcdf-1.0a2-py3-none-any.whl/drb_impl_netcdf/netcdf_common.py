import abc
import enum
from abc import ABC
from typing import Optional, List, Any, Dict, Tuple


from drb import DrbNode
from drb.exceptions import DrbNotImplementationException
from drb.path import ParsedPath
from drb.utils.logical_node import DrbLogicalNode


class DrbNetcdfAttributeNames(enum.Enum):
    UNLIMITED = 'unlimited'


class DrbNetcdfAbstractNode(DrbLogicalNode, abc.ABC):

    _path = None

    @property
    def namespace_uri(self) -> Optional[str]:
        return 'http://www.unidata.ucar.edu/netcdf'

    def close(self) -> None:
        pass

    @property
    def path(self) -> ParsedPath:
        if self._path is None:
            self._path = self.parent.path / self.name
        return self._path


class DrbNetcdfSimpleNode(DrbNetcdfAbstractNode, ABC):

    def __init__(self, parent: DrbNode, name):
        self._parent: DrbNode = parent
        self._attributes = None
        self._name = name
        self._value = None

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> List[DrbNode]:
        return []


class DrbNetcdfSimpleValueNode(DrbNetcdfSimpleNode):

    def __init__(self, parent: DrbNode, name: str, value: any):
        super().__init__(parent, name)
        self._value = value

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    @property
    def value(self) -> Any:
        return self._value

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type) -> Any:
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')
