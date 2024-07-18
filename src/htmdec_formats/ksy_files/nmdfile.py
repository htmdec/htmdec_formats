# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Nmdfile(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.sequence = []
        for i in range(837):
            self.sequence.append(self._io.read_u4le())

        self.unk = self._io.read_bytes(3)
        self._raw_xml = self._io.read_bytes_term(0, False, True, True)
        _io__raw_xml = KaitaiStream(BytesIO(self._raw_xml))
        self.xml = Nmdfile.XmlSection(_io__raw_xml, self, self._root)
        self.padding = self._io.read_bytes(1)
        if not self.padding == b"\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x00", self.padding, self._io, u"/seq/3")
        self.rest = self._io.read_bytes_full()

    class XmlSection(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.raw_contents = self._io.read_bytes_full()

        @property
        def contents(self):
            if hasattr(self, '_m_contents'):
                return self._m_contents

            _pos = self._io.pos()
            self._io.seek(0)
            self._m_contents = (self._io.read_bytes((len(self.raw_contents) - 2))).decode(u"utf-8")
            self._io.seek(_pos)
            return getattr(self, '_m_contents', None)

        @property
        def rows(self):
            if hasattr(self, '_m_rows'):
                return self._m_rows

            io = self._root._io
            _pos = io.pos()
            io.seek((((len(self.raw_contents) - 2) + (837 * 4)) + 3))
            self._m_rows = Nmdfile.VariableOutput(io, self, self._root)
            io.seek(_pos)
            return getattr(self, '_m_rows', None)


    class Datasets(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.variables = []
            i = 0
            while not self._io.is_eof():
                self.variables.append(Nmdfile.VariableOutput(self._io, self, self._root))
                i += 1



    class VariableOutput(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.row_count = self._io.read_u4le()
            self.values = self._io.read_bytes((8 * self.row_count))


    @property
    def data(self):
        if hasattr(self, '_m_data'):
            return self._m_data

        _pos = self._io.pos()
        self._io.seek(((((837 * 4) + 3) + len(self._root.xml.raw_contents)) - 2))
        self._m_data = Nmdfile.Datasets(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_data', None)


