from __future__ import annotations
from typing import TYPE_CHECKING

from dearpygui import core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.data import DrawPos, DrawPropertyPos, DrawPropertyColorRGBA
from dearpygui_obj.wrapper.widget import Widget, ItemWidget
from dearpygui_obj.wrapper.drawing import DrawCommand, DrawProperty

if TYPE_CHECKING:
    from typing import Any, Optional, Tuple, Sequence
    from dearpygui_obj.data import Pos2D, ColorRGBA


@_register_item_type('mvAppItemType::Drawing')
class DrawingCanvas(Widget, ItemWidget):
    """A widget that displays the result of drawing commands."""

    def __init__(self, size: Tuple[int, int] = (300, 300), *, name_id: str = None, **config):
        super().__init__(size=size, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_drawing(self.id, **dpg_args)

    def clear(self) -> None:
        """Clears the drawing.

        Warning:
            Any :class:`.DrawCommand` objects created using this canvas must not be used after this
            method is called.

            This includes reading or writing to any properties of :class:`DrawCommand` objects.
        """
        dpgcore.clear_drawing(self.id)

    def get_mouse_pos(self) -> Optional[Tuple[int, int]]:
        """Get the mouse position within the drawing, or ``None`` if the drawing is not hovered."""
        if not self.is_hovered():
            return None
        return dpgcore.get_drawing_mouse_pos()

    def draw_line(self, p1: Pos2D, p2: Pos2D, color: ColorRGBA, thickness: int) -> DrawLine:
        """See :class:`.DrawLine`"""
        return DrawLine(self, p1, p2, color, thickness)

    def draw_rectangle(self, pmin: Pos2D, pmax: Pos2D, color: ColorRGBA, **kwargs: Any) -> DrawRectangle:
        """See :class:`.DrawRectangle` for keyword arguments."""
        return DrawRectangle(self, pmin, pmax, color, **kwargs)

    def draw_circle(self, center: Pos2D, radius: float, color: ColorRGBA, **kwargs: Any) -> DrawCircle:
        """See :class:`.DrawCircle` for keyword arguments."""
        return DrawCircle(self, center, radius, color, **kwargs)

    def draw_text(self, pos: Pos2D, text: str, **kwargs) -> DrawText:
        """See :class:`.DrawText` for keyword arguments."""
        return DrawText(self, pos, text, **kwargs)

    def draw_arrow(self, p1: Pos2D, p2: Pos2D, color: ColorRGBA, thickness: int, arrow_size: int) -> DrawArrow:
        """See :class:`.DrawArrow` for keyword arguments."""
        return DrawArrow(self, p1, p2, color, thickness, arrow_size)

    def draw_polyline(self, points: Sequence[Pos2D], color: ColorRGBA, **kwargs: Any) -> DrawPolyLine:
        """See :class:`.DrawPolyLine` for keyword arguments."""
        return DrawPolyLine(self, points, color, **kwargs)

    def draw_triangle(self, p1: Pos2D, p2: Pos2D, p3: Pos2D, color: ColorRGBA, **kwargs: Any) -> DrawTriangle:
        """See :class:`.DrawTriangle` for keyword arguments."""
        return DrawTriangle(self, p1, p2, p3, color, **kwargs)

    def draw_quad(self, p1: Pos2D, p2: Pos2D, p3: Pos2D, p4: Pos2D, color: ColorRGBA, **kwargs: Any) -> DrawQuad:
        """See :class:`.DrawQuod` for keyword arguments."""
        return DrawQuad(self, p1, p2, p3, p4, color, **kwargs)

    def draw_polygon(self, points: Sequence[Pos2D], color: ColorRGBA, **kwargs) -> DrawPolygon:
        """See :class:`.DrawPolygon` for keyword arguments."""
        return DrawPolygon(self, points, color, **kwargs)

    def draw_bezier_curve(self, p1: Pos2D, p2: Pos2D, p3: Pos2D, p4: Pos2D, color: ColorRGBA, **kwargs: Any) -> DrawBezierCurve:
        """See :class:`.DrawBezierCurve` for keyword arguments."""
        return DrawBezierCurve(self, p1, p2, p3, p4, color, **kwargs)

class DrawLine(DrawCommand):
    """Draws a line."""

    p1: Pos2D = DrawPropertyPos()
    p2: Pos2D = DrawPropertyPos()
    color: ColorRGBA = DrawPropertyColorRGBA()
    thickness: int = DrawProperty()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_line(self.canvas.id, tag=self.id, **draw_args)

class DrawRectangle(DrawCommand):
    """Draws a rectangle."""

    pmin: Pos2D = DrawPropertyPos()
    pmax: Pos2D = DrawPropertyPos()
    color: ColorRGBA = DrawPropertyColorRGBA()

    fill: ColorRGBA = DrawPropertyColorRGBA()
    rounding: float = DrawProperty()
    thickness: float = DrawProperty()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_rectangle(self.canvas.id, tag=self.id, **draw_args)

class DrawCircle(DrawCommand):
    """Draws a circle."""

    center: Pos2D = DrawPropertyPos()
    radius: float = DrawProperty()
    color: ColorRGBA = DrawPropertyColorRGBA()

    segments: int = DrawProperty()
    thickness: float = DrawProperty()
    fill: ColorRGBA = DrawPropertyColorRGBA()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_circle(self.canvas.id, tag=self.id, **draw_args)

class DrawText(DrawCommand):
    """Draws text."""

    pos: Pos2D = DrawPropertyPos()
    text: str = DrawProperty()

    color: ColorRGBA = DrawPropertyColorRGBA()
    font_size: int = DrawProperty(key='size')

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_text(self.canvas.id, tag=self.id, **draw_args)

class DrawArrow(DrawCommand):
    """Draw a line with an arrowhead."""

    p1: Pos2D = DrawPropertyPos()
    p2: Pos2D = DrawPropertyPos()
    color: ColorRGBA = DrawPropertyColorRGBA()
    thickness: int = DrawProperty()
    arrow_size: int = DrawProperty(key='size')

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_arrow(self.canvas.id, tag=self.id, **draw_args)

class DrawPolyLine(DrawCommand):
    """Draws connected lines."""

    @DrawProperty()
    def points(self) -> Sequence[Pos2D]:
        return [ DrawPos(*p) for p in self.get_config()['points'] ]

    @points.getconfig
    def points(self, value: Sequence[Pos2D]):
        return { 'points' : [ list(p) for p in value ] }

    color: ColorRGBA = DrawPropertyColorRGBA()

    closed: bool = DrawProperty()
    thickness: float = DrawProperty()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_polyline(self.canvas.id, tag=self.id, **draw_args)

class DrawTriangle(DrawCommand):
    """Draws a triangle."""

    p1: Pos2D = DrawPropertyPos()
    p2: Pos2D = DrawPropertyPos()
    p3: Pos2D = DrawPropertyPos()
    color: ColorRGBA = DrawPropertyColorRGBA()

    fill: ColorRGBA = DrawPropertyColorRGBA()
    thickness: float = DrawProperty()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_triangle(self.canvas.id, tag=self.id, **draw_args)

class DrawQuad(DrawCommand):
    """Draws a quadrilateral."""

    p1: Pos2D = DrawPropertyPos()
    p2: Pos2D = DrawPropertyPos()
    p3: Pos2D = DrawPropertyPos()
    p4: Pos2D = DrawPropertyPos()
    color: ColorRGBA = DrawPropertyColorRGBA()

    fill: ColorRGBA = DrawPropertyColorRGBA()
    thickness: float = DrawProperty()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_quad(self.canvas.id, tag=self.id, **draw_args)

class DrawPolygon(DrawCommand):
    """Draws a polygon."""

    @DrawProperty()
    def points(self) -> Sequence[Pos2D]:
        return [ DrawPos(*p) for p in self.get_config()['points'] ]

    @points.getconfig
    def points(self, value: Sequence[Pos2D]):
        return { 'points' : [ list(p) for p in value ] }

    color: ColorRGBA = DrawPropertyColorRGBA()

    fill: ColorRGBA = DrawPropertyColorRGBA()
    thickness: float = DrawProperty()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_polygon(self.canvas.id, tag=self.id, **draw_args)

class DrawBezierCurve(DrawCommand):
    """Draws a bezier curve."""

    p1: Pos2D = DrawPropertyPos()
    p2: Pos2D = DrawPropertyPos()
    p3: Pos2D = DrawPropertyPos()
    p4: Pos2D = DrawPropertyPos()
    color: ColorRGBA = DrawPropertyColorRGBA()

    thickness: float = DrawProperty()
    segments: int = DrawProperty()

    def _draw_internal(self, draw_args) -> None:
        dpgcore.draw_bezier_curve(self.canvas.id, tag=self.id, **draw_args)

## class DrawImage TODO

__all__ = [
    'DrawingCanvas',
    'DrawLine',
    'DrawRectangle',
    'DrawCircle',
    'DrawText',
    'DrawArrow',
    'DrawPolyLine',
    'DrawTriangle',
    'DrawQuad',
    'DrawPolygon',
    'DrawBezierCurve',
]