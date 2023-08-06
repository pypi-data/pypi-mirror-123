import datetime
import enum
import io
import tarfile
from typing import Any, List, Dict, Tuple


from drb import DrbNode
from drb.exceptions import DrbNotImplementationException
from drb.utils.logical_node import DrbLogicalNode


class DrbTarAttributeNames(enum.Enum):
    SIZE = 'size'
    DIRECTORY = 'directory'
    MODIFIED = 'modified'


class DrbTarNode(DrbLogicalNode):
    supported_impl = {
        io.BufferedIOBase,
        tarfile.ExFileObject
    }

    def __init__(self, parent: DrbNode, tar_info: tarfile.TarInfo):
        self._tar_info = tar_info
        path = parent.path / self._get_name()
        DrbLogicalNode.__init__(self, path, parent=parent)

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            name_attribute = DrbTarAttributeNames.DIRECTORY.value
            self._attributes[name_attribute, None] = \
                self._tar_info.type == tarfile.DIRTYPE

            name_attribute = DrbTarAttributeNames.SIZE.value
            self._attributes[name_attribute, None] = self._tar_info.size

            date_time = datetime.datetime.fromtimestamp(self._tar_info.mtime)

            name_attribute = DrbTarAttributeNames.MODIFIED.value
            self._attributes[name_attribute, None] = date_time.strftime("%c")

        return self._attributes

    def _get_name(self) -> str:
        if self._tar_info.name.endswith('/'):
            name = self._tar_info.name[:-1]
        else:
            name = self._tar_info.name
        if '/' in name:
            name = name[name.rindex('/') + 1:]
        return name

    def get_members(self):
        return self.parent.get_members()

    def _is_a_child(self, filename):
        if not filename.startswith(self._tar_info.name):
            return False

        filename = filename[len(self._tar_info.name):]
        if not filename:
            return False

        if not filename.startswith('/') and \
                not self._tar_info.name.endswith('/'):
            return False

        filename = filename[1:]
        if filename.endswith('/'):
            filename = filename[:-1]

        # Either the name do not contains sep either only one a last position
        return '/' not in filename

    @property
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = [DrbTarNode(self, entry) for entry in
                              self.get_members()
                              if self._is_a_child(entry.name)]
            self._children = sorted(self._children,
                                    key=lambda entry_cmp: entry_cmp.name)

        return self._children

    def has_impl(self, impl: type) -> bool:
        if impl in self.supported_impl:
            return not self.get_attribute(DrbTarAttributeNames.DIRECTORY.value,
                                          None)

    def get_impl(self, impl: type) -> Any:
        if self.has_impl(impl):
            return self.parent.open_member(self._tar_info)
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def close(self):
        pass

    def open_member(self, tar_info: tarfile.TarInfo):
        # open a member to retrieve tje implementation
        # back to first parent that is file tar to open it...
        return self.parent.open_member(tar_info)
