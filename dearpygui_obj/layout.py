"""Widgets for controlling layout."""

from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import _dearpygui_wrapper
from dearpygui_obj.wrapper import PyGuiObject, ConfigProperty

if TYPE_CHECKING:
    from typing import Tuple

@_dearpygui_wrapper('mvAppItemType::Spacing')
class VSpacing(PyGuiObject):
    """Adds vertical spacing."""

    space: int = ConfigProperty(key='count') #: The amount of vertical space.

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_spacing(name=self.id, **dpg_args)


@_dearpygui_wrapper('mvAppItemType::SameLine')
class HAlignNext(PyGuiObject):
    """Places a widget on the same line as the previous widget.
    Can also be used for horizontal spacing."""

    xoffset: float = ConfigProperty() #: offset from containing window
    spacing: float = ConfigProperty() #: offset from previous widget

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_same_line(name=self.id, **dpg_args)

def align_horizontal(spacing: float = -1, *, name_id: str = None) -> LayoutGroup:
    """Shortcut for ``LayoutGroup(horizontal=True)``"""
    return LayoutGroup(horizontal=True, horizontal_spacing=spacing, name_id=name_id)

@_dearpygui_wrapper('mvAppItemType::Group')
class LayoutGroup(PyGuiObject):
    """Grouped widgets behave as a single unit when acted on by e.g. :class:`HAlignNext`.

    They can optionally have their contents flow horizontally instead of vertically.
    """

    horizontal: bool = ConfigProperty()
    horizontal_spacing: float = ConfigProperty()

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_group(self.id, **dpg_args)

    def __enter__(self) -> LayoutGroup:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()

@_dearpygui_wrapper('mvAppItemType::Indent')
class LayoutIndent(PyGuiObject):
    """Adds an indent to contained items."""

    offset: float = ConfigProperty()

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_indent(name=self.id, **dpg_args)

    def __enter__(self) -> LayoutIndent:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.unindent()


@_dearpygui_wrapper('mvAppItemType::Child')
class ScrollView(PyGuiObject):
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

    def __enter__(self) -> ScrollView:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()


@_dearpygui_wrapper('mvAppItemType::Dummy')
class Dummy(PyGuiObject):
    """Adds a spacer or 'dummy' widget."""
    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_dummy(name=self.id, **dpg_args)


if __name__ == '__main__':
    from dearpygui.core import *
    from dearpygui.simple import *
    from dearpygui.demo import *
    from dearpygui_obj import *
    from dearpygui_obj.window import Window
    from dearpygui_obj.basic import Button
    from dearpygui_obj.devtools import *

    with window('window'):
        with group('group1', horizontal=True, horizontal_spacing=12):
            add_button('button1')
            add_button('button2')
            add_button('button3')


        add_button('button4')
        with LayoutIndent():
            add_button('button5')
            add_button('button6')
            with LayoutIndent():
                add_button('button7')
            add_button('button8')
            add_button('button9')

    show_demo()


    start_dearpygui()

