# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class SimpleXls(KaitaiStruct):

    class RecordTypes(Enum):
        number_cell = 3
        string_cell = 4
        eof = 10
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = self._io.read_bytes(8)
        self.cells = []
        i = 0
        while True:
            _ = SimpleXls.Cell(self._io, self, self._root)
            self.cells.append(_)
            if _.rec_type == SimpleXls.RecordTypes.eof:
                break
            i += 1

    class EofCell(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    class CellHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rw = self._io.read_u2le()
            self.col = self._io.read_u2le()
            self.ixfe = self._io.read_u2le()


    class NumberCell(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = SimpleXls.CellHeader(self._io, self, self._root)
            self.unk1 = self._io.read_u1()
            self.value = self._io.read_f8le()


    class StringCell(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = SimpleXls.CellHeader(self._io, self, self._root)
            self.nbytes = self._io.read_u1()
            self.length = self._io.read_u1()
            self.value = (self._io.read_bytes(self.length)).decode(u"cp437")


    class Cell(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rec_type = KaitaiStream.resolve_enum(SimpleXls.RecordTypes, self._io.read_u2le())
            self.substream_length = self._io.read_u2le()
            _on = self.rec_type
            if _on == SimpleXls.RecordTypes.string_cell:
                self.record_value = SimpleXls.StringCell(self._io, self, self._root)
            elif _on == SimpleXls.RecordTypes.number_cell:
                self.record_value = SimpleXls.NumberCell(self._io, self, self._root)
            elif _on == SimpleXls.RecordTypes.eof:
                self.record_value = SimpleXls.EofCell(self._io, self, self._root)



