from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, Sequence, MutableSequence, overload

from dearpygui_obj import _generate_id
from dearpygui_obj.plots import Plot
if TYPE_CHECKING:
    from typing import Any, Optional, Type, Callable, Mapping, Iterable, NoReturn
    from dearpygui_obj.plots import PlotYAxis, YAxis

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

    def __len__(self) -> int:
        return len(self.series._data[self.key])

    def __iter__(self) -> Iterable[TValue]:
        return iter(self.series._data[self.key])

    @overload
    def __getitem__(self, index: int) -> TValue:
        ...

    @overload
    def __getitem__(self, index: slice) -> Iterable[TValue]:
        ...

    def __getitem__(self, index):
        """Get values for a particular data field using index or slice."""
        return self.series._data[self.key][index]

    @overload
    def __setitem__(self, index: int, value: TValue) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[TValue]) -> None:
        ...

    def __setitem__(self, index, value):
        """Set values for a particular data field using index or slice.

        Raises:
            TypeError: if the slice assignment would change the length of the sequence."""
        if isinstance(index, slice):
            self._set_slice(index, value)
        else:
            self.series._data[self.key][index] = value

    # raises a TypeError if the slice will change the length of the sequence
    def _set_slice(self, s: slice, value: Iterable) -> None:
        if not hasattr(value, '__len__'):
            value = list(value)
        if len(range(*s.indices(len(self)))) != len(value):
            raise TypeError('cannot change length of individual DataSeries field')
        self.series._data[self.key][s] = value

    def __delitem__(self, index: Any) -> NoReturn:
        """Always raises :class:`.TypeError`."""
        raise TypeError('cannot change length of individual DataSeries field')

    def insert(self, index: int, value: TValue) -> NoReturn:
        """Always raises :class:`.TypeError`."""
        raise TypeError('cannot change length of individual DataSeries field')

class DataSeriesField:
    """Supports assignment to a DataSeries' data field attributes."""
    def __set_name__(self, owner: Type[DataSeries], name: str):
        self.name = '_' + name
        self.__doc__ = f"Access '{name}' data as a linear sequence."

    def __get__(self, instance: DataSeries, owner: Type[DataSeries] = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance: DataSeries, value: Any) -> None:
        raise AttributeError('can\'t set attribute')

TRecord = TypeVar('TRecord', bound=Sequence)
class DataSeries(ABC, MutableSequence[TRecord]):
    """Abstract base class for plot data series."""

    @property
    @abstractmethod
    def __update_func__(self) -> Callable:
        """The DPG function used to add/update the data series."""
        ...

    @staticmethod
    def __create_record__(*values: Any) -> TRecord:
        """Factory function used to create records when retrieving individual data points."""
        return tuple(values)

    #: The keywords used to give the data to the DPG ``add_*_series()`` function.
    #: The order of keywords is used when creating records using :meth:`__create_record__`.
    __data_keywords__: Sequence[str]

    @classmethod
    def _get_data_keywords(cls) -> Iterable[str]:
        if cls.__data_keywords__ is None:
            # noinspection PyUnresolvedReferences
            return cls._record_type._fields
        if isinstance(cls.__data_keywords__, str):
            cls.__data_keywords__ = cls.__data_keywords__.split()
        return cls.__data_keywords__

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
            setattr(self, '_' + name, field)

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

    def update(self, plot: Plot, update_bounds: bool = True) -> None:
        """Updates a plot with this DataSeries.

        If this DataSeries has not been added to the plot before, this method will add it.

        Any changes made to a DataSeries's properties will only take effect when this method is called.

        Parameters:
            plot: the :class:`.Plot` to update.
            update_bounds: also update plot bounds if ``True``.
        """
        self.__update_func__(
            plot.id, self.id, axis=self._axis.index, update_bounds=update_bounds,
            **self._config, **dict(zip(self._get_data_keywords(), self._data))
        )

    ## Mutable Sequence Implementation

    def __len__(self) -> int:
        """Get the size of the data series."""
        return len(self._data[0])  # they should all be the same length

    def __iter__(self) -> Iterable[TRecord]:
        """Iterate the data series."""
        for values in zip(*self._data):
            yield self.__create_record__(*values)

    # def _iter_slice(self, iterable: Iterable, s: slice) -> Iterable:
    #     return itertools.islice(iterable, s.start or 0, )

    @overload
    def __getitem__(self, index: int) -> TRecord:
        ...

    @overload
    def __getitem__(self, index: slice) -> Iterable[TRecord]:
        ...

    def __getitem__(self, index):
        """Get data from the dataseries using an index or slice."""
        if isinstance(index, slice):
            return (
                self.__create_record__(*values)
                for values in zip(*(field[index] for field in self._data))
            )
        else:
            return self.__create_record__(*(field[index] for field in self._data))

    @overload
    def __setitem__(self, index: int, item: TRecord) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, item: Iterable[TRecord]) -> None:
        ...

    def __setitem__(self, index, item) -> None:
        """Modify the data series using an index or slice."""
        if isinstance(index, slice):
            item = zip(*item)
        for field_idx, value in enumerate(item):
            self._data[field_idx][index] = value

    @overload
    def __delitem__(self, index: int) -> None: ...

    @overload
    def __delitem__(self, index: slice) -> None: ...

    def __delitem__(self, index):
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
