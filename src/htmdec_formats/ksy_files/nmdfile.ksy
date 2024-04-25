meta:
  id: nmdfile
  file-extension: "NMD"
  endian: le
seq:
  - id: sequence
    type: u4le
    repeat: expr
    repeat-expr: 837
  - id: unk
    size: 3
  - id: xml
    type: xml_section
    terminator: 0x00
  - id: padding
    contents: [0x00]
  - id: rest
    size-eos: true
instances:
  data:
    pos: 837*4 + 3 + _root.xml.raw_contents.length - 2
    type: datasets
types:
  xml_section:
    seq:
      - id: raw_contents
        size-eos: true
    instances:
      contents:
        pos: 0
        size: raw_contents.length - 2
        type: str
        encoding: utf-8
      rows:
        io: _root._io
        pos: raw_contents.length - 2 + 837*4 + 3
        type: variable_output
  datasets:
    seq:
      - id: variables
        type: variable_output
        repeat: eos
  variable_output:
    seq:
      - id: row_count
        type: u4le
      - id: values
        size: 8 * row_count
        #type: f8
        #repeat: expr
        #repeat-expr: row_count
