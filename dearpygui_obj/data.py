from __future__ import annotations

import string
import datetime
import calendar
from datetime import date, time
from typing import TYPE_CHECKING, NamedTuple

from dearpygui_obj.wrapper.widget import ConfigProperty

if TYPE_CHECKING:
    from typing import Any, List, Iterable, Union, Mapping
    from dearpygui_obj.wrapper.widget import Widget, ItemConfigData


    number = Union[int, float]

## Colors

class ColorRGBA(NamedTuple):
    """RGBA color data.

    Values should be expressed in the range between 0 and 255 (since that's what DPG uses).
    The alpha value is optional.

    Using the :func:`.color_from_float`, :func:`.color_from_rgba8`, and :func:`.color_from_hex`
    constructor functions should be preferred over instantiating ColorRGBA tuples directly, as
    the internal representation may be subject to change."""
    r: number  #: red channel
    g: number  #: green channel
    b: number  #: blue channel
    a: number = 255  #: alpha channel

def color_from_float(r: float, g: float, b: float, a: float = 1.0) -> ColorRGBA:
    # noinspection PyArgumentList
    return ColorRGBA(r*255.0, g*255.0, b*255.0, a*255.0)

def color_from_rgba8(r: number, g: number, b: number, a: number = 255) -> ColorRGBA:
    """Create a :class:`.ColorRGBA` from 0-255 channel values."""
    # noinspection PyArgumentList
    return ColorRGBA(r, g, b, a)

def color_from_hex(color: str) -> ColorRGBA:
    """Create a :class:`.ColorRGBA` from a hex color string.

    Supported formats (The "#" and alpha channel are optional):

    - "[#]RGB[A]" (hex shorthand format)
    - "[#]RRGGBB[AA]"
    """

    # strip all non-hex characters from input
    hexstr = ''.join(c for c in color if c in string.hexdigits)
    hexlen = len(hexstr)
    if hexlen == 3 or hexlen == 4:
        values = (c*2 for c in hexstr)  # hex shorthand format
    elif hexlen == 6 or hexlen == 8:
        values = (hexstr[i:i+2] for i in range(0, hexlen, 2))
    else:
        raise ValueError("unsupported hex color format")

    return color_from_rgba8(*(int(value, 16) for value in values))

def dpg_import_color(colorlist: List[number]) -> ColorRGBA:
    """Create a ColorRGBA from DPG color data."""
    return ColorRGBA(*(min(max(0, value), 255) for value in colorlist))

def dpg_export_color(color: Iterable[number]) -> List[number]:
    """Convert a :class:`ColorRGBA`-like iterable into DPG color data (list of floats 0-255)"""
    return [min(max(0, value), 255) for value in color]

class ConfigPropertyColorRGBA(ConfigProperty):
    def fvalue(self, instance: Widget) -> Any:
        return dpg_import_color(instance.get_config()[self.key])
    def fconfig(self, instance: Widget, value: ColorRGBA) -> ItemConfigData:
        return {self.key : dpg_export_color(value)}

## Date/Time

MINYEAR = 1970 #: the smallest year number supported by DPG.
MAXYEAR = 2999 #: the largest year number supported by DPG.

def _clamp(value, min_val, max_val):
    return min(max(min_val, value), max_val)

def dpg_import_date(date_data: Mapping[str, int]) -> date:
    """Convert date data used by DPG into a :class:`~datetime.date` object."""
    year = _clamp(date_data.get('year', MINYEAR), datetime.MINYEAR, datetime.MAXYEAR)
    month = _clamp(date_data.get('month', 1), 1, 12)

    _, max_day = calendar.monthrange(year, month)
    day = _clamp(date_data.get('month_day', 1), 1, max_day)
    return date(year, month, day)

def dpg_export_date(date_val: date) -> Mapping:
    """Convert a :class:`date` into date data used by DPG.

    Unfortunately the range of year numbers supported by DPG is smaller than that of python.
    See the :data:`.MINYEAR` and :data:`.MAXYEAR` constants.

    If a date outside of the supported range is given, this function will still return a value,
    however that value may not produce desired results when supplied to DPG's date widgets
    (should get clamped)."""
    return {
        'month_day': date_val.day,
        'month': date_val.month,
        'year': date_val.year - 1900
    }


## Textures

# class TextureFormat(Enum):
#     """Texture format useds by DPG.
#
#     Values come from DPG's "mvTEX_XXXX_XXXXX" constants.
#     """
#     RGBA_INT   = 0
#     RGBA_FLOAT = 1
#     RGB_FLOAT  = 2
#     RGB_INT    = 3
#
__all__ = [
    'ColorRGBA',
    'color_from_float',
    'color_from_rgba8',
    'color_from_hex',
    'ConfigPropertyColorRGBA',
]


