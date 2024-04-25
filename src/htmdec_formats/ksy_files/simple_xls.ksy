meta:
  id: simple_xls
  file-extension: xls
  endian: le
seq:
  - id: header
    size: 8
  - id: cells
    type: cell
    repeat: until
    repeat-until: _.rec_type == record_types::eof
types:
  cell:
    seq:
      - id: rec_type
        type: u2
        enum: record_types
      - id: substream_length
        type: u2
      - id: record_value
        type:
          switch-on: rec_type
          cases:
            record_types::string_cell: string_cell
            record_types::number_cell: number_cell
            record_types::eof: eof_cell
  cell_header:
    seq:
      - id: rw
        type: u2
      - id: col
        type: u2
      - id: ixfe
        type: u2
  eof_cell:
    seq: []
  string_cell:
    seq:
      - id: header
        type: cell_header
      - id: nbytes
        type: u1
      - id: length
        type: u1
      - id: value
        type: str
        encoding: cp437
        size: length
  number_cell:
    seq:
      - id: header
        type: cell_header
      - id: unk1
        type: u1
      - id: value
        type: f8
enums:
  record_types:
    4: string_cell
    3: number_cell
    10: eof
