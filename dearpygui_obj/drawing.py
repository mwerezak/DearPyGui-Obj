from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Optional, Any

from dearpygui import core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.data import DrawPropertyPos, DrawPropertyColorRGBA
from dearpygui_obj.wrapper.widget import PyGuiWidget
from dearpygui_obj.wrapper.drawing import DrawCommand, DrawProperty

if TYPE_CHECKING:
    from dearpygui_obj.data import Pos2D, ColorData

__all__ = [
    'DrawingCanvas',
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


class DrawLine(DrawCommand):
    """Draws a line."""

    p1: Pos2D = DrawPropertyPos()
    p2: Pos2D = DrawPropertyPos()
    color: ColorData = DrawPropertyColorRGBA()
    thickness: int = DrawProperty()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_line(self.canvas.id, tag=self.id, **draw_args)

class DrawCircle(DrawCommand):
    """Draws a circle."""

    center: Pos2D = DrawPropertyPos()
    radius: float = DrawProperty()
    color: ColorData = DrawPropertyColorRGBA()

    segments: int = DrawProperty()
    thickness: float = DrawProperty()
    fill: ColorData = DrawPropertyColorRGBA()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_circle(self.canvas.id, tag=self.id, **draw_args)