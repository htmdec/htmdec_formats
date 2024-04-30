import dataclasses
from typing import Mapping
import numpy as np


def cast_to_dataclass(cls, attrib: Mapping[str, str | float | bool | int]):
    new_attrib = {}
    for field in dataclasses.fields(cls):
        value = attrib[field.name.upper()]
        if not isinstance(value, field.type):
            value = field.type(value)
        new_attrib[field.name] = value
    return cls(**new_attrib)


@dataclasses.dataclass
class IndenterVar:
    name: str
    displayname: str
    formula: str
    decimals: int
    notation: str
    unitclass: str
    unittype: int
    defaultvalue: float
    minimumvalue: float
    maximumvalue: float
    defaultvaluei50: float
    minimumvaluei50: float
    maximumvaluei50: float
    defaultvaluei1k: float
    minimumvaluei1k: float
    maximumvaluei1k: float
    defaultvaluexp: float
    minimumvaluexp: float
    maximumvaluexp: float
    hasminimum: bool
    hasmaximum: bool
    actuatorspecific: bool
    canedit: bool
    doublevalue: float
    when: int
    reset: bool
    visibletoui: bool
    documentation: str
    stringvalue: str
    accumulator: np.ndarray
    statistics: np.ndarray


@dataclasses.dataclass
class IndenterTestInput:
    name: str
    displayname: str
    formula: str
    decimals: int
    notation: str
    unitclass: str
    unittype: int
    defaultvalue: float
    minimumvalue: float
    maximumvalue: float
    defaultvaluei50: float
    minimumvaluei50: float
    maximumvaluei50: float
    defaultvaluei1k: float
    minimumvaluei1k: float
    maximumvaluei1k: float
    defaultvaluexp: float
    minimumvaluexp: float
    maximumvaluexp: float
    hasminimum: bool
    hasmaximum: bool
    actuatorspecific: bool
    canedit: bool
    doublevalue: float
    when: int
    reset: bool
    visibletoui: bool
    documentation: str
    stringvalue: str


@dataclasses.dataclass
class IndenterCalculation:
    name: str
    displayname: str
    formula: str
    decimals: int
    notation: str
    unitclass: str
    unittype: int
    defaultvalue: float
    minimumvalue: float
    maximumvalue: float
    defaultvaluei50: float
    minimumvaluei50: float
    maximumvaluei50: float
    defaultvaluei1k: float
    minimumvaluei1k: float
    maximumvaluei1k: float
    defaultvaluexp: float
    minimumvaluexp: float
    maximumvaluexp: float
    hasminimum: bool
    hasmaximum: bool
    actuatorspecific: bool
    canedit: bool
    doublevalue: float
    when: int
    reset: bool
    visibletoui: bool
    documentation: str
    stringvalue: str


@dataclasses.dataclass
class IndenterSyschannel:
    name: str
    displayname: str
    formula: str
    decimals: int
    notation: str
    unitclass: str
    unittype: int
    defaultvalue: float
    minimumvalue: float
    maximumvalue: float
    defaultvaluei50: float
    minimumvaluei50: float
    maximumvaluei50: float
    defaultvaluei1k: float
    minimumvaluei1k: float
    maximumvaluei1k: float
    defaultvaluexp: float
    minimumvaluexp: float
    maximumvaluexp: float
    hasminimum: bool
    hasmaximum: bool
    actuatorspecific: bool
    canedit: bool
    doublevalue: float
    when: int
    reset: bool
    visibletoui: bool
    documentation: str
    stringvalue: str
    dataindex: int = -1


@dataclasses.dataclass
class IndenterChannel:
    name: str
    displayname: str
    formula: str
    decimals: int
    notation: str
    unitclass: str
    unittype: int
    defaultvalue: float
    minimumvalue: float
    maximumvalue: float
    defaultvaluei50: float
    minimumvaluei50: float
    maximumvaluei50: float
    defaultvaluei1k: float
    minimumvaluei1k: float
    maximumvaluei1k: float
    defaultvaluexp: float
    minimumvaluexp: float
    maximumvaluexp: float
    hasminimum: bool
    hasmaximum: bool
    actuatorspecific: bool
    canedit: bool
    doublevalue: float
    when: int
    reset: bool
    visibletoui: bool
    documentation: str
    stringvalue: str
    dataindex: int = -1


@dataclasses.dataclass
class IndenterSample:
    name: str
    folder: str
    templatename: str
    methodfolder: str
    uniqueid: str
    protected: bool
    savedver: str
    supportfasttest: bool
    supportsingletest: bool
    supportmultisample: bool
    contactsurfacedistanceedit: bool
    contactsurfacevelocityedit: bool
    contactsurfacesensitivityedit: bool
    contactsurfaceadvanced: bool
    contactsurfacesensitivity: str
    contactsurfacevelocity: str
    contactsurfaceheight: str
    contactsurfacesensitivitydefault: str
    contactsurfacevelocitydefault: str
    contactsurfaceheightdefault: str
    contactsurface_advancedconfig: str
    maxdatapoints: int
    maxdatapointspertest: int
    maxdatapointstoplot: int
    maxtimepertest: float
    autoexportpath: str
    autoexportformat: str
    autoexport: bool
    blitz3d: bool
    blitz4d: bool
    surveyscan: bool


@dataclasses.dataclass
class IndenterChannelBins:
    name: str
    unitclass: str
    unittype: int
    bins: np.ndarray
