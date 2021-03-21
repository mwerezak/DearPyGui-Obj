from __future__ import annotations

from typing import TYPE_CHECKING, Sequence, cast

import dearpygui.core as dpgcore

from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper.widget import Widget, ItemWidget, ValueWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Any, Optional, Union, Type


@_register_item_type('mvAppItemType::SimplePlot')
class SimplePlot(Widget, ItemWidget, ValueWidget[Sequence[float]]):
    """A simple plot to visualize a sequence of float values."""

    label: str = ConfigProperty()

    #: Overlays text (similar to a plot title).
    title: str = ConfigProperty(key='overlay')

    minscale: float = ConfigProperty()
    maxscale: float = ConfigProperty()
    histogram: bool = ConfigProperty()

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_simple_plot(self.id, **dpg_args)


## Rich Plots

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
    axis: PlotXAxis

    time: bool = PlotAxisConfigProperty()

class PlotYAxisConfig(PlotAxisConfig):
    axis: PlotYAxis

class PlotOptAxisConfig(PlotYAxisConfig):
    axis: PlotYAxis

    @property
    def enabled(self) -> bool:
        # noinspection PyUnresolvedReferences
        return self.plot.get_config()[self.axis.optkey]

    @enabled.setter
    def enabled(self, enable: bool) -> None:
        # noinspection PyUnresolvedReferences
        self.plot.set_config(**{self.axis.optkey : enable})

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

class Plot(Widget, ItemWidget):
    """A rich plot widget."""

    ## Plot Axes

    xaxis: PlotXAxisConfig  = PlotXAxis()
    yaxis: PlotYAxisConfig  = PlotYAxis(0)
    y2axis: PlotYAxisConfig = PlotYAxis(1, 'yaxis2')
    y3axis: PlotYAxisConfig = PlotYAxis(2, 'yaxis3')

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
        self._y2axis_config = PlotOptAxisConfig(self, cast(PlotYAxis, Plot.y2axis))
        self._y3axis_config = PlotOptAxisConfig(self, cast(PlotYAxis, Plot.y3axis))

        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_plot(self.id, **dpg_args)


__all__ = [
    'SimplePlot',
]
