# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Dotnetlist(KaitaiStruct):

    class RecordTypeEnum(Enum):
        serialized_stream_header = 0
        class_with_id = 1
        system_class_with_members = 2
        class_with_members = 3
        system_class_with_members_and_types = 4
        class_with_members_and_types = 5
        binary_object_string = 6
        binary_array = 7
        member_primitive_typed = 8
        member_reference = 9
        object_null = 10
        message_end = 11
        binary_library = 12
        object_null_multiple_256 = 13
        object_null_multiple = 14
        array_single_primitive = 15
        array_single_object = 16
        array_single_string = 17
        method_call = 21
        method_return = 22

    class BinaryTypeEnum(Enum):
        primitive = 0
        string = 1
        object = 2
        system_class = 3
        klass = 4
        object_array = 5
        string_array = 6
        primitive_array = 7

    class PrimitiveTypeEnum(Enum):
        boolean = 1
        byte = 2
        char = 3
        empty = 4
        decimal = 5
        double = 6
        int16 = 7
        int32 = 8
        int64 = 9
        sbyte = 10
        single = 11
        timespan = 12
        datetime = 13
        uint16 = 14
        uint32 = 15
        uint64 = 16
        null_ = 17
        string = 18
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.records = []
        i = 0
        while True:
            _ = Dotnetlist.SerializedRecord(self._io, self, self._root)
            self.records.append(_)
            if _.record_type == Dotnetlist.RecordTypeEnum.message_end:
                break
            i += 1

    class SerializationHeaderRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.top_id = self._io.read_u4le()
            self.header_id = self._io.read_u4le()
            self.major_version = self._io.read_u4le()
            self.minor_version = self._io.read_u4le()


    class LengthByte(KaitaiStruct):
        def __init__(self, idx, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.idx = idx
            self._read()

        def _read(self):
            self.val = self._io.read_u1()

        @property
        def last(self):
            if hasattr(self, '_m_last'):
                return self._m_last if hasattr(self, '_m_last') else None

            self._m_last = (self.val & 128) == 0
            return self._m_last if hasattr(self, '_m_last') else None

        @property
        def current_value(self):
            if hasattr(self, '_m_current_value'):
                return self._m_current_value if hasattr(self, '_m_current_value') else None

            self._m_current_value = (self.val if self.idx == 0 else (self._parent.length_bytes[(self.idx - 1)].current_value + (self.val << (self.idx * 8))))
            return self._m_current_value if hasattr(self, '_m_current_value') else None


    class PrimitiveType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ptype = KaitaiStream.resolve_enum(Dotnetlist.PrimitiveTypeEnum, self._io.read_u1())


    class MemberTypeInfo(KaitaiStruct):
        def __init__(self, count, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.count = count
            self._read()

        def _read(self):
            self.binary_type = [None] * (self.count)
            for i in range(self.count):
                self.binary_type[i] = KaitaiStream.resolve_enum(Dotnetlist.BinaryTypeEnum, self._io.read_u1())

            self.additional_infos = [None] * (self.count)
            for i in range(self.count):
                _on = self.binary_type[i]
                if _on == Dotnetlist.BinaryTypeEnum.primitive:
                    self.additional_infos[i] = Dotnetlist.PrimitiveType(self._io, self, self._root)
                elif _on == Dotnetlist.BinaryTypeEnum.system_class:
                    self.additional_infos[i] = Dotnetlist.SystemClassName(self._io, self, self._root)
                elif _on == Dotnetlist.BinaryTypeEnum.klass:
                    self.additional_infos[i] = Dotnetlist.ClassInfo(self._io, self, self._root)
                elif _on == Dotnetlist.BinaryTypeEnum.primitive_array:
                    self.additional_infos[i] = Dotnetlist.PrimitiveType(self._io, self, self._root)

            self.members = [None] * (self.count)
            for i in range(self.count):
                _on = self.binary_type[i]
                if _on == Dotnetlist.BinaryTypeEnum.primitive:
                    self.members[i] = Dotnetlist.PrimitiveValue(self.additional_infos[i].ptype, self._io, self, self._root)
                elif _on == Dotnetlist.BinaryTypeEnum.primitive_array:
                    self.members[i] = Dotnetlist.SerializedRecord(self._io, self, self._root)



    class SerializedRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.record_type = KaitaiStream.resolve_enum(Dotnetlist.RecordTypeEnum, self._io.read_u1())
            _on = self.record_type
            if _on == Dotnetlist.RecordTypeEnum.serialized_stream_header:
                self.record = Dotnetlist.SerializationHeaderRecord(self._io, self, self._root)
            elif _on == Dotnetlist.RecordTypeEnum.system_class_with_members_and_types:
                self.record = Dotnetlist.SystemClassWithMembersAndTypesRecord(self._io, self, self._root)
            elif _on == Dotnetlist.RecordTypeEnum.member_reference:
                self.record = Dotnetlist.MemberReferenceRecord(self._io, self, self._root)
            elif _on == Dotnetlist.RecordTypeEnum.array_single_primitive:
                self.record = Dotnetlist.ArraySinglePrimitiveRecord(self._io, self, self._root)


    class ClassInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.object_id = self._io.read_u4le()
            self.name = Dotnetlist.LengthPrefixedString(self._io, self, self._root)
            self.member_count = self._io.read_u4le()
            self.member_names = [None] * (self.member_count)
            for i in range(self.member_count):
                self.member_names[i] = Dotnetlist.LengthPrefixedString(self._io, self, self._root)



    class SystemClassName(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.class_name = (self._io.read_bytes_term(0, False, True, True)).decode(u"utf-8")


    class ArrayInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.object_id = self._io.read_u4le()
            self.length = self._io.read_u4le()


    class SystemClassWithMembersAndTypesRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.info = Dotnetlist.ClassInfo(self._io, self, self._root)
            self.type_info = Dotnetlist.MemberTypeInfo(self.info.member_count, self._io, self, self._root)


    class LengthPrefixedString(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.length_bytes = []
            i = 0
            while True:
                _ = Dotnetlist.LengthByte(i, self._io, self, self._root)
                self.length_bytes.append(_)
                if _.last == True:
                    break
                i += 1
            self.value = (self._io.read_bytes(self.length)).decode(u"utf-8")

        @property
        def length(self):
            if hasattr(self, '_m_length'):
                return self._m_length if hasattr(self, '_m_length') else None

            self._m_length = self.length_bytes[(len(self.length_bytes) - 1)].current_value
            return self._m_length if hasattr(self, '_m_length') else None


    class MemberReferenceRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id_ref = self._io.read_u4le()


    class ArraySinglePrimitiveRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.info = Dotnetlist.ArrayInfo(self._io, self, self._root)
            self.value_type = KaitaiStream.resolve_enum(Dotnetlist.PrimitiveTypeEnum, self._io.read_u1())
            self.values = [None] * (self.info.length)
            for i in range(self.info.length):
                _on = self.value_type
                if _on == Dotnetlist.PrimitiveTypeEnum.double:
                    self.values[i] = self._io.read_f8le()
                elif _on == Dotnetlist.PrimitiveTypeEnum.uint16:
                    self.values[i] = self._io.read_u2le()
                elif _on == Dotnetlist.PrimitiveTypeEnum.int16:
                    self.values[i] = self._io.read_s2le()
                elif _on == Dotnetlist.PrimitiveTypeEnum.int64:
                    self.values[i] = self._io.read_s8le()
                elif _on == Dotnetlist.PrimitiveTypeEnum.int32:
                    self.values[i] = self._io.read_s4le()
                elif _on == Dotnetlist.PrimitiveTypeEnum.byte:
                    self.values[i] = self._io.read_u1()
                elif _on == Dotnetlist.PrimitiveTypeEnum.uint32:
                    self.values[i] = self._io.read_u4le()
                elif _on == Dotnetlist.PrimitiveTypeEnum.uint64:
                    self.values[i] = self._io.read_u8le()
                elif _on == Dotnetlist.PrimitiveTypeEnum.char:
                    self.values[i] = self._io.read_u1()
                elif _on == Dotnetlist.PrimitiveTypeEnum.single:
                    self.values[i] = self._io.read_f4le()



    class PrimitiveValue(KaitaiStruct):
        def __init__(self, value_type, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.value_type = value_type
            self._read()

        def _read(self):
            _on = self.value_type
            if _on == Dotnetlist.PrimitiveTypeEnum.double:
                self.value = self._io.read_f8le()
            elif _on == Dotnetlist.PrimitiveTypeEnum.uint16:
                self.value = self._io.read_u2le()
            elif _on == Dotnetlist.PrimitiveTypeEnum.int16:
                self.value = self._io.read_s2le()
            elif _on == Dotnetlist.PrimitiveTypeEnum.int64:
                self.value = self._io.read_s8le()
            elif _on == Dotnetlist.PrimitiveTypeEnum.int32:
                self.value = self._io.read_s4le()
            elif _on == Dotnetlist.PrimitiveTypeEnum.byte:
                self.value = self._io.read_u1()
            elif _on == Dotnetlist.PrimitiveTypeEnum.uint32:
                self.value = self._io.read_u4le()
            elif _on == Dotnetlist.PrimitiveTypeEnum.uint64:
                self.value = self._io.read_u8le()
            elif _on == Dotnetlist.PrimitiveTypeEnum.char:
                self.value = self._io.read_u1()
            elif _on == Dotnetlist.PrimitiveTypeEnum.single:
                self.value = self._io.read_f4le()



