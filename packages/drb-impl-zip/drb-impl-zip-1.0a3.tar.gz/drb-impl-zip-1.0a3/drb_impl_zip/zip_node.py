import enum
import io
import zipfile
from typing import Any, List, Dict, Optional, Tuple

import drb

from drb import DrbNode
from drb.exceptions import DrbNotImplementationException
from drb.utils.logical_node import DrbLogicalNode


class DrbZipAttributeNames(enum.Enum):
    SIZE = 'size'
    DIRECTORY = 'directory'
    RATIO = 'ratio'
    PACKED = 'packed'


class DrbZipNode(DrbLogicalNode):

    supported_impl = {
        io.BufferedIOBase,
        zipfile.ZipExtFile
    }

    def __init__(self, parent: DrbNode, zip_info: zipfile.ZipInfo):
        self._zip_info = zip_info
        path = parent.path / self._get_name_zip()
        DrbLogicalNode.__init__(self, path, parent=parent)

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            name_attribute = DrbZipAttributeNames.DIRECTORY.value
            self._attributes[name_attribute, None] = self._zip_info.is_dir()

            name_attribute = DrbZipAttributeNames.SIZE.value
            self._attributes[name_attribute, None] = self._zip_info.file_size

            name_attribute = DrbZipAttributeNames.RATIO.value
            if self._zip_info.compress_size > 0:
                self._attributes[name_attribute, None] = \
                    self._zip_info.file_size / self._zip_info.compress_size
            else:
                self._attributes[name_attribute, None] = 0
            name_attribute = DrbZipAttributeNames.PACKED.value
            self._attributes[name_attribute, None] = \
                self._zip_info.compress_size
        return self._attributes

    def _get_name_zip(self) -> str:
        if self._zip_info.filename.endswith('/'):
            name = self._zip_info.filename[:-1]
        else:
            name = self._zip_info.filename
        if '/' in name:
            name = name[name.rindex('/') + 1:]
        return name

    def get_file_list(self):
        return self.parent.get_file_list()

    def _is_a_child(self, filename):
        if not filename.startswith(self._zip_info.filename):
            return False

        filename = filename[len(self._zip_info.filename):]

        if not filename:
            return False

        if not filename.startswith('/') and \
                not self._zip_info.filename.endswith('/'):
            return False

        # Either the name do not contains sep either only one a last position
        return '/' not in filename or filename.index('/') == (
                len(filename) - 1)

    @property
    @drb.resolve_children
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = [DrbZipNode(self, entry) for entry in
                              self.get_file_list()
                              if self._is_a_child(entry.filename)]
            self._children = sorted(self._children,
                                    key=lambda entry_cmp: entry_cmp.name)

        return self._children

    def has_impl(self, impl: type) -> bool:
        if impl in self.supported_impl:
            return not self.get_attribute(
                DrbZipAttributeNames.DIRECTORY.value, None)

    def get_impl(self, impl: type) -> Any:
        if self.has_impl(impl):
            return self.parent.open_entry(self._zip_info)
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def close(self):
        pass

    def open_entry(self, zip_info: zipfile.ZipInfo):
        # open the entry on zip file to return ZipExtFile
        # we back to the first node_file to open is
        return self.parent.open_entry(zip_info)
