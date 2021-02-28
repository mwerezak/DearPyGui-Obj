from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple, Protocol

import dearpygui.core as dpgcore
from dearpygui_obj import _generate_id

if TYPE_CHECKING:
    from typing import Any, List


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

