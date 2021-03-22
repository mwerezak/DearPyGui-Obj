from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from dearpygui_obj import _generate_id

if TYPE_CHECKING:
    from typing import Any, Optional, Union, Type, Callable, Mapping
    from dearpygui_obj.plots import Plot, PlotYAxis, PlotYAxisConfig

    YAxis = Union[PlotYAxis, PlotYAxisConfig]
    ConvertFunc = Callable[[Any], Any]


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