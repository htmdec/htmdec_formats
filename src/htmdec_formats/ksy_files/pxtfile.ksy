meta:
  id: pxtfile
  file-extension: pxtfile
  endian: le
seq:
  - id: unk1
    type: u2
  - id: unk2
    type: u2
  - id: unk3
    type: u4
  - id: unk4
    type: u2
  - id: unk5
    type: u2
  - id: wave_size
    type: u4
  - id: wave
    type: wave_data
    size: wave_size + 40
  - id: unk7
    type: u4
    repeat: expr
    repeat-expr: 4
  - id: metadata
    type: str
    encoding: utf-8
    size-eos: true
types:
  wave_data:
    seq:
      - id: unk0
        type: u4
        repeat: expr
        repeat-expr: 21
      - id: name
        type: str
        encoding: utf-8
        size: 40
      - id: num_rows
        type: u4
      - id: num_cols
        type: u4
      - id: num_layers
        type: u4
      - id: unk1
        type: u4
      - id: row_delta
        type: f8
      - id: col_delta
        type: f8
      - id: layer_delta
        type: f8
      - id: unk2
        type: f8
      - id: row_start
        type: f8
      - id: col_start
        type: f8
      - id: layer_start
        type: f8
      - id: unk4
        type: f8
      - id: unk5
        type: f4
        repeat: expr
        repeat-expr: 39
      - id: layers
        repeat: expr
        repeat-expr: "num_layers > 0 ? num_layers : 1"
        type: layer
  layer:
    seq:
      - id: value
        type: f4
        repeat: expr
        repeat-expr: "(_parent.num_rows > 0 ? _parent.num_rows : 1) * (_parent.num_cols > 0 ? _parent.num_cols : 1)"
