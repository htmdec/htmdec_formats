# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
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

    class Blank(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    class LightInfo(KaitaiStruct):
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
                return self._m_value if hasattr(self, '_m_value') else None

            _pos = self._io.pos()
            self._io.seek(self.root_pos)
            self._m_value = self._io.read_u1()
            self._io.seek(_pos)
            return self._m_value if hasattr(self, '_m_value') else None


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
            self.reserved1 = [None] * (3)
            for i in range(3):
                self.reserved1[i] = self._io.read_u4le()

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
            self.reserved3 = [None] * (5)
            for i in range(5):
                self.reserved3[i] = self._io.read_u4le()

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
                raise kaitaistruct.ValidationNotAnyOfError(self.bit_depth, self._io, u"/types/data_image/seq/2")
            self.compression = self._io.read_u4le()
            self.byte_size = self._io.read_u4le()
            self.palette_range_min = self._io.read_u4le()
            self.palette_range_max = self._io.read_u4le()
            self.palette = [None] * (768)
            for i in range(768):
                self.palette[i] = self._io.read_u4le()

            self.data = self._io.read_bytes(self.byte_size)

        @property
        def bps(self):
            if hasattr(self, '_m_bps'):
                return self._m_bps if hasattr(self, '_m_bps') else None

            self._m_bps = (self.bit_depth >> 3)
            return self._m_bps if hasattr(self, '_m_bps') else None


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
            self.light = [None] * (3)
            for i in range(3):
                self.light[i] = self._io.read_u4le()

            self.height = [None] * (3)
            for i in range(3):
                self.height[i] = self._io.read_u4le()

            self.color_peak_thumbnail = self._io.read_u4le()
            self.color_thumbnail = self._io.read_u4le()
            self.light_thumbnail = self._io.read_u4le()
            self.height_thumbnail = self._io.read_u4le()
            self.assemble = self._io.read_u4le()
            self.line_measure = self._io.read_u4le()
            self.line_thickness = self._io.read_u4le()
            self.string_data = self._io.read_u4le()
            self.reserved = self._io.read_u4le()


    @property
    def assembly_header(self):
        if hasattr(self, '_m_assembly_header'):
            return self._m_assembly_header if hasattr(self, '_m_assembly_header') else None

        _pos = self._io.pos()
        self._io.seek(self.offset_table.assemble)
        self._m_assembly_header = Vk4.AssemblyHeader(self._io, self, self._root)
        self._io.seek(_pos)
        return self._m_assembly_header if hasattr(self, '_m_assembly_header') else None

    @property
    def lights(self):
        if hasattr(self, '_m_lights'):
            return self._m_lights if hasattr(self, '_m_lights') else None

        self._m_lights = [None] * (len(self.offset_table.light))
        for i in range(len(self.offset_table.light)):
            _on = self.offset_table.light[i] > 0
            if _on == True:
                self._m_lights[i] = Vk4.LightInfo(self.offset_table.light[i], self._io, self, self._root)
            elif _on == False:
                self._m_lights[i] = Vk4.Blank(self._io, self, self._root)

        return self._m_lights if hasattr(self, '_m_lights') else None


