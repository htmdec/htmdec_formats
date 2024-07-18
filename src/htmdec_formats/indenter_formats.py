"""Main module."""

import sys
import itertools

try:
    from .ksy_files.nmdfile import Nmdfile as KaitaiNmdfile
    from .ksy_files.simple_xls import SimpleXls
except ImportError as e:
    print(f"Error: {e}")
    print("Please run 'make install' to install the necessary dependencies.")
    sys.exit(1)

from .utils.convert import (
    export_results_to_xlsx,
    export_inputs_to_xlsx,
    export_summary_to_xlsx,
    export_test_to_xlsx,
)
from .indenter_types import (
    IndenterVar,
    IndenterTestInput,
    IndenterCalculation,
    IndenterSyschannel,
    IndenterChannel,
    IndenterChannelBins,
    IndenterSample,
    cast_to_dataclass,
)
import pandas as pd
import numpy as np
import xlsxwriter
import xml.etree.ElementTree as ET
import base64


class XmlDummy:
    def __init__(self, contents: str):
        self.contents = contents


_DELIM_START = b"<SAMPLE"
_DELIM_END = b"</SAMPLE>"


class Nmdfile:
    # We are re-implementing this without using Kaitai so that we can improve
    # performance.  The kaitai wrapper was, and is, very useful.  However, with
    # our specific use case, where we rely on a delimiter to find the end of the
    # XML portion, it conducts a progressive "+=" concatenation to construct the
    # string.  For very long strings, like we have, this becomes extremely slow.
    def __init__(self, filename: str):
        # We will read the whole file into memory
        with open(filename, "rb") as f:
            file_contents = f.read()
        xml_start = file_contents.find(_DELIM_START)
        xml_end = file_contents.rfind(_DELIM_END) + len(_DELIM_END)
        self.unk = file_contents[837 * 4 : xml_start]
        self.xml = XmlDummy(file_contents[xml_start:xml_end].decode("utf-8"))
        assert file_contents[xml_end + 2 : xml_end + 4] == b"\x00\x00"

        self.data = KaitaiNmdfile.Datasets.from_bytes(file_contents[xml_end:])

    @classmethod
    def from_filename(cls, filename: str) -> "Nmdfile":
        return cls(filename)


class IndenterDataset:
    nmd_file: Nmdfile
    _xml_tree: ET.ElementTree
    result_vars: dict[str, "IndenterVar"]
    tests: list["IndenterTest"]
    metadata: IndenterSample
    sample_summary: "IndenterSampleSummary"

    def __init__(self, nmd_file: Nmdfile):
        self.nmd_file = nmd_file
        self._load_xml()
        self._load_tests()
        if self._xml_tree.find("Sample") is not None:
            self.metadata = cast_to_dataclass(
                IndenterSample, self._xml_tree.find("Sample").attrib
            )
        if self._xml_tree.find("SAMPLESUMMARY") is not None:
            self.sample_summary = IndenterSampleSummary(
                self._xml_tree.find("SAMPLESUMMARY")
            )

    def _load_xml(self):
        self._xml_tree = ET.ElementTree(ET.fromstring(self.nmd_file.xml.contents))
        ET.indent(self._xml_tree.getroot())
        results = {}
        for result in self._xml_tree.findall("RESULTS/Result") or []:
            stats = base64.b64decode(result.attrib["STATISTICS"])
            accum = base64.b64decode(result.attrib["ACCUMULATOR"])
            results[result.attrib["NAME"]] = {
                "statistics": np.frombuffer(stats, dtype="f8"),
                "accumulator": np.frombuffer(accum, dtype="f8"),
            }
        result_vars = {}
        for var in self._xml_tree.find("RESULTS/VarList") or []:
            attrib = var.attrib.copy()
            attrib["ACCUMULATOR"] = results[var.attrib["NAME"]]["accumulator"]
            attrib["STATISTICS"] = results[var.attrib["NAME"]]["statistics"]
            result_vars[attrib["NAME"]] = cast_to_dataclass(IndenterVar, attrib)
        self.result_vars = result_vars

    def _load_tests(self):
        buffers = []
        for seq in self.nmd_file.data.variables:
            buffers.append(np.frombuffer(seq.values, dtype="<f8"))
        self.tests = []
        for test in self._xml_tree.findall("TEST"):
            self.tests.append(IndenterTest(test, buffers))

    @classmethod
    def from_filename(cls, filename: str) -> "IndenterDataset":
        """Creates an IndenterDataset object from a .nmd file."""
        nmd: Nmdfile = Nmdfile.from_filename(filename)
        return cls(nmd)

    def to_df(self) -> pd.DataFrame:
        """Converts a .nmd file to a concatenated set of pandas DataFrames."""
        tests = []
        for i, test in enumerate(self.tests):
            test_df = test.to_df()
            test_df.insert(0, "TEST_NUM", i)
            test_df.insert(1, "UNIQUEID", test.unique_id)
            test_df.insert(2, "STARTTIME", test.start_time)
            tests.append(test_df)
        return pd.concat(tests)

    def to_csv(self, filename: str):
        self.to_df().to_csv(filename, index=False)

    def to_xlsx(self, filename: str):
        with xlsxwriter.Workbook(filename) as workbook:
            export_results_to_xlsx(self, workbook)
            export_inputs_to_xlsx(self, workbook, "Pre-Test Inputs")
            export_summary_to_xlsx(self, workbook)
            export_inputs_to_xlsx(self, workbook, "Post-Test Inputs")

            for test_index, test in enumerate(self.tests):
                export_test_to_xlsx(test, test_index, workbook)


