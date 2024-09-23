# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Pxtfile(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.unk1 = self._io.read_u2le()
        self.unk2 = self._io.read_u2le()
        self.unk3 = self._io.read_u4le()
        self.unk4 = self._io.read_u2le()
        self.unk5 = self._io.read_u2le()
        self.wave_size = self._io.read_u4le()
        self._raw_wave = self._io.read_bytes((self.wave_size + 40))
        _io__raw_wave = KaitaiStream(BytesIO(self._raw_wave))
        self.wave = Pxtfile.WaveData(_io__raw_wave, self, self._root)
        self.unk7 = []
        for i in range(4):
            self.unk7.append(self._io.read_u4le())

        self.metadata = (self._io.read_bytes_full()).decode(u"utf-8")

    class WaveData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk0 = []
            for i in range(21):
                self.unk0.append(self._io.read_u4le())

            self.name = (self._io.read_bytes(40)).decode(u"utf-8")
            self.num_rows = self._io.read_u4le()
            self.num_cols = self._io.read_u4le()
            self.num_layers = self._io.read_u4le()
            self.unk1 = self._io.read_u4le()
            self.row_delta = self._io.read_f8le()
            self.col_delta = self._io.read_f8le()
            self.layer_delta = self._io.read_f8le()
            self.unk2 = self._io.read_f8le()
            self.row_start = self._io.read_f8le()
            self.col_start = self._io.read_f8le()
            self.layer_start = self._io.read_f8le()
            self.unk4 = self._io.read_f8le()
            self.unk5 = []
            for i in range(39):
                self.unk5.append(self._io.read_f4le())

            self.layers = []
            for i in range((self.num_layers if self.num_layers > 0 else 1)):
                self.layers.append(Pxtfile.Layer(self._io, self, self._root))



    class Layer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.value = []
            for i in range(((self._parent.num_rows if self._parent.num_rows > 0 else 1) * (self._parent.num_cols if self._parent.num_cols > 0 else 1))):
                self.value.append(self._io.read_f4le())




