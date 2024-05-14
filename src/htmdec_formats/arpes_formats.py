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

    def __init__(self, pxt_file: KaitaiPxtfile):
        self.pxt_file = pxt_file
        for attr in ["row", "col", "layer"]:
            setattr(self, f"num_{attr}s", getattr(pxt_file.wave, f"num_{attr}s"))
            setattr(self, f"{attr}_start", getattr(pxt_file.wave, f"{attr}_start"))
            setattr(self, f"{attr}_delta", getattr(pxt_file.wave, f"{attr}_delta"))
        self.array_data = np.reshape(
            [_.value for _ in pxt_file.wave.layers],
            (self.num_layers, self.num_cols, self.num_rows),
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
