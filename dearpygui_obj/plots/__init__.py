from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, cast

import dearpygui.core as dpgcore

from dearpygui_obj import _register_item_type, _generate_id
from dearpygui_obj.data import ColorRGBA, export_color_to_dpg
from dearpygui_obj.wrapper.widget import Widget, ItemWidgetMx, ConfigProperty

if TYPE_CHECKING:
    from typing import Any, Optional, Union, Type, Tuple, Iterable
    from dearpygui_obj.plots.dataseries import DataSeries

    TickLabel = Tuple[str, float]
    PlotLimits = Tuple[float, float]
    YAxis = Union['PlotYAxis', 'PlotYAxisConfig']

## Plot Axis Configuration

class PlotAxisConfigProperty:
    def __set_name__(self, owner: Type[PlotAxisConfig], name: str):
        self.key = '_' + name

    def __get__(self, config: Optional[PlotAxisConfig], owner: Type[PlotAxisConfig]) -> Any:
        if config is None:
            return self
        config_key = config.axis.key + self.key
        return config.plot.get_config()[config_key]

    def __set__(self, config: PlotAxisConfig, value: Any) -> None:
        config_key = config.axis.key + self.key
        config.plot.set_config(**{config_key : value})

class PlotAxisConfig:
    """Container for axis configuration properties.

    This class can be used to modify the configuration of a single axis of a :class:`.Plot`.
    """
    no_gridlines: bool = PlotAxisConfigProperty()
    no_tick_marks: bool = PlotAxisConfigProperty()
    no_tick_labels: bool = PlotAxisConfigProperty()
    log_scale: bool = PlotAxisConfigProperty()
    invert: bool = PlotAxisConfigProperty()
    lock_min: bool = PlotAxisConfigProperty()
    lock_max: bool = PlotAxisConfigProperty()

    def __init__(self, plot: Plot, axis: PlotAxis):
        self.plot = plot
        self.axis = axis

class PlotXAxisConfig(PlotAxisConfig):
    """Configuration container for plot X-axis."""
    axis: PlotXAxis

    time: bool = PlotAxisConfigProperty()

class PlotYAxisConfig(PlotAxisConfig):
    """Configuration container for plot Y-axis."""
    axis: PlotYAxis

class PlotOptYAxisConfig(PlotYAxisConfig):
    """Configuration container for optional Y-axes.

    This class is similar to :class:`.PlotYAxisConfig`. It provides the :attr:`enabled` property
    which can be used to enable or disable the optional Y-axes.
    """
    axis: PlotYAxis

    @property
    def enabled(self) -> bool:
        """Enable or disable the optional Y-axis."""
        # noinspection PyUnresolvedReferences
        return self.plot.get_config()[self.axis.optkey]

    @enabled.setter
    def enabled(self, enable: bool) -> None:
        # noinspection PyUnresolvedReferences
        self.plot.set_config(**{self.axis.optkey : enable})

## Plot Axis Descriptors

class PlotAxis:
    key: str

    def __set_name__(self, owner: Type[Plot], name: str):
        self.key = name
        self.config = f'_{name}_config'

    def __get__(self, plot: Optional[Plot], owner: Type[Plot]) -> Union[PlotAxisConfig, PlotAxis]:
        if plot is None:
            return self
        return getattr(plot, self.config)

class PlotXAxis(PlotAxis):
    pass

class PlotYAxis(PlotAxis):
    def __init__(self, index: int, optkey: Optional[str] = None):
        self.index = index
        self.optkey = optkey

## Plot Class

