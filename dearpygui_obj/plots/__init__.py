from __future__ import annotations

from typing import TYPE_CHECKING, cast

import dearpygui.core as dpgcore

from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper.widget import Widget, ItemWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Any, Optional, Union, Type, Tuple, Iterable
    from dearpygui_obj.plots.dataseries import DataSeries

    TickLabel = Tuple[str, float]
    PlotLimits = Tuple[float, float]

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
class Plot(Widget, ItemWidget):
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

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_plot(self.id, **dpg_args)

    def add_dataseries(self, series: DataSeries, *, update_bounds: bool = True) -> None:
        """Add a :class:`.DataSeries` to this plot (or update it).

        Updates the data series if it has already been added."""
        series.update_plot(self, update_bounds)

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


__all__ = [
    'Plot',
]
