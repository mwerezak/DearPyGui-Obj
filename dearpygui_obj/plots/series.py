from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj.data import dpg_import_color, dpg_export_color
from dearpygui_obj.wrapper.dataseries import DataSeries, DataSeriesProperty

if TYPE_CHECKING:
    from typing import Any, Tuple, Sequence
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