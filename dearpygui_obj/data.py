from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, NamedTuple

from dearpygui_obj.wrapper.widget import ConfigProperty
from dearpygui_obj.wrapper.drawing import DrawProperty, DrawCommand

if TYPE_CHECKING:
    from typing import Any, List
    from dearpygui_obj.wrapper.widget import PyGuiWidget, ItemConfigData
    from dearpygui_obj.wrapper.drawing import DrawConfigData

## Colors

def color_from_rgba8(r: float, g: float, b: float, a: float = 255.0) -> ColorRGBA:
    """Create a :class:`.ColorRGBA` from 0-255 channel values."""
    return ColorRGBA(r/255.0, g/255.0, b/255.0, a/255.0)

def color_from_hex(color: str) -> ColorRGBA:
    """Create a :class:`.ColorRGBA` from a hex color string.

    Supported formats (The "#" and alpha channel are optional):

    - "[#]RGB[A]" (hex shorthand format)
    - "[#]RRGGBB[AA]"
    """
    color = color.lstrip('#')

    strlen = len(color)
    if strlen == 3 or strlen == 4:
        values = (c*2 for c in color)  # hex shorthand format
    elif strlen == 6 or strlen == 8:
        values = (color[i:i+2] for i in range(0, strlen, 2))
    else:
        raise ValueError("invalid hex string length")

    return color_from_rgba8(*(int(value, 16) for value in values))


class ColorRGBA(NamedTuple):
    """RGBA color data.

    Values should be expressed in the range between 0.0 and 1.0. The alpha value is optional.
    """
    r: float  #: red channel
    g: float  #: green channel
    b: float  #: blue channel
    a: float = 1.0  #: alpha channel

    def dpg_export(self) -> List[float]:
        """Get DPG color data (list of floats) from this ColorRGBA."""
        return [ min(max(0.0, 255.0 * value), 255.0) for value in self ]

    @classmethod
    def dpg_import(cls, colorlist: List[float]) -> ColorRGBA:
        """Create a ColorRGBA from DPG color data."""
        return ColorRGBA(*(min(max(0.0, value / 255.0), 1.0) for value in colorlist))

class ConfigPropertyColorRGBA(ConfigProperty):
    def get_value(self, instance: PyGuiWidget) -> Any:
        return ColorRGBA.dpg_import(instance.get_config()[self.key])
    def get_config(self, instance: PyGuiWidget, value: ColorRGBA) -> ItemConfigData:
        return {self.key : value.dpg_export()}

class DrawPropertyColorRGBA(DrawProperty):
    def get_value(self, instance: PyGuiWidget) -> Any:
        return ColorRGBA.dpg_import(instance.get_config()[self.key])
    def get_config(self, instance: PyGuiWidget, value: ColorRGBA) -> DrawConfigData:
        return {self.key : value.dpg_export()}


Pos2D = Tuple[float, float]  #: Type alias for 2D position data

class DrawPos(NamedTuple):
    """2D position data used for drawing."""
    x: float  #: x coordinate
    y: float  #: y coordinate

class DrawPropertyPos(DrawProperty):
    def get_value(self, instance: DrawCommand) -> DrawPos:
        return DrawPos(*instance.get_config()[self.key])
    def get_config(self, instance: DrawCommand, value: Pos2D) -> DrawConfigData:
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
    'color_from_rgba8',
    'color_from_hex',
    'ColorRGBA',
    'ConfigPropertyColorRGBA',
    'DrawPropertyColorRGBA',
    'DrawPos',
    'DrawPropertyPos',
]