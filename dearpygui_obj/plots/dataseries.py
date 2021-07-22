from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, NamedTuple

from dearpygui import dearpygui as dpgcore
from dearpygui_obj.data import import_color_from_dpg, export_color_to_dpg
from dearpygui_obj.wrapper.dataseries import DataSeries, DataSeriesConfig, DataSeriesField

if TYPE_CHECKING:
    from typing import Any, Tuple, Iterable, MutableSequence
    from dearpygui_obj.data import ColorRGBA


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

class DataSeriesConfigColorRGBA(DataSeriesConfig):
    def fvalue(self, config: Any) -> ColorRGBA:
        return import_color_from_dpg(config)
    def fconfig(self, color: ColorRGBA) -> Any:
        return export_color_to_dpg(color)

class DataSeriesConfigMarker(DataSeriesConfig):
    def fvalue(self, config: Any) -> PlotMarker:
        return PlotMarker(config)
    def fconfig(self, marker: PlotMarker) -> Any:
        return marker.value

class XYData(NamedTuple):
    """Common 2D data point used by many data series types."""
    x: float #: X-axis data.
    y: float #: Y-axis data.


## Data Series

class AreaSeries(DataSeries[XYData]):
    """Adds an area series to a plot."""
    __update_func__ = dpgcore.add_area_series
    __create_record__ = XYData
    __data_keywords__ = 'x y'

    x: MutableSequence[float] = DataSeriesField()
    y: MutableSequence[float] = DataSeriesField()

    color: ColorRGBA = DataSeriesConfigColorRGBA()
    fill: ColorRGBA = DataSeriesConfigColorRGBA()

    weight: float = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], color: ColorRGBA, fill: ColorRGBA, **config: Any):
        super().__init__(label, data, color=color, fill=fill, **config)


class BarSeries(DataSeries[XYData]):
    """Adds a bar series to a plot."""
    __update_func__ = dpgcore.add_bar_series
    __create_record__ = XYData
    __data_keywords__ = 'x y'

    x: MutableSequence[float] = DataSeriesField()
    y: MutableSequence[float] = DataSeriesField()

    weight: float = DataSeriesConfig()
    horizontal: bool = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)

class CandleSeriesData(NamedTuple):
    """Data record type for :class:`.CandleSeries`."""
    date: float  #: POSIX timestamp
    open: float
    high: float
    low: float
    close: float

class CandleSeries(DataSeries[CandleSeriesData]):
    """Adds a candle series to a plot."""
    __update_func__ = dpgcore.add_candle_series
    __create_record__ = CandleSeriesData
    __data_keywords__ = 'date opens highs lows closes'

    date: MutableSequence[float] = DataSeriesField()
    opens: MutableSequence[float] = DataSeriesField()
    highs: MutableSequence[float] = DataSeriesField()
    lows: MutableSequence[float] = DataSeriesField()
    closes: MutableSequence[float] = DataSeriesField()

    tooltip: bool = DataSeriesConfig()
    bull_color: ColorRGBA = DataSeriesConfigColorRGBA()
    bear_color: ColorRGBA = DataSeriesConfigColorRGBA()
    weight: float = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)


class ErrorSeriesData(NamedTuple):
    """Data record type for :class:`.ErrorSeries`."""
    x: float
    y: float
    negative: float
    positive: float

class ErrorSeries(DataSeries[ErrorSeriesData]):
    """Adds an error series to a plot."""
    __update_func__ = dpgcore.add_error_series
    __create_record__ = ErrorSeriesData
    __data_keywords__ = 'x y negative positive'


    x: MutableSequence[float] = DataSeriesField()
    y: MutableSequence[float] = DataSeriesField()
    negative: MutableSequence[float] = DataSeriesField()
    positive: MutableSequence[float] = DataSeriesField()

    horizontal: bool = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)


class HeatSeries(DataSeries[tuple]):
    """Adds a heat series to a plot."""
    __update_func__ = dpgcore.add_heat_series
    __data_keywords__ = 'values'

    values: MutableSequence[float] = DataSeriesField()

    rows: int = DataSeriesConfig()
    columns: int = DataSeriesConfig()
    scale_min: float = DataSeriesConfig()
    scale_max: float = DataSeriesConfig()

    format: str = DataSeriesConfig()
    bounds_min: Tuple[float, float]
    bounds_max: Tuple[float, float]

    @DataSeriesConfig(key='bounds_min')
    def bounds_min(self, config) -> Tuple[float, float]:
        return tuple(config)

    @DataSeriesConfig(key='bounds_max')
    def bounds_max(self, config) -> Tuple[float, float]:
        return tuple(config)

    def __init__(self, label: str,
                values: Iterable[float],
                rows: int, columns: int,
                scale_min: float, scale_max: float,
                 **config: Any):
        values = ((v,) for v in values)
        super().__init__(label, values, rows=rows, columns=columns, scale_min=scale_min, scale_max=scale_max, **config)


class HLineSeries(DataSeries[tuple]):
    """Adds an infinite horizontal line series to a plot."""
    __update_func__ = dpgcore.add_hline_series
    __data_keywords__ = 'x'

    x: MutableSequence[float] = DataSeriesField()

    color: ColorRGBA = DataSeriesConfigColorRGBA()
    weight: float = DataSeriesConfig()

    def __init__(self, label: str, x: Iterable[float], **config: Any):
        super().__init__(label, ((v,) for v in x), **config)


class VLineSeries(DataSeries[tuple]):
    """Adds an infinite vertical line series to a plot."""
    __update_func__ = dpgcore.add_vline_series
    __data_keywords__ = 'x'

    x: MutableSequence[float] = DataSeriesField()

    color: ColorRGBA = DataSeriesConfigColorRGBA()
    weight: float = DataSeriesConfig()

    def __init__(self, label: str, x: Iterable[float], **config: Any):
        super().__init__(label, ((v,) for v in x), **config)


# TODO
# class ImageSeries(DataSeries):
#     """Adds an image series to a plot."""

class LineSeries(DataSeries[XYData]):
    """Adds a line series to a plot."""
    __update_func__ = dpgcore.add_line_series
    __create_record__ = XYData
    __data_keywords__ = 'x y'

    x: MutableSequence[float] = DataSeriesField()
    y: MutableSequence[float] = DataSeriesField()

    color: ColorRGBA = DataSeriesConfigColorRGBA()
    weight: float = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)

class PieSeriesData(NamedTuple):
    """Data record type for :class:`.PieSeries`."""
    value: float
    label: str

class PieSeries(DataSeries[PieSeriesData]):
    """Adds a pie chart to a plot."""
    __update_func__ = dpgcore.add_pie_series
    __create_record__ = PieSeriesData
    __data_keywords__ = 'values labels'

    values: MutableSequence[float] = DataSeriesField()
    labels: MutableSequence[str] = DataSeriesField()

    x: float = DataSeriesConfig()
    y: float = DataSeriesConfig()
    radius: float = DataSeriesConfig()

    normalize: bool = DataSeriesConfig()
    angle: bool = DataSeriesConfig()
    format: str = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any],
                 x: float, y: float, radius: float,
                 **config: Any):
        super().__init__(label, data, x=x, y=y, radius=radius, **config)

class ScatterSeries(DataSeries[XYData]):
    """Adds a scatter series to a plot."""
    __update_func__ = dpgcore.add_scatter_series
    __create_record__ = XYData
    __data_keywords__ = 'x y'

    x: MutableSequence[float] = DataSeriesField()
    y: MutableSequence[float] = DataSeriesField()

    marker: PlotMarker = DataSeriesConfigMarker()
    size: float = DataSeriesConfig()
    weight: float = DataSeriesConfig()
    outline: ColorRGBA = DataSeriesConfigColorRGBA()
    fill: ColorRGBA = DataSeriesConfigColorRGBA()
    xy_data_format: bool = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)


class ShadeSeries(DataSeries[XYData]):
    """Adds a single-sided shade series to a plot."""
    __update_func__ = dpgcore.add_scatter_series
    __create_record__ = XYData
    __data_keywords__ = 'x y1'

    x: MutableSequence[float] = DataSeriesField()
    y1: MutableSequence[float] = DataSeriesField()

    color: ColorRGBA = DataSeriesConfigColorRGBA()
    fill: ColorRGBA = DataSeriesConfigColorRGBA()
    weight: float = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)


class ShadeRangeData(NamedTuple):
    """Data record type for :class:`.ShadeRangeSeries`."""
    x: float
    y1: float
    y2: float

class ShadeRangeSeries(DataSeries[ShadeRangeData]):
    """Adds a single-sided shade series to a plot."""
    __update_func__ = dpgcore.add_scatter_series
    __create_record__ = ShadeRangeData
    __data_keywords__ = 'x y1 y2'

    x: MutableSequence[float] = DataSeriesField()
    y1: MutableSequence[float] = DataSeriesField()
    y2: MutableSequence[float] = DataSeriesField()

    color: ColorRGBA = DataSeriesConfigColorRGBA()
    fill: ColorRGBA = DataSeriesConfigColorRGBA()
    weight: float = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)


class StairSeries(DataSeries[XYData]):
    """Add a stair series to a plot."""
    __update_func__ = dpgcore.add_stair_series
    __create_record__ = XYData
    __data_keywords__ = 'x y'

    x: MutableSequence[float] = DataSeriesField()
    y: MutableSequence[float] = DataSeriesField()

    color: ColorRGBA = DataSeriesConfigColorRGBA()
    weight: float = DataSeriesConfig()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)


class StemSeries(DataSeries[XYData]):
    """Add a stem series to a plot."""
    __update_func__ = dpgcore.add_stem_series
    __create_record__ = XYData
    __data_keywords__ = 'x y'

    x: MutableSequence[float] = DataSeriesField()
    y: MutableSequence[float] = DataSeriesField()

    marker: PlotMarker = DataSeriesConfigMarker()
    size: float = DataSeriesConfig()
    weight: float = DataSeriesConfig()
    outline: ColorRGBA = DataSeriesConfigColorRGBA()
    fill: ColorRGBA = DataSeriesConfigColorRGBA()

    def __init__(self, label: str, data: Iterable[Any], **config: Any):
        super().__init__(label, data, **config)


__all__ = [
    'AreaSeries',
    'BarSeries',
    'CandleSeries',
    'CandleSeriesData',
    'ErrorSeries',
    'ErrorSeriesData',
    'HeatSeries',
    'HLineSeries',
    'PieSeries',
    'PieSeriesData',
    'LineSeries',
    'ScatterSeries',
    'ShadeSeries',
    'ShadeRangeSeries',
    'ShadeRangeData',
    'StairSeries',
    'StemSeries',
    'XYData',
    'PlotMarker',
]

if TYPE_CHECKING:
    from dearpygui_obj.wrapper.dataseries import DataSeries
    __all__.append('DataSeries')