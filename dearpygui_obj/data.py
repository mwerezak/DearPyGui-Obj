from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from dearpygui_obj.wrapper.widget import ConfigProperty
from dearpygui_obj.wrapper.drawing import DrawProperty, DrawCommand

if TYPE_CHECKING:
    from typing import Any, Sequence, List, Tuple
    from dearpygui_obj.wrapper.widget import PyGuiWidget, ItemConfigData
    from dearpygui_obj.wrapper.drawing import DrawConfigData

## Colors

def color_from_rgba8(r: float, g: float, b: float, a: float = 255.0) -> ColorRGBA:
    return ColorRGBA(r/255.0, g/255.0, b/255.0, a/255.0)

def color_from_hex(color: str) -> ColorRGBA:
    color = color.lstrip('#')

    strlen = len(color)
    if strlen == 3 or strlen == 4:
        values = tuple(color)
    elif strlen == 6:
        values = color[0:2], color[2:4], color[4:6]
    elif strlen == 8:
        values = color[0:2], color[2:4], color[4:6], color[6:8]
    else:
        raise ValueError("invalid hex string length")

    return color_from_rgba8(*(int(value, 16) for value in values))

if TYPE_CHECKING:
    ColorData = Sequence[float]

class ColorRGBA(NamedTuple):
    """RGBA color data.

    Values should be expressed in the range between 0.0 and 1.0. The alpha value is optional.
    """
    r: float
    g: float
    b: float
    a: float = 1.0

    def dpg_export(self) -> List[float]:
        return [ min(max(0.0, 255.0 * value), 255.0) for value in self ]

    @classmethod
    def dpg_import(cls, colorlist: List[float]) -> ColorRGBA:
        return ColorRGBA(*(min(max(0.0, value / 255.0), 1.0) for value in colorlist))

class ConfigPropertyColorRGBA(ConfigProperty):
    def get_value(self, instance: PyGuiWidget) -> Any:
        return ColorRGBA.dpg_import(instance.get_config()[self.key])
    def get_config(self, instance: PyGuiWidget, value: ColorData) -> ItemConfigData:
        return {self.key : ColorRGBA(*value).dpg_export()}

class DrawPropertyColorRGBA(DrawProperty):
    def get_value(self, instance: PyGuiWidget) -> Any:
        return ColorRGBA.dpg_import(instance.get_config()[self.key])
    def get_config(self, instance: PyGuiWidget, value: ColorData) -> DrawConfigData:
        return {self.key : ColorRGBA(*value).dpg_export()}


if TYPE_CHECKING:
    Pos2D = Tuple[float, float]

class DrawPos(NamedTuple):
    x: float
    y: float

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