"""Widgets for controlling layout."""

from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper.widget import Widget, ItemWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Sequence

@_register_item_type('mvAppItemType::Spacing')
class VSpacing(Widget, ItemWidget):
    """Adds vertical spacing."""

    space: int = ConfigProperty(key='count') #: The amount of vertical space.

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_spacing(name=self.id, **dpg_args)


@_register_item_type('mvAppItemType::SameLine')
class HAlignNext(Widget, ItemWidget):
    """Places a widget on the same line as the previous widget.
    Can also be used for horizontal spacing."""

    xoffset: float = ConfigProperty() #: offset from containing window
    spacing: float = ConfigProperty() #: offset from previous widget

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_same_line(name=self.id, **dpg_args)

def group_horizontal(spacing: float = -1, *, name_id: str = None, **config: Any) -> LayoutGroup:
    """Shortcut constructor for ``LayoutGroup(horizontal=True)``"""
    return LayoutGroup(horizontal=True, horizontal_spacing=spacing, name_id=name_id, **config)

@_register_item_type('mvAppItemType::Group')
class LayoutGroup(Widget, ItemWidget):
    """Grouped widgets behave as a single unit when acted on by other layout widgets.

    They can optionally have their contents flow horizontally instead of vertically.
    """

    horizontal: bool = ConfigProperty()
    horizontal_spacing: float = ConfigProperty()

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_group(self.id, **dpg_args)

    def __enter__(self) -> LayoutGroup:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()

@_register_item_type('mvAppItemType::Indent')
class LayoutIndent(Widget, ItemWidget):
    """Adds an indent to contained items."""

    offset: float = ConfigProperty()

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_indent(name=self.id, **dpg_args)

    def __enter__(self) -> LayoutIndent:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.unindent()


@_register_item_type('mvAppItemType::ManagedColumns')
class LayoutColumns(Widget, ItemWidget):
    """Places contents into columns.

    Each new widget added will be placed in the next column, wrapping around to the start."""

    num_cols: int = ConfigProperty(key='columns', no_init=True)  #: Number of columns.
    border: bool = ConfigProperty()  #: Draw a border between columns.

    def __init__(self, num_cols: int = 2, *, name_id: str = None, **config):
        super().__init__(columns=num_cols, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_managed_columns(name=self.id, **dpg_args)

    def __enter__(self) -> LayoutColumns:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()

    @property
    def column_widths(self) -> Sequence[float]:
        """Get or set column widths as a sequence of floats."""
        return tuple(
            dpgcore.get_managed_column_width(self.id, i)
            for i in range(self.columns)
        )

    @column_widths.setter
    def column_widths(self, widths: Sequence[float]) -> None:
        if len(widths) != self.columns:
            raise ValueError('incorrect number of widths')
        for i, width in enumerate(widths):
            dpgcore.set_managed_column_width(self.id, i, width)

    def get_column_width(self, col_idx: int) -> float:
        """Get an individual column width."""
        return dpgcore.get_managed_column_width(self.id, col_idx)

    def set_column_width(self, col_idx: int, width: float) -> None:
        """Set an individual column width."""
        dpgcore.set_managed_column_width(self.id, col_idx, width)


@_register_item_type('mvAppItemType::Child')
class ChildView(Widget, ItemWidget):
    """Adds an embedded child window with optional scollbars."""

    border: bool = ConfigProperty()
    autosize_x: bool = ConfigProperty()
    autosize_y: bool = ConfigProperty()
    menubar: bool = ConfigProperty()

    #: Disable scrollbars (can still scroll with mouse or programmatically).
    no_scrollbar: bool = ConfigProperty()

    #: Allow horizontal scrollbar to appear.
    horizontal_scrollbar: bool = ConfigProperty()

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_child(self.id, **dpg_args)

    def __enter__(self) -> ChildView:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()


@_register_item_type('mvAppItemType::Dummy')
class Dummy(Widget, ItemWidget):
    """Adds a spacer or 'dummy' widget."""
    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_dummy(name=self.id, **dpg_args)


__all__ = [
    'VSpacing',
    'HAlignNext',
    'group_horizontal',
    'LayoutGroup',
    'LayoutIndent',
    'LayoutColumns',
    'ChildView',
    'Dummy',
]