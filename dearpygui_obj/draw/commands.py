from __future__ import annotations

from typing import TYPE_CHECKING

from dearpygui import core as dpgcore

from dearpygui_obj.draw.wrapper import DrawProperty, DrawCommand
from dearpygui_obj.data import DrawPropertyPos, DrawPropertyColorRGBA

if TYPE_CHECKING:
    from dearpygui_obj.data import Pos2D, ColorData


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
