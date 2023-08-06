import io
import os
from typing import Any, Optional, Union, List

import netCDF4

from drb import DrbNode
from drb.factory import DrbFactory
from drb.utils.logical_node import DrbLogicalNode

from drb_impl_netcdf.execptions import DrbNetcdfNodeException
from drb_impl_netcdf.netcdf_group_node import DrbNetcdfGroupNode


class DrbNetcdfNode(DrbLogicalNode):

    def __init__(self, base_node: DrbNode):
        self._netcdf_file_source = None
        self._root_dataset = None
        DrbLogicalNode.__init__(self, base_node)

        if self._wrapped_node.has_impl(io.BufferedIOBase):
            self._netcdf_file_source = self._wrapped_node \
                         .get_impl(io.BufferedIOBase)
            self._root_dataset = netCDF4.Dataset(filename=self
                                                 ._netcdf_file_source.name)
            self.root_node = DrbNetcdfGroupNode(self, self._root_dataset)

        else:
            raise DrbNetcdfNodeException(f'Unsupported parent '
                                         f'{type(self.parent).__name__} '
                                         f'for DrbNetcdfRootNode')

    @property
    def children(self) -> List[DrbNode]:
        return [self.root_node]

    def has_impl(self, impl: type) -> bool:
        return self._wrapped_node.has_impl(impl)

    def get_impl(self, impl: type) -> Any:
        return self._wrapped_node.get_impl(impl)

    def close(self):
        if self._root_dataset is not None:
            self._root_dataset.close()
        if self._netcdf_file_source is not None:
            self._netcdf_file_source.close()
        self._wrapped_node.close()


class DrbNetcdfFactory(DrbFactory):

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbNetcdfNode(base_node=node)