@_register_item_type('mvAppItemType::Plot')
class Plot(Widget, ItemWidgetMx):
    """A rich plot widget."""

    ## Plot Axes

    xaxis: PlotXAxisConfig  = PlotXAxis()  #: The X-axis
    yaxis: PlotYAxisConfig  = PlotYAxis(0)  #: The Y-axis
    y2axis: PlotOptYAxisConfig = PlotYAxis(1, 'yaxis2')  #: Optional Y-axis 2
    y3axis: PlotOptYAxisConfig = PlotYAxis(2, 'yaxis3')  #: Optional Y-axis 3

    ## Config Properties

    label: str = ConfigProperty()
    x_axis_label: str = ConfigProperty(key='x_axis_name')
    y_axis_label: str = ConfigProperty(key='y_axis_name')

    show_annotations: bool = ConfigProperty()
    show_drag_lines: bool = ConfigProperty()
    show_drag_points: bool = ConfigProperty()
    show_color_scale: bool = ConfigProperty()

    scale_min: float = ConfigProperty()
    scale_max: float = ConfigProperty()
    scale_height: int = ConfigProperty()
    equal_aspects: bool = ConfigProperty()

    query: bool = ConfigProperty()
    crosshairs: bool = ConfigProperty()
    no_legend: bool = ConfigProperty()
    no_menus: bool = ConfigProperty()
    no_box_select: bool = ConfigProperty()
    no_mouse_pos: bool = ConfigProperty()
    no_highlight: bool = ConfigProperty()
    no_child: bool = ConfigProperty()

    anti_aliased: bool = ConfigProperty()

    def __init__(self, *, name_id: str = None, **config):
        # not super happy that we have to resort to typing.cast() here, but it works
        self._xaxis_config = PlotXAxisConfig(self, cast(PlotXAxis, Plot.xaxis))
        self._yaxis_config = PlotYAxisConfig(self, cast(PlotYAxis, Plot.yaxis))
        self._y2axis_config = PlotOptYAxisConfig(self, cast(PlotYAxis, Plot.y2axis))
        self._y3axis_config = PlotOptYAxisConfig(self, cast(PlotYAxis, Plot.y3axis))

        super().__init__(name_id=name_id, **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_plot(self.id, **dpg_args)

    def add_dataseries(self, series: DataSeries, *, update_bounds: bool = True) -> None:
        """Add a :class:`.DataSeries` to this plot (or update it).

        Updates the data series if it has already been added."""
        series.update(self, update_bounds)

    def remove_dataseries(self, series: DataSeries) -> None:
        """Remove a :class:`.DataSeries` from this plot if it has been added."""
        dpgcore.delete_series(self.id, series.id)

    def clear(self) -> None:
        dpgcore.clear_plot(self.id)

    def set_xlimits(self, limits: Optional[PlotLimits]) -> None:
        """Set the ``(min, max)`` limits for the x-axis, or pass ``None`` to use automatic limits."""
        if limits is None:
            dpgcore.set_plot_xlimits_auto(self.id)
        else:
            dpgcore.set_plot_xlimits(self.id, *limits)

    def set_ylimits(self, limits: Optional[PlotLimits]) -> None:
        """Set the ``(min, max)`` limits for the y-axis, or pass ``None`` to use automatic limits."""
        if limits is None:
            dpgcore.set_plot_ylimits_auto(self.id)
        else:
            dpgcore.set_plot_ylimits(self.id, *limits)

    def set_xticks(self, ticks: Optional[Iterable[TickLabel]]) -> None:
        """Set the tick labels for the x-axis, or pass ``None`` to use automatic ticks."""
        if ticks is None:
            dpgcore.reset_xticks(self.id)
        else:
            dpgcore.set_xticks(self.id, ticks)

    def set_yticks(self, ticks: Optional[Iterable[TickLabel]]) -> None:
        """Set the tick labels for the y-axis, or pass ``None`` to use automatic ticks."""
        if ticks is None:
            dpgcore.reset_yticks(self.id)
        else:
            dpgcore.set_yticks(self.id, ticks)

    def add_annotation(self, text: str, pos: Tuple[float, float], offset: Tuple[float, float], *,
                       color: ColorRGBA = None, clamped: bool = True) -> PlotAnnotation:
        """Creates a :class:`.PlotAnnotation` and adds it to the plot."""
        return PlotAnnotation(self, text, pos, offset, color=color, clamped=clamped)

    def get_mouse_pos(self) -> Optional[Tuple[float, float]]:
        """Returns the ``(x, y)`` mouse position in the plot if it is hovered, or ``None``."""
        if not self.is_hovered():
            return None
        return dpgcore.get_plot_mouse_pos()

    def get_selected_query_area(self) -> Optional[PlotQueryArea]:
        """Returns a :class:`.PlotQueryArea` for the selected query area if there is one.

        A query area can be selected by the user by holding control and right-click dragging in
        a plot. If a query area has not been selected, this will return ``None``."""
        if not dpgcore.is_plot_queried(self.id):
            return None
        return PlotQueryArea(*dpgcore.get_plot_query_area(self.id))


class PlotQueryArea(NamedTuple):
    """The position of a selected :class:`.Plot` query area."""
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    @property
    def min_corner(self) -> Tuple[float, float]:
        """Returns ``(x_min, y_min)`` as a tuple."""
        return self.x_min, self.y_min

    @property
    def max_corner(self) -> Tuple[float, float]:
        """Returns ``(x_max, y_max)`` as a tuple."""
        return self.x_max, self.y_max

class PlotAnnotation:
    """Adds a plot annotation.

    Note:
        DPG does not support modifying existing plot annoations (other than to delete).
        Any methods provided that "mutate" the annotation actually delete and
        re-create the annotation in DPG.
    """

    plot: Plot
    text: str
    color: Optional[ColorRGBA] #: If ``None``, then the annotation will have no callout bubble.
    clamped: bool #: If ``True``, the label will be free to shift so that it is not clipped by the plot limits.

    x: float
    y: float
    offset: Tuple[float, float]

    _tag_id: str = None
    def __init__(self,
                 plot: Plot,
                 text: str,
                 pos: Tuple[float, float],
                 offset: Tuple[float, float], *,
                 color: ColorRGBA = None,
                 clamped: bool = True):

        self._tag_id = _generate_id(self)
        self._plot = plot
        self._text = text
        self._pos = pos
        self._offset = offset
        self._color = color
        self._clamped = clamped
        self._create_annotation()

    def _create_annotation(self) -> None:
        x, y = self._pos
        xoff, yoff = self.offset
        color = export_color_to_dpg(self._color) if self._color is not None else (0, 0, 0, -1)
        dpgcore.add_annotation(
            self._plot.id, self._text, x, y, xoff, yoff,
            color=color, clamped=self.clamped,
            tag=self._tag_id
        )

    def _delete_annotation(self) -> None:
        dpgcore.delete_annotation(self._plot.id, self._tag_id)

    def delete(self) -> None:
        self._delete_annotation()
        del self._tag_id

    @property
    def is_valid(self) -> bool:
        """``False`` if the annotation has been deleted."""
        return self._tag_id is not None

    @property
    def id(self) -> str: return self._tag_id
    @property
    def plot(self) -> Plot: return self._plot
    @property
    def text(self) -> str: return self._text
    @property
    def color(self) -> ColorRGBA: return self._color
    @property
    def clamped(self) -> bool: return self._clamped
    @property
    def x(self) -> float: return self._pos[0]
    @property
    def y(self) -> float: return self._pos[1]
    @property
    def offset(self) -> Tuple[float, float]: return self._offset

    def set_text(self, text: str) -> None:
        self._text = text
        self._delete_annotation()
        self._create_annotation()

    def set_color(self, color: Optional[ColorRGBA]) -> None:
        self._color = color
        self._delete_annotation()
        self._create_annotation()

    def set_position(self, x: float, y: float) -> None:
        self._pos = (x, y)
        self._delete_annotation()
        self._create_annotation()

    def set_offset(self, xoffset: float, yoffset: float) -> None:
        self._offset = (xoffset, yoffset)
        self._delete_annotation()
        self._create_annotation()

class PlotText:
    """Adds a point with text on a plot.

    Due to the limitations of DPG the each PlotText instance must
    have a unique label within each plot that it is added to.
    """

    def __init__(self,
                 label: str,
                 pos: Tuple[float, float], *,
                 vertical: bool = False,
                 offset: Tuple[int, int] = (0, 0),
                 axis: YAxis = Plot.yaxis):

        self.axis = axis
        self._name_id = label
        self.pos = pos
        self.offset = offset
        self.vertical = vertical

    @property
    def id(self) -> str:
        return self._name_id

    @property
    def axis(self) -> PlotYAxis:
        """Set the Y-axis used to display the data series."""
        return self._axis

    @axis.setter
    def axis(self, axis: YAxis) -> None:
        if hasattr(axis, 'axis'):
            self._axis = axis.axis
        else:
            self._axis = axis

    def update(self, plot: Plot, update_bounds: bool = True) -> None:
        x, y = self.pos
        xoff, yoff = self.offset
        dpgcore.add_text_point(
            plot.id, self._name_id, x, y,
            vertical=self.vertical,
            xoffset=xoff, yoffset=yoff,
            update_bounds=update_bounds,
            axis=self.axis.index
        )

__all__ = [
    'Plot',
]
