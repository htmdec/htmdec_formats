"""Main module."""

import sys

try:
    from .ksy_files.nmdfile import Nmdfile
    from .ksy_files.simple_xls import SimpleXls
except ImportError as e:
    print(f"Error: {e}")
    print("Please run 'make install' to install the necessary dependencies.")
    sys.exit(1)

import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET


class IndenterDataset:
    nmd_file: Nmdfile
    buffers: dict[str, np.ndarray]
    _xml_tree: ET.Element

    def __init__(self, nmd_file: Nmdfile):
        self.nmd_file = nmd_file
        self._xml_tree = ET.fromstring(nmd_file.xml.contents)
        self._load_buffers()

    def _load_buffers(self):
        self.buffers = {}
        for i, seq in enumerate(self.nmd_file.data.variables):
            self.buffers[f"seq_{i:04d}"] = np.frombuffer(seq.values, dtype="<f8")

    @staticmethod
    def from_filename(filename: str) -> "IndenterDataset":
        """Creates an IndenterDataset object from a .nmd file."""
        nmd: Nmdfile = Nmdfile.from_file(filename)
        return IndenterDataset(nmd)

    def to_df(self) -> pd.DataFrame:
        """Converts a .nmd file to a pandas DataFrame."""
        df: pd.DataFrame = pd.DataFrame(self.buffers)
        return df
