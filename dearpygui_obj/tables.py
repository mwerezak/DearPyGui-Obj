from __future__ import annotations
from typing import TYPE_CHECKING, overload

import dearpygui.core as dpgcore

from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper.widget import Widget, ItemWidgetMx, ConfigProperty

if TYPE_CHECKING:
    from typing import Any, Union, Tuple, Iterable, Sequence, List, MutableMapping

@_register_item_type('mvAppItemType::Table')
class Table(Widget, ItemWidgetMx):
    """Adds a simple table that can hold text.

    A Table's data consists of a sequence of rows, each row being a sequence of strings.

    Note that a Table has two different kinds of "columns". A Table will have a number of *data*
    columns and a number of *header* columns.

    These won't always match. If you have more data columns than header columns, only a subsection
    of the data will actually get shown. This will be the case even if :attr:`hide_headers` is
    ``True``.

    Parameters:
        headers: can be an iterable of header strings or an integer. If an integer is used,
            it will set the number of header columns and the :attr:`hide_headers` property
            will be set to ``True``.

    To get/set values in the table, indexing syntax can be used. For example:

    .. code-block:: python

        table[2, 3] = 'cell content'
        table[3, :] = ['sets', 'an', 'entire', 'row']
        table[:, 4] = ['sets', 'an', 'entire', 'column']
        table[:, :] = [['first', row'], ['second', 'row'], ['third', 'row]]

    Cell selection state can also be modified in a similar manner.

    .. code-block:: python

        table.selection[1, :] = True  # selects the entire second row.

    """

    hide_headers: bool = ConfigProperty()  #: If ``True``, table headers will not be displayed.

    #: A :class:`.TableSelection` instance that can be used to get or modify the table's cell
    #: selection state.
    selected: TableSelection

    def __init__(self, headers: Union[int, Iterable[str]] = 2, *, name_id: str = None, **config: Any):
        if isinstance(headers, int):
            super().__init__(headers=['' for i in range(headers)], hide_headers=True, name_id=name_id, **config)
        else:
            super().__init__(headers=headers, name_id=name_id, **config)
        self.selected = TableSelection(self)

    def __setup_add_widget__(self, dpg_args: MutableMapping[str, Any]) -> None:
        dpgcore.add_table(self.id, **dpg_args)

    def set_headers(self, headers: Union[Iterable[str], int]) -> None:
        """Set the table headers.

        This determines the number of displayed columns (distinct from the number of data columns!).
        If an integer is passed, the headers will be replaced with empty strings and hidden."""
        if isinstance(headers, int):
            headers = ['' for i in range(headers)]
            self.hide_headers = True
        dpgcore.set_headers(self.id, headers)

    def _get_data(self) -> List[List[str]]:
        return dpgcore.get_table_data(self.id)

    @property
    def rows(self) -> int:
        """The number of data rows."""
        return len(self._get_data())

    @property
    def columns(self) -> int:
        """The number of data columns."""
        data = self._get_data()
        if len(data):
            return len(data[0])
        return 0

    @overload
    def __getitem__(self, indices: Tuple[int, int]) -> str:
        ...

    @overload
    def __getitem__(self, indices: Tuple[int, slice]) -> Sequence[str]:
        ...

    @overload
    def __getitem__(self, indices: Tuple[slice, int]) -> Sequence[str]:
        ...

    @overload
    def __getitem__(self, indices: Tuple[slice, slice]) -> Sequence[Sequence[str]]:
        ...

    def __getitem__(self, indices):
        """Get table data using indices or slices."""
        row_idx, col_idx = indices
        if isinstance(row_idx, slice) and isinstance(col_idx, slice):
            return tuple(tuple(row[col_idx]) for row in self._get_data()[row_idx])
        elif isinstance(row_idx, slice):
            return tuple(row[col_idx] for row in self._get_data()[row_idx])
        elif isinstance(col_idx, slice):
            return tuple(self._get_data()[row_idx][col_idx])
        else:
            return dpgcore.get_table_item(self.id, row_idx, col_idx)


    @overload
    def __setitem__(self, indices: Tuple[int, int], value: str) -> None:
        ...

    @overload
    def __setitem__(self, indices: Tuple[int, slice], value: Iterable[str]) -> None:
        ...

    @overload
    def __setitem__(self, indices: Tuple[slice, int], value: Iterable[str]) -> None:
        ...

    @overload
    def __setitem__(self, indices: Tuple[slice, slice], value: Iterable[Iterable[str]]) -> None:
        ...

    def __setitem__(self, indices, value):
        """Set table data using indices or slices.
        The shape of the **value** argument must match the provided indices/slices."""
        row_idx, col_idx = indices

        ## both row_idx and col_idx are slices. value is an iterable of iterables
        if isinstance(row_idx, slice) and isinstance(col_idx, slice):
            if row_idx == slice(None) and col_idx == slice(None):
                data = value  # overwrite entire table data
            else:
                data = self._get_data()  # overwrite just sliced rows and columns
                for data_row, set_row in zip(data[row_idx], value):
                    data_row[col_idx] = set_row
            dpgcore.set_table_data(self.id, data)

        ## just row_idx is a slice. value is an iterable
        elif isinstance(row_idx, slice):
            data = self._get_data()
            for row, s in zip(data[row_idx], value):
                row[col_idx] = s
            dpgcore.set_table_data(self.id, data)

        ## just col_idx is a slice. value is an iterable
        elif isinstance(col_idx, slice):
            data = self._get_data()
            data[row_idx][col_idx] = value
            dpgcore.set_table_data(self.id, data)

        ## neither are slices
        else:
            dpgcore.set_table_item(self.id, row_idx, col_idx, value)

    def clear(self) -> None:
        """Clear the table.

        This will remove all rows from the table.
        It does NOT change the table headers and therefore the number of visible columns."""
        dpgcore.clear_table(self.id)

    def append_row(self, row: Iterable[str]) -> None:
        dpgcore.add_row(self.id, list(row))

    def insert_row(self, row_idx: int, row: Iterable[str]) -> None:
        dpgcore.insert_row(self.id, row_idx, list(row))

    def remove_row(self, row_idx: int) -> None:
        dpgcore.delete_row(self.id, row_idx)

    def append_column(self, header: str, column: Iterable[str]) -> None:
        dpgcore.add_column(self.id, header, list(column))

    def insert_column(self, col_idx: int, header: str, column: Iterable[str]) -> None:
        dpgcore.insert_column(self.id, col_idx, header, list(column))

    def remove_column(self, col_idx: int) -> None:
        dpgcore.delete_column(self.id, col_idx)


