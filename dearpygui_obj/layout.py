"""Widgets for controlling layout."""

from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj.wrapper import PyGuiObject, dearpygui_wrapper, ConfigProperty

if TYPE_CHECKING:
    from typing import Tuple

@dearpygui_wrapper('mvAppItemType::Spacing')
class VSpacing(PyGuiObject):
    """Adds vertical spacing."""

    space: int = ConfigProperty(key='count') #: The amount of vertical space.

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_spacing(name=self.id, **dpg_args)


@dearpygui_wrapper('mvAppItemType::SameLine')
class HAlignNext(PyGuiObject):
    """Places a widget on the same line as the previous widget.
    Can also be used for horizontal spacing."""

    xoffset: float = ConfigProperty() #: offset from containing window
    spacing: float = ConfigProperty() #: offset from previous widget

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_same_line(name=self.id, **dpg_args)


@dearpygui_wrapper('mvAppItemType::Child')
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
        if self.is_container():
            dpgcore.end()


if __name__ == '__main__':
    from dearpygui.core import *
    from dearpygui.simple import *
    from dearpygui_obj import *
    from dearpygui_obj.window import Window
    from dearpygui_obj.basic import Button
    from dearpygui_obj.devtools import *

    with Window():
        with ScrollView():
            Button()



    start_dearpygui()