class IndenterSampleSummary:
    startmarkername: str
    endmarkername: str
    normchanname: str
    channels: dict[str, IndenterChannelBins]

    def __init__(self, sample_xml_subtree: ET.Element):
        self.startmarkername = sample_xml_subtree.attrib["STARTMARKERNAME"]
        self.endmarkername = sample_xml_subtree.attrib["ENDMARKERNAME"]
        self.normchanname = sample_xml_subtree.attrib["NORMCHANNAME"]
        self.channels = {}
        for channel in sample_xml_subtree.findall("Channels/Channel") or []:
            bins = []
            for bin in channel.findall("Bins/Bin") or []:
                b = base64.b64decode(bin.attrib["VALUE"])
                bins.append(np.frombuffer(b, dtype="f8"))
            bins = np.array(bins)
            attrib = channel.attrib.copy()
            attrib["BINS"] = bins
            self.channels[attrib["NAME"]] = cast_to_dataclass(
                IndenterChannelBins, attrib
            )


class IndenterTest:
    start_time: str
    unique_id: str
    inputs: dict[str, IndenterTestInput]
    calculations: dict[str, IndenterCalculation]
    syschannels: dict[str, IndenterSyschannel]
    channels: dict[str, IndenterChannel]
    xml_subtree: ET.Element
    arrays: dict[str, np.ndarray]

    def __init__(self, test_xml_subtree: ET.Element, buffers: list[np.ndarray]):
        self.start_time = test_xml_subtree.attrib["STARTTIME"]
        self.unique_id = test_xml_subtree.attrib["UNIQUEID"]
        self.xml_subtree = test_xml_subtree
        self.inputs = self._parse_element_type("INPUT", IndenterTestInput)
        self.calculations = self._parse_element_type("CALCULATION", IndenterCalculation)
        self.syschannels = self._parse_element_type("SYSCHANNEL", IndenterSyschannel)
        self.channels = self._parse_element_type("CHANNEL", IndenterChannel)
        data_index_values = {}
        for key, value in self.syschannels.items():
            if value.dataindex != -1:
                data_index_values[value.dataindex] = key
        for key, value in self.channels.items():
            if value.dataindex != -1:
                data_index_values[value.dataindex] = key
        self.arrays = {}
        for i in sorted(data_index_values.keys()):
            self.arrays[data_index_values[i]] = buffers.pop(0)

    def get_fields(self):
        return list(
            itertools.chain(
                self.inputs, self.calculations, self.syschannels, self.channels
            )
        )

    def get_inputs(self):
        df = pd.DataFrame(self.inputs.values()).set_index("name")
        return df

    def get_channels(self):
        df = pd.DataFrame(self.channels.values()).set_index("name")
        return df

    def get_syschannels(self):
        df = pd.DataFrame(self.syschannels.values()).set_index("name")
        return df

    def get_calculations(self):
        df = pd.DataFrame(self.calculations.values()).set_index("name")
        return df

    def get_field(
        self, key
    ) -> IndenterTestInput | IndenterCalculation | IndenterSyschannel | IndenterChannel:
        if key in self.inputs:
            return self.inputs[key]
        elif key in self.calculations:
            return self.calculations[key]
        elif key in self.syschannels:
            return self.syschannels[key]
        elif key in self.channels:
            return self.channels[key]
        else:
            raise KeyError(key)

    def to_df(self, include_id=False) -> pd.DataFrame:
        df = pd.DataFrame(self.arrays)
        if include_id:
            df.insert(0, "UNIQUEID", self.unique_id)
            df.insert(1, "STARTTIME", self.start_time)
        return df

    def to_csv(self, filename: str):
        self.to_df().to_csv(filename, index=False)

    def _parse_element_type(self, etype: str, cls: type):
        result = {}
        for el in self.xml_subtree.findall(etype) or []:
            result[el.attrib["NAME"]] = cast_to_dataclass(cls, el.attrib)
        return result

    def __getitem__(self, key):
        return self.arrays[key]

    def __contains__(self, key):
        return key in self.arrays

    def __iter__(self):
        return iter(self.arrays)

    def __len__(self):
        return len(self.arrays)

    def keys(self):
        return self.arrays.keys()

    def values(self):
        return self.arrays.values()

    def items(self):
        return self.arrays.items()
