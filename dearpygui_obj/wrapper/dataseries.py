from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, NamedTuple, TypeVar, MutableSequence

from dearpygui_obj import _generate_id
from dearpygui_obj.plots import Plot
if TYPE_CHECKING:
    from typing import Any, Optional, Union, Type, Callable, Mapping, Iterable, Sequence
    from dearpygui_obj.plots import PlotYAxis, PlotYAxisConfig

    YAxis = Union[PlotYAxis, PlotYAxisConfig]
    ConvertFunc = Callable[[Any], Any]


class DataSeriesConfig:
    """Descriptor used to get/set non-data config properties for :class:`DataSeries` objects."""

    def __init__(self, key: str = None):
        self.key = key

    def __set_name__(self, owner: Type[DataSeries], name: str):
        if self.key is None:
            self.key = name

    def __get__(self, instance: Optional[DataSeries], owner: Type[DataSeries]) -> Any:
        if instance is None:
            return self
        return self.fvalue(instance.get_config(self.key))

    def __set__(self, instance: DataSeries, value: Any) -> None:
        instance.set_config(self.key, self.fconfig(value))

    def __call__(self, fvalue: ConvertFunc):
        """Allows the DataSeriesConfig itself to be used as a decorator equivalent to :attr:`getvalue`."""
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


TValue = TypeVar('TValue')
class DataSeriesCollection(MutableSequence[TValue]):
    """Collection type that allows set/get of individual data fields of a data series.

    Individual data fields are read-write. Appending, inserting, or deleting individual fields
    is not permitted however. Any operations that change the length of the sequence will raise a
    :class:`TypeError`."""

    def __init__(self, series: DataSeries, key: int):
        self.series = series
        self.key = key

    # raises a TypeError if the slice will change the length of the sequence
    def _set_slice(self, s: slice, value: Iterable) -> None:
        if not hasattr(value, '__len__'):
            value = list(value)
        if len(range(*s.indices(len(self)))) != len(value):
            raise TypeError('cannot change length of individual DataSeries field')
        self.series._data[self.key][s] = value

    def __len__(self) -> int:
        return len(self.series._data[self.key])

    def __getitem__(self, index: int) -> TValue:
        return self.series._data[self.key][index]

    def __setitem__(self, index: int, value: TValue) -> None:
        if isinstance(index, slice):
            self._set_slice(index, value)
        else:
            self.series._data[self.key][index] = value

    def __delitem__(self, index: int) -> None:
        raise TypeError('cannot change length of individual DataSeries field')

    def insert(self, index: int, value: TValue) -> None:
        raise TypeError('cannot change length of individual DataSeries field')

class DataSeriesField:
    """Supports assignment to a DataSeries' data field attributes."""
    def __set_name__(self, owner: Type[DataSeries], name: str):
        self.name = f'_{name}_accessor'

    def __get__(self, instance: DataSeries, owner: Type[DataSeries]) -> DataSeriesField:
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance: DataSeries, value: Iterable[Any]) -> None:
        getattr(instance, self.name)[:] = value

TRecord = TypeVar('TRecord')
class DataSeries(ABC, MutableSequence[TRecord]):
    """Abstract base class for plot data series."""

    @property
    @abstractmethod
    def _update_func(self) -> Callable:
        """The DPG function used to add/update the data series."""
        ...

    @staticmethod
    def _create_record(*values: Any) -> TRecord:
        """Factory function used to create records when retrieving individual data points."""
        return tuple(values)

    #: The keywords used to give the data to the DPG ``add_*_series()`` function.
    #: The order of keywords is used when creating records using :meth:`_create_record`.
    _data_keywords: Sequence[str]

    @classmethod
    def _get_data_keywords(cls) -> Iterable[str]:
        if cls._data_keywords is None:
            # noinspection PyUnresolvedReferences
            return cls._record_type._fields
        if isinstance(cls._data_keywords, str):
            cls._data_keywords = cls._data_keywords.split()
        return cls._data_keywords

    @classmethod
    def _get_config_properties(cls) -> Mapping[str, DataSeriesConfig]:
        config_properties = cls.__dict__.get('_config_properties')
        if config_properties is None:
            config_properties = {}
            for name in dir(cls):
                value = getattr(cls, name)
                if isinstance(value, DataSeriesConfig):
                    config_properties[name] = value
            setattr(cls, '_config_properties', config_properties)
        return config_properties

    def __init__(self, label: str, data: Iterable, *, axis: YAxis = Plot.yaxis, **config: Any):
        self.axis = axis
        self._name_id = label + '##' +  _generate_id(self)
        self._data = []
        self._config = {}

        ## create data fields from record type
        for index, name in enumerate(self._get_data_keywords()):
            self._data.append([])
            field = DataSeriesCollection(self, index)
            setattr(self, f'_{name}_accessor', field)

        ## non-data config properties
        props = self._get_config_properties()
        for prop_name, value in config.items():
            prop = props.get(prop_name)
            if prop is None:
                raise AttributeError(f"no config property named '{prop_name}'")
            prop.__set__(self, value)

        self.extend(data)

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

    def get_config(self, key: str) -> Any:
        """Get a config value."""
        return self._config[key]

    def set_config(self, key: str, value: Any) -> None:
        """Set a config value."""
        self._config[key] = value

    def update_plot(self, plot: Plot, update_bounds: bool = True) -> None:
        """Updates a plot with this DataSeries.

        If this DataSeries has not been added to the plot before, this method will add it.

        Any changes made to a DataSeries's properties will only take effect when this method is called.

        Parameters:
            plot: the :class:`.Plot` to update.
            update_bounds: also update plot bounds if ``True``.
        """
        self._update_func(
            plot.id, self.id, axis=self._axis.index, update_bounds=update_bounds,
            **self._config, **dict(zip(self._get_data_keywords(), self._data))
        )

    ## Mutable Sequence Implementation

    def __len__(self) -> int:
        return len(self._data[0])  # they should all be the same length

    def __iter__(self) -> Iterable[TRecord]:
        for values in zip(*self._data):
            yield self._create_record(*values)

    def __getitem__(self, index: int) -> TRecord:
        return self._create_record(*(seq[index] for seq in self._data))

    def __setitem__(self, index: int, item: Any) -> None:
        for field_idx, value in enumerate(item):
            self._data[field_idx][index] = value

    def __delitem__(self, index: int) -> None:
        for seq in self._data:
            del seq[index]

    def insert(self, index: int, item: Any) -> None:
        for field_idx, value in enumerate(item):
            self._data[field_idx].insert(index, value)

    def append(self, item: Any) -> None:
        for field_idx, value in enumerate(item):
            self._data[field_idx].append(value)

    def extend(self, items: Iterable[Any]) -> None:
        # unzip into 1D sequences for each field
        for field_idx, values in enumerate(zip(*items)):
            self._data[field_idx].extend(values)

    # these work because tuples typically have value semantics
    def index(self, item: Any, start: int = None, stop: int = None) -> int:
        # improve on the naive default implementation by zipping everything up front
        data = (s[start:stop] for s in self._data)
        for idx, row in enumerate(zip(*data)):
            if row == item:
                return idx
        raise ValueError(f'{item} is not in {self.__class__.__name__}')

    def remove(self, item: Any) -> None:
        for idx, row in enumerate(zip(*self._data)):
            if row == item:
                del self[idx]
                return

    def clear(self) -> None:
        for seq in self._data:
            seq.clear()
