from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, NamedTuple

import dearpygui.core as dpgcore
from dearpygui_obj.wrapper import ConfigProperty

if TYPE_CHECKING:
    from typing import Any, List
    from dearpygui_obj.wrapper import PyGuiWidget, ItemConfigData

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

class ColorRGBA(NamedTuple):
    """RGBA color data.

    Values should be expressed in the range between 0.0 and 1.0. The alpha value is optional.
    """
    r: float
    g: float
    b: float
    a: float = 1.0

    def dpg_export(self) -> List[float]:
        return [ 255.0 * value for value in self ]

    @classmethod
    def dpg_import(cls, colorlist: List[float]) -> ColorRGBA:
        return ColorRGBA(*(value / 255.0 for value in colorlist))

class ConfigPropertyColorRGBA(ConfigProperty):
    """A ConfigProperty that accesses a ColorRGBA value by default."""

    def _get_value(self, instance: PyGuiWidget) -> Any:
        return ColorRGBA.dpg_import(instance.get_config()[self.key])

    def _get_config(self, instance: PyGuiWidget, value: Any) -> ItemConfigData:
        return {self.key : value.dpg_export()}

## Textures

class TextureFormat(Enum):
    """Texture format useds by DPG.

    Values come from DPG's "mvTEX_XXXX_XXXXX" constants.
    """
    RGBA_INT   = 0
    RGBA_FLOAT = 1
    RGB_FLOAT  = 2
    RGB_INT    = 3

