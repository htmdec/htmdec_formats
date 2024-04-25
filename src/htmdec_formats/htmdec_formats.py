"""Main module."""

import sys
from typing import Mapping
import itertools

try:
    from .ksy_files.nmdfile import Nmdfile
    from .ksy_files.simple_xls import SimpleXls
except ImportError as e:
    print(f"Error: {e}")
    print("Please run 'make install' to install the necessary dependencies.")
    sys.exit(1)

from .indenter_types import (
    IndenterVar,
    IndenterTestInput,
    IndenterCalculation,
    IndenterSyschannel,
    IndenterChannel,
    cast_to_dataclass,
)
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import base64


class IndenterDataset:
    nmd_file: Nmdfile
    _xml_tree: ET.ElementTree
    result_vars: dict[str, "IndenterVar"]
    tests: list["IndenterTest"]

    def __init__(self, nmd_file: Nmdfile):
        self.nmd_file = nmd_file
        self._load_xml()
        self._load_tests()

    def _load_xml(self):
        self._xml_tree = ET.ElementTree(ET.fromstring(self.nmd_file.xml.contents))
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

    @staticmethod
    def from_filename(filename: str) -> "IndenterDataset":
        """Creates an IndenterDataset object from a .nmd file."""
        with open(filename, "rb") as f:
            filebytes = f.read()
        nmd: Nmdfile = Nmdfile.from_bytes(filebytes)
        return IndenterDataset(nmd)

    def to_df(self) -> pd.DataFrame:
        """Converts a .nmd file to a pandas DataFrame."""
        df: pd.DataFrame = pd.DataFrame(self.buffers)
        return df


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

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.arrays)

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
