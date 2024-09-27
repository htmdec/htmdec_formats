"""
Formats for the ARPES data, specifically their sub-dialect of pxt
"""

import sys

try:
    from .ksy_files.pxtfile import Pxtfile as KaitaiPxtfile
except ImportError as e:
    print(f"Error: {e}")
    print("Please run 'make install' to install the necessary dependencies.")
    sys.exit(1)

import numpy as np
import pandas as pd
from typing import Optional
import configparser
import re
import io


class ARPESDataset:
    pxt_file: KaitaiPxtfile
    num_rows: int
    num_cols: int
    num_layers: int

    row_start: float
    col_start: float
    layer_start: float

    row_delta: float
    col_delta: float
    layer_delta: float

    _metadata: str
    metadata: configparser.ConfigParser
    dims: str

    def __init__(self, pxt_file: KaitaiPxtfile):
        self.pxt_file = pxt_file
        for attr in ["row", "col", "layer"]:
            setattr(self, f"num_{attr}s", getattr(pxt_file.wave, f"num_{attr}s"))
            setattr(self, f"{attr}_start", getattr(pxt_file.wave, f"{attr}_start"))
            setattr(self, f"{attr}_delta", getattr(pxt_file.wave, f"{attr}_delta"))
        self.array_data = np.reshape(
            [_.value for _ in pxt_file.wave.layers],
            (max(self.num_layers, 1), self.num_cols, self.num_rows),
        )

        if "\r\r" in pxt_file.metadata:
            md, self.dims = pxt_file.metadata.rsplit("\r\r", 1)
        else:
            md = pxt_file.metadata
            self.dims = ""
        # The 'Run Mode Information' section is not "standard" as it is set up
        # such that each line is an entry in the list, where the first element
        # is usually an integer index and the rest are things like x, y, z,
        # theta, phi.  So we can't use use splitlines -- as of 3.2, it includes
        # \v , which is used as a delimiter in the metadata.
        # This is not ideal, so we go back in and fix it up.
        self._metadata = "\n".join(re.split("\n|\r", md))
        self.metadata = configparser.ConfigParser(delimiters=["=", chr(0x0b)])
        self.metadata.read_string(self._metadata)
        # Now we're going to fix up the 'Run Mode Information' section by
        # removing it from the config parser and adding it to the top-level
        # class attributes here.
        self.metadata.pop("Run Mode Information", {})
        # We go back to our original data to find the run mode information and
        # turn that into usable information.
        rmi_string = "\n".join(line for line in self._metadata.split("\n") if "\x0b" in line)
        self.run_mode_info = pd.read_csv(
            io.StringIO(rmi_string), sep="\x0b"
        )

    @property
    def bounds(self):
        return np.array(
            [
                [
                    self.layer_start,
                    self.layer_start + self.layer_delta * self.num_layers,
                ],
                [
                    self.col_start,
                    self.col_start + self.col_delta * self.num_cols,
                ],
                [
                    self.row_start,
                    self.row_start + self.row_delta * self.num_rows,
                ],
            ]
        )

    @classmethod
    def from_file(cls, filename: str) -> "ARPESDataset":
        return cls(KaitaiPxtfile.from_file(filename))

    def get_layer(self, layer: int) -> np.ndarray:
        """This function returns a 2D numpy array of the data for a given layer.
        It is 1-indexed, not zero-indexed.."""
        if layer > self.num_layers or layer < 1:
            raise IndexError(f"Layer {layer} is out of bounds.")
        return self.array_data[layer - 1, :, :]

    def to_hdf5(self, filename: str):
        """Write the data to an HDF5 file."""
        import h5py

        with h5py.File(filename, "w") as f:
            dataset = f.create_dataset("data", data=self.array_data)
            dataset.attrs["bounds"] = self.bounds
            dataset.attrs["dims"] = self.dims
            dataset.attrs["metadata"] = self._metadata
