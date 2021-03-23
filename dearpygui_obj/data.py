from __future__ import annotations

import string
from typing import TYPE_CHECKING, Tuple, NamedTuple

from dearpygui_obj.wrapper.widget import ConfigProperty
from dearpygui_obj.wrapper.drawing import DrawProperty, DrawCommand

if TYPE_CHECKING:
    from typing import Any, List, Iterable, Union
    from dearpygui_obj.wrapper.widget import Widget, ItemConfigData
    from dearpygui_obj.wrapper.drawing import DrawConfigData

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

class DrawPropertyColorRGBA(DrawProperty):
    def fvalue(self, instance: Widget) -> Any:
        return dpg_import_color(instance.get_config()[self.key])
    def fconfig(self, instance: Widget, value: ColorRGBA) -> DrawConfigData:
        return {self.key : dpg_export_color(value)}


Pos2D = Tuple[float, float]  #: Type alias for 2D position data

class DrawPos(NamedTuple):
    """2D position data used for drawing."""
    x: float  #: x coordinate
    y: float  #: y coordinate

class DrawPropertyPos(DrawProperty):
    def fvalue(self, instance: DrawCommand) -> DrawPos:
        return DrawPos(*instance.get_config()[self.key])
    def fconfig(self, instance: DrawCommand, value: Pos2D) -> DrawConfigData:
        return {self.key : list(value)}


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
    'DrawPropertyColorRGBA',
    'DrawPos',
    'DrawPropertyPos',
]


