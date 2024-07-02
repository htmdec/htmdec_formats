# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Vk4(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_header = self._io.read_bytes(12)
        _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
        self.header = Vk4.Header(_io__raw_header, self, self._root)
        self._raw_offset_table = self._io.read_bytes(72)
        _io__raw_offset_table = KaitaiStream(BytesIO(self._raw_offset_table))
        self.offset_table = Vk4.OffsetTable(_io__raw_offset_table, self, self._root)
        self.meas_conds = Vk4.MeasurementConditions(self._io, self, self._root)

    class FalseColorImage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.bit_depth = self._io.read_u4le()
            if not  ((self.bit_depth == 8) or (self.bit_depth == 16) or (self.bit_depth == 32)) :
                raise kaitaistruct.ValidationNotAnyOfError(self.bit_depth, self._io, u"/types/false_color_image/seq/2")
            self.compression = self._io.read_u4le()
            self.byte_size = self._io.read_u4le()
            self.palette_range_min = self._io.read_u4le()
            self.palette_range_max = self._io.read_u4le()
            self.palette = []
            for i in range(256):
                self.palette.append(Vk4.RgbRecord(self._io, self, self._root))

            self.data = self._io.read_bytes(((self.width * self.height) * self.bit_depth) // 8)

        @property
        def bps(self):
            if hasattr(self, '_m_bps'):
                return self._m_bps

            self._m_bps = (self.bit_depth >> 3)
            return getattr(self, '_m_bps', None)


    class RgbRecord(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.red = self._io.read_u1()
            self.green = self._io.read_u1()
            self.blue = self._io.read_u1()


    class TrueColorImage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.bit_depth = self._io.read_u4le()
            if not  ((self.bit_depth == 24)) :
                raise kaitaistruct.ValidationNotAnyOfError(self.bit_depth, self._io, u"/types/true_color_image/seq/2")
            self.compression = self._io.read_u4le()
            self.byte_size = self._io.read_u4le()
            self.data = self._io.read_bytes(((self.width * self.height) * self.bit_depth) // 8)

        @property
        def bps(self):
            if hasattr(self, '_m_bps'):
                return self._m_bps

            self._m_bps = (self.bit_depth >> 3)
            return getattr(self, '_m_bps', None)


    class Blank(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    class CodedString(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.length = self._io.read_u4le()
            self.string = (self._io.read_bytes((self.length * 2))).decode(u"UTF-16LE")


    class MeasurementCondition(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.year = self._io.read_u4le()
            self.month = self._io.read_u4le()
            self.day = self._io.read_u4le()
            self.hour = self._io.read_u4le()
            self.minute = self._io.read_u4le()
            self.second = self._io.read_u4le()
            self.diff_utc_by_minutes = self._io.read_s4le()
            self.image_attributes = self._io.read_u4le()
            self.user_interface_mode = self._io.read_u4le()
            self.color_composite_mode = self._io.read_u4le()
            self.num_layer = self._io.read_u4le()
            self.run_mode = self._io.read_u4le()
            self.peak_mode = self._io.read_u4le()
            self.sharpening_level = self._io.read_u4le()
            self.speed = self._io.read_u4le()
            self.distance = self._io.read_u4le()
            self.pitch = self._io.read_u4le()
            self.optical_zoom = self._io.read_u4le()
            self.num_line = self._io.read_u4le()
            self.line0_pos = self._io.read_u4le()
            self.reserved1 = []
            for i in range(3):
                self.reserved1.append(self._io.read_u4le())

            self.lens_mag = self._io.read_u4le()
            self.pmt_gain_mode = self._io.read_u4le()
            self.pmt_gain = self._io.read_u4le()
            self.pmt_offset = self._io.read_u4le()
            self.nd_filter = self._io.read_u4le()
            self.reserved2 = self._io.read_u4le()
            self.persist_count = self._io.read_u4le()
            self.shutter_speed_mode = self._io.read_u4le()
            self.shutter_speed = self._io.read_u4le()
            self.white_balance_mode = self._io.read_u4le()
            self.white_balance_red = self._io.read_u4le()
            self.white_balance_blue = self._io.read_u4le()
            self.camera_gain = self._io.read_u4le()
            self.plane_compensation = self._io.read_u4le()
            self.xy_length_unit = self._io.read_u4le()
            self.z_length_unit = self._io.read_u4le()
            self.xy_decimal_place = self._io.read_u4le()
            self.z_decimal_place = self._io.read_u4le()
            self.x_length_per_pixel = self._io.read_u4le()
            self.y_length_per_pixel = self._io.read_u4le()
            self.z_length_per_digit = self._io.read_u4le()
            self.reserved3 = []
            for i in range(5):
                self.reserved3.append(self._io.read_u4le())

            self.light_filter_type = self._io.read_u4le()
            self.reserved4 = self._io.read_u4le()
            self.gamma_reverse = self._io.read_u4le()
            self.gamma = self._io.read_u4le()
            self.gamma_offset = self._io.read_u4le()
            self.ccd_bw_offset = self._io.read_u4le()
            self.numerical_aperture = self._io.read_u4le()
            self.head_type = self._io.read_u4le()
            self.pmt_gain2 = self._io.read_u4le()
            self.omit_color_image = self._io.read_u4le()
            self.lens_id = self._io.read_u4le()
            self.light_lut_mode = self._io.read_u4le()
            self.light_lut_in0 = self._io.read_u4le()
            self.light_lut_out0 = self._io.read_u4le()
            self.light_lut_in1 = self._io.read_u4le()
            self.light_lut_out1 = self._io.read_u4le()
            self.light_lut_in2 = self._io.read_u4le()
            self.light_lut_out2 = self._io.read_u4le()
            self.light_lut_in3 = self._io.read_u4le()
            self.light_lut_out3 = self._io.read_u4le()
            self.light_lut_in4 = self._io.read_u4le()
            self.light_lut_out4 = self._io.read_u4le()
            self.upper_position = self._io.read_u4le()
            self.lower_position = self._io.read_u4le()
            self.light_effective_bit_depth = self._io.read_u4le()
            self.height_effective_bit_depth = self._io.read_u4le()
            self.remainder = self._io.read_bytes_full()


    class AssemblyHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u4le()
            self.file_type = self._io.read_u2le()
            if not  ((self.file_type == 0) or (self.file_type == 1) or (self.file_type == 2)) :
                raise kaitaistruct.ValidationNotAnyOfError(self.file_type, self._io, u"/types/assembly_header/seq/1")
            self.stage_type = self._io.read_u2le()
            self.x_position = self._io.read_u4le()
            self.y_position = self._io.read_u4le()
            self.auto_adjustement = self._io.read_bytes(1)
            self.source = self._io.read_bytes(1)
            self.thin_out = self._io.read_u2le()
            self.count_x = self._io.read_u2le()
            self.count_y = self._io.read_u2le()


    class MeasurementConditions(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.struct_size = self._io.read_u4le()
            if not self.struct_size >= 304:
                raise kaitaistruct.ValidationLessThanError(304, self.struct_size, self._io, u"/types/measurement_conditions/seq/0")
            self._raw_conditions = self._io.read_bytes((self.struct_size - 4))
            _io__raw_conditions = KaitaiStream(BytesIO(self._raw_conditions))
            self.conditions = Vk4.MeasurementCondition(_io__raw_conditions, self, self._root)


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x56\x4B\x34\x5F":
                raise kaitaistruct.ValidationNotEqualError(b"\x56\x4B\x34\x5F", self.magic, self._io, u"/types/header/seq/0")
            self.dll_version = self._io.read_bytes(4)
            self.file_type = self._io.read_bytes(4)


    class DataImage(KaitaiStruct):
        def __init__(self, root_pos, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.root_pos = root_pos
            self._read()

        def _read(self):
            pass

        @property
        def value(self):
            if hasattr(self, '_m_value'):
                return self._m_value

            _pos = self._io.pos()
            self._io.seek(self.root_pos)
            self._m_value = Vk4.FalseColorImage(self._io, self, self._root)
            self._io.seek(_pos)
            return getattr(self, '_m_value', None)


    class OffsetTable(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.setting = self._io.read_u4le()
            self.color_peak = self._io.read_u4le()
            self.color_light = self._io.read_u4le()
            self.light = []
            for i in range(3):
                self.light.append(self._io.read_u4le())

            self.height = []
            for i in range(3):
                self.height.append(self._io.read_u4le())

            self.color_peak_thumbnail = self._io.read_u4le()
            self.color_light_thumbnail = self._io.read_u4le()
            self.light_thumbnail = self._io.read_u4le()
            self.height_thumbnail = self._io.read_u4le()
            self.assemble = self._io.read_u4le()
            self.line_measure = self._io.read_u4le()
            self.line_thickness = self._io.read_u4le()
            self.string_data = self._io.read_u4le()
            self.reserved = self._io.read_u4le()


    @property
    def height(self):
        if hasattr(self, '_m_height'):
            return self._m_height

        self._m_height = []
        for i in range(len(self.offset_table.height)):
            _on = self.offset_table.height[i] > 0
            if _on == True:
                self._m_height.append(Vk4.DataImage(self.offset_table.height[i], self._io, self, self._root))
            elif _on == False:
                self._m_height.append(Vk4.Blank(self._io, self, self._root))

        return getattr(self, '_m_height', None)

    @property
    def light(self):
        if hasattr(self, '_m_light'):
            return self._m_light

        self._m_light = []
        for i in range(len(self.offset_table.light)):
            _on = self.offset_table.light[i] > 0
            if _on == True:
                self._m_light.append(Vk4.DataImage(self.offset_table.light[i], self._io, self, self._root))
            elif _on == False:
                self._m_light.append(Vk4.Blank(self._io, self, self._root))

        return getattr(self, '_m_light', None)

    @property
    def color_light(self):
        if hasattr(self, '_m_color_light'):
            return self._m_color_light

        _pos = self._io.pos()
        self._io.seek(self.offset_table.color_light)
        self._m_color_light = Vk4.TrueColorImage(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_color_light', None)

    @property
    def strings(self):
        if hasattr(self, '_m_strings'):
            return self._m_strings

        _pos = self._io.pos()
        self._io.seek(self.offset_table.string_data)
        self._m_strings = []
        for i in range(2):
            self._m_strings.append(Vk4.CodedString(self._io, self, self._root))

        self._io.seek(_pos)
        return getattr(self, '_m_strings', None)

    @property
    def color_peak(self):
        if hasattr(self, '_m_color_peak'):
            return self._m_color_peak

        _pos = self._io.pos()
        self._io.seek(self.offset_table.color_peak)
        self._m_color_peak = Vk4.TrueColorImage(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_color_peak', None)

    @property
    def color_light_thumbnail(self):
        if hasattr(self, '_m_color_light_thumbnail'):
            return self._m_color_light_thumbnail

        _pos = self._io.pos()
        self._io.seek(self.offset_table.color_light_thumbnail)
        self._m_color_light_thumbnail = Vk4.TrueColorImage(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_color_light_thumbnail', None)

    @property
    def assembly_header(self):
        if hasattr(self, '_m_assembly_header'):
            return self._m_assembly_header

        _pos = self._io.pos()
        self._io.seek(self.offset_table.assemble)
        self._m_assembly_header = Vk4.AssemblyHeader(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_assembly_header', None)

    @property
    def height_thumbnail(self):
        if hasattr(self, '_m_height_thumbnail'):
            return self._m_height_thumbnail

        _pos = self._io.pos()
        self._io.seek(self.offset_table.height_thumbnail)
        self._m_height_thumbnail = Vk4.TrueColorImage(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_height_thumbnail', None)

    @property
    def color_peak_thumbnail(self):
        if hasattr(self, '_m_color_peak_thumbnail'):
            return self._m_color_peak_thumbnail

        _pos = self._io.pos()
        self._io.seek(self.offset_table.color_peak_thumbnail)
        self._m_color_peak_thumbnail = Vk4.TrueColorImage(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_color_peak_thumbnail', None)

    @property
    def light_thumbnail(self):
        if hasattr(self, '_m_light_thumbnail'):
            return self._m_light_thumbnail

        _pos = self._io.pos()
        self._io.seek(self.offset_table.light_thumbnail)
        self._m_light_thumbnail = Vk4.TrueColorImage(self._io, self, self._root)
        self._io.seek(_pos)
        return getattr(self, '_m_light_thumbnail', None)


