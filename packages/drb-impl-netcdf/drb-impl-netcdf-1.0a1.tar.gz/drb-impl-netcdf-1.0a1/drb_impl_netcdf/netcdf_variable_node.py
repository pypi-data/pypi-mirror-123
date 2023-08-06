from typing import Any, List, Dict, Optional, Tuple

import numpy
from drb import DrbNode
from drb.exceptions import DrbNotImplementationException
import netCDF4 as netCDF

from drb.utils.logical_node import DrbLogicalNode
from drb_impl_netcdf.netcdf_common import DrbNetcdfAbstractNode, \
    DrbNetcdfSimpleValueNode


class DrbNetcdfVariableNode(DrbNetcdfAbstractNode):

    def __init__(self, parent: DrbNode, variable: netCDF.Variable):
        name = variable.name
        path = parent.path / name
        DrbLogicalNode.__init__(self, path, parent=parent)
        self._children: List[DrbNode] = None
        self._variable = variable
        # value scalar indicate a variable with only one value
        # in this case value return this value
        # and all method to retrieve array are not activated
        # this type of variable can be for example a time...
        self._is_scalar = len(self._variable.shape) == 0
        self.supported_impl = [netCDF.Variable]
        if not self._is_scalar:
            self.supported_impl.append(numpy.ndarray)
            if variable.mask:
                self.supported_impl.append(numpy.ma.masked_array)
                self.supported_impl.append(numpy.ma.core.MaskedArray)

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            for attribute_name in self._variable.ncattrs():
                self._attributes[(attribute_name, None)] = getattr(
                    self._variable, attribute_name)

        return self._attributes

    @property
    def value(self) -> Any:
        if self._is_scalar:
            return self._variable.getValue()
        return None

    @property
    def children(self) -> List[DrbNode]:

        if self._children is None:
            self._children = []
            if not self._is_scalar:
                self._children.append(DrbNetcdfSimpleValueNode(
                    self, 'dimensions', self._variable.dimensions))
                self._children.append(DrbNetcdfSimpleValueNode(
                    self, 'shape', self._variable.shape))
            self._children.append(DrbNetcdfSimpleValueNode(
                self, 'size', self._variable.size))
        return self._children

    def has_impl(self, impl: type) -> bool:
        if impl in self.supported_impl:
            return True

    def get_impl(self, impl: type) -> Any:
        if self.has_impl(impl):
            if impl == netCDF.Variable:
                return self._variable
            elif not self._is_scalar:
                if impl == numpy.ndarray and self._variable.mask:
                    # if we ask ndarray and not masked array
                    # and array is masked we temporary unset
                    # auto mask to return value unmasked
                    self._variable.set_auto_mask(False)
                    array_to_return = self._variable[:]
                    # restore mask as previous
                    self._variable.set_auto_mask(True)
                else:
                    array_to_return = self._variable[:]
                return array_to_return
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')