class TableSelection:
    """Get/set which cells are selected in a :class:`.Table`."""
    def __init__(self, table: Table):
        self.table = table

    def __iter__(self) -> Iterable[Tuple[int, int]]:
        """Iterate the selected cells as ``(row, col)`` pairs."""
        for pair in dpgcore.get_table_selections(self.table.id):
            yield tuple(pair)

    def __setitem__(self, indices: Tuple[Union[int, slice], Union[int, slice]], selected: bool) -> None:
        """Modify the cell selection state.

        Uses the same syntax as table indexing, allowing the selection of multiple cells to be
        modified at once using slices."""
        row_idx, col_idx = indices

        if isinstance(row_idx, slice) and isinstance(col_idx, slice):
            ## both row_idx and col_idx are slices
            for i in range(*row_idx.indices(self.table.rows)):
                for j in range(*col_idx.indices(self.table.columns)):
                    dpgcore.set_table_selection(self.table.id, i, j, selected)

        elif isinstance(row_idx, slice):
            ## just row_idx is a slice. value is a sequence
            for i in range(*row_idx.indices(self.table.rows)):
                dpgcore.set_table_selection(self.table.id, i, col_idx, selected)

        ## just col_idx is a slice. value is a sequence
        elif isinstance(col_idx, slice):
            for j in range(*col_idx.indices(self.table.columns)):
                dpgcore.set_table_selection(self.table.id, row_idx, j, selected)

        else:
            ## neither are slices
            dpgcore.set_table_selection(self.table.id, row_idx, col_idx, selected)


__all__ = [
    'Table',
]