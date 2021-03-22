from __future__ import annotations

from enum import Enum
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore

from dearpygui_obj import _generate_id
from dearpygui_obj.data import dpg_import_color, dpg_export_color
from dearpygui_obj.plots import Plot

if TYPE_CHECKING:
    from typing import Any, Optional, Union, Type, Callable, Tuple, Mapping, Sequence
    from dearpygui_obj.data import ColorRGBA
    from dearpygui_obj.plots import PlotYAxis, PlotYAxisConfig

    YAxis = Union[PlotYAxis, PlotYAxisConfig]
    ConvertFunc = Callable[[Any], Any]

class PlotMarker(Enum):
    """Marker shapes that can be used with certain data series."""

    NoMarker  = -1 #: no marker
    Circle    = 0  #: a circle marker
    Square    = 1  #: a square maker
    Diamond   = 2  #: a diamond marker
    Up        = 3  #: an upward-pointing triangle marker
    Down      = 4  #: an downward-pointing triangle marker
    Left      = 5  #: an leftward-pointing triangle marker
    Right     = 6  #: an rightward-pointing triangle marker
    Cross     = 7  #: a cross marker (not fillable)
    Plus      = 8  #: a plus marker (not fillable)
    Asterisk  = 9  #: a asterisk marker (not fillable)


class DataSeriesProperty:
    """Descriptor used to implement data series properties."""

    def __init__(self, key: str = None):
        self.key = key

    def __set_name__(self, owner: Type[DataSeries], name: str):
        if self.key is None:
            self.key = name

    def __get__(self, instance: Optional[DataSeries], owner: Type[DataSeries]) -> Any:
        if instance is None:
            return self
        return self.fvalue(instance[self.key])

    def __set__(self, instance: DataSeries, value: Any) -> None:
        instance[self.key] = self.fconfig(value)

    def __call__(self, fvalue: ConvertFunc):
        """Allows the DataSeriesProperty itself to be used as a decorator equivalent to :attr:`getvalue`."""
        return self.getvalue(fvalue)

    def getvalue(self, fvalue: ConvertFunc):
        self.fvalue = fvalue
        self.__doc__ = fvalue.__doc__ # use the docstring of the getter, the same way property() works
        return self

    def getconfig(self, fconfig: ConvertFunc):
        self.fconfig = fconfig
        return self

    ## default implementations
    fvalue: ConvertFunc
    fconfig: ConvertFunc

    def fvalue(self, config: Any) -> Any:
        return config

    def fconfig(self, value: Any) -> Any:
        return value

class DataSeriesPropertyColorRGBA(DataSeriesProperty):
    def fvalue(self, config: Any) -> ColorRGBA:
        return dpg_import_color(config)
    def fconfig(self, color: ColorRGBA) -> Any:
        return dpg_export_color(color)

class DataSeriesPropertyMarker(DataSeriesProperty):
    def fvalue(self, config: Any) -> PlotMarker:
        return PlotMarker(config)
    def fconfig(self, marker: PlotMarker) -> Any:
        return marker.value


class DataSeries(ABC):
    """Abstract base class for plot data series."""

    @property
    @abstractmethod
    def _update_func(self) -> Callable:
        ...

    @classmethod
    def _get_config_properties(cls) -> Mapping[str, DataSeriesProperty]:
        config_properties = cls.__dict__.get('_config_properties')
        if config_properties is None:
            config_properties = {}
            for name in cls.__annotations__:
                value = getattr(cls, name)
                if isinstance(value, DataSeriesProperty):
                    config_properties[name] = value
            setattr(cls, '_config_properties', config_properties)
        return config_properties

    def __init__(self, label: str, *, axis: YAxis = Plot.yaxis, **config: Any):
        self.axis = axis
        self._name_id = label + '##' +  _generate_id(self)
        self._config = {}

        props = self._get_config_properties()
        for prop_name, value in config.items():
            prop = props.get(prop_name)
            if prop is None:
                raise AttributeError(f"no config property named '{prop_name}'")
            prop.__set__(self, value)

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

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._config[key] = value

    def update_plot(self, plot: Plot, update_bounds: bool = True) -> None:
        """Updates a plot with this DataSeries.

        If this DataSeries has not been added to the plot before, this method will add it.

        Any changes made to a DataSeries's properties will only take effect when this method is called.

        Parameters:
            plot: the :class:`.Plot` to update.
            update_bounds: also update plot bounds if ``True``.
        """
        self._update_func(plot.id, self.id, axis=self._axis.index, update_bounds=update_bounds, **self._config)


## Data Series

class AreaSeries(DataSeries):
    """Adds an area series to a plot."""
    _update_func = dpgcore.add_area_series

    x: Sequence[float] = DataSeriesProperty()
    y: Sequence[float] = DataSeriesProperty()

    color: ColorRGBA = DataSeriesPropertyColorRGBA()
    fill: ColorRGBA = DataSeriesPropertyColorRGBA()

    weight: float = DataSeriesProperty()

    def __init__(self, label: str, x: Sequence[float], y: Sequence[float], color: ColorRGBA, fill: ColorRGBA, **config: Any):
        super().__init__(label, x=x, y=y, color=color, fill=fill, **config)


class BarSeries(DataSeries):
    """Adds a bar series to a plot."""
    _update_func = dpgcore.add_bar_series

    x: Sequence[float] = DataSeriesProperty()
    y: Sequence[float] = DataSeriesProperty()

    weight: float = DataSeriesProperty()
    horizontal: bool = DataSeriesProperty()

    def __init__(self, label: str, x: Sequence[float], y: Sequence[float], **config: Any):
        super().__init__(label, x=x, y=y, **config)


class CandleSeries(DataSeries):
    """Adds a candle series to a plot."""
    _update_func = dpgcore.add_candle_series

    date: Sequence[float] = DataSeriesProperty() #: POSIX timestamps
    opens: Sequence[float] = DataSeriesProperty()
    highs: Sequence[float] = DataSeriesProperty()
    lows: Sequence[float] = DataSeriesProperty()
    closes: Sequence[float] = DataSeriesProperty()

    tooltip: bool = DataSeriesProperty()
    bull_color: ColorRGBA = DataSeriesPropertyColorRGBA()
    bear_color: ColorRGBA = DataSeriesPropertyColorRGBA()
    weight: float = DataSeriesProperty()

    def __init__(self, label: str,
                 date: Sequence[float],
                 opens: Sequence[float],
                 highs: Sequence[float],
                 lows: Sequence[float],
                 closes: Sequence[float],
                 **config: Any):

        super().__init__(label, date=date, opens=opens, highs=highs, lows=lows, closes=closes, **config)


class ErrorSeries(DataSeries):
    """Adds an error series to a plot."""
    _update_func = dpgcore.add_error_series

    x: Sequence[float] = DataSeriesProperty()
    y: Sequence[float] = DataSeriesProperty()
    negative: Sequence[float] = DataSeriesProperty()
    positive: Sequence[float] = DataSeriesProperty()

    horizontal: bool = DataSeriesProperty()

    def __init__(self, label: str,
                 x: Sequence[float], y: Sequence[float],
                 negative: Sequence[float], positive: Sequence[float],
                 **config: Any):
        super().__init__(label, x=x, y=y, negative=negative, positive=positive, **config)


class HeatSeries(DataSeries):
    """Adds a heat series to a plot."""
    _update_func = dpgcore.add_heat_series

    values: Sequence[float] = DataSeriesProperty()
    rows: int = DataSeriesProperty()
    columns: int = DataSeriesProperty()
    scale_min: float = DataSeriesProperty()
    scale_max: float = DataSeriesProperty()

    format: str = DataSeriesProperty()
    bounds_min: Tuple[float, float]
    bounds_max: Tuple[float, float]

    @DataSeriesProperty(key='bounds_min')
    def bounds_min(self, config) -> Tuple[float, float]:
        return tuple(config)

    @DataSeriesProperty(key='bounds_max')
    def bounds_max(self, config) -> Tuple[float, float]:
        return tuple(config)

    def __init__(self, label: str,
                values: Sequence[float],
                rows: int, columns: int,
                scale_min: float, scale_max: float,
                 **config: Any):
        super().__init__(label, values=values, rows=rows, columns=columns, scale_min=scale_min, scale_max=scale_max, **config)


class HLineSeries(DataSeries):
    """Adds an infinite horizontal line series to a plot."""
    _update_func = dpgcore.add_hline_series

    x: Sequence[float] = DataSeriesProperty()

    color: ColorRGBA = DataSeriesPropertyColorRGBA()
    weight: float = DataSeriesProperty()

    def __init__(self, label: str, x: Sequence[float], **config: Any):
        super().__init__(label, x=x, **config)


# TODO
# class ImageSeries(DataSeries):
#     """Adds an image series to a plot."""

class LineSeries(DataSeries):
    """Adds a line series to a plot."""
    _update_func = dpgcore.add_line_series

    x: Sequence[float] = DataSeriesProperty()
    y: Sequence[float] = DataSeriesProperty()

    color: ColorRGBA = DataSeriesPropertyColorRGBA()
    weight: float = DataSeriesProperty()

    def __init__(self, label: str, x: Sequence[float], y: Sequence[float], **config: Any):
        super().__init__(label, x=x, y=y, **config)


class PieSeries(DataSeries):
    """Adds a pie chart to a plot."""

    pass

"""
    values : List[float]

    labels : List[str]

    x : float

    y : float

    radius : float

    Keyword Only Arguments

    normalize : bool = False

    angle : float = 90.0

    format : str = '%0.2f'
"""

class ScatterSeries(DataSeries):
    """Adds a scatter series to a plot."""
    _update_func = dpgcore.add_scatter_series

    x: Sequence[float] = DataSeriesProperty()
    y: Sequence[float] = DataSeriesProperty()

    marker: PlotMarker = DataSeriesPropertyMarker()
    size: float = DataSeriesProperty()
    weight: float = DataSeriesProperty()
    outline: ColorRGBA = DataSeriesPropertyColorRGBA()
    fill: ColorRGBA = DataSeriesPropertyColorRGBA()
    xy_data_format: bool = DataSeriesProperty()

    def __init__(self, label: str, x: Sequence[float], y: Sequence[float], **config: Any):
        super().__init__(label, x=x, y=y, **config)



__all__ = [
    'PlotMarker',
    'ScatterSeries',
    'LineSeries',
]