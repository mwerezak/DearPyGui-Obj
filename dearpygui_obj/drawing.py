from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Optional, Any

from dearpygui import core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper import PyGuiWidget
from dearpygui_obj.draw.commands import DrawLine, DrawCircle

if TYPE_CHECKING:
    from dearpygui_obj.data import Pos2D, ColorData

__all__ = [
    'DrawingCanvas',
    'DrawLine',
    'DrawCircle',
]

@_register_item_type('mvAppItemType::Drawing')
class DrawingCanvas(PyGuiWidget):
    """A widget that displays the result of drawing commands."""

    def __init__(self, size: Tuple[int, int] = (300, 300), *, name_id: str = None, **config):
        super().__init__(size=size, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_drawing(self.id, **dpg_args)

    def clear(self) -> None:
        """Clears the drawing.

        Warning:
            Any :class:`DrawCommand` objects created using this canvas must not be used after this
            method is called.

            This includes reading or writing to any properties of :class:`DrawCommand` objects.
        """
        dpgcore.clear_drawing(self.id)

    def get_mouse_pos(self) -> Optional[Tuple[int, int]]:
        """Get the mouse position within the drawing, or ``None`` if the drawing is not hovered."""
        if not self.is_hovered():
            return None
        return dpgcore.get_drawing_mouse_pos()

    def draw_line(self, p1: Pos2D, p2: Pos2D, color: ColorData, thickness: int) -> DrawLine:
        return DrawLine(self, p1, p2, color, thickness)

    def draw_circle(self, center: Pos2D, radius: float, color: ColorData, **kwargs: Any) -> DrawCircle:
        return DrawCircle(self, center, radius, color, **kwargs)