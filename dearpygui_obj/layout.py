"""Widgets for controlling layout."""

from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj.wrapper import PyGuiBase, dearpygui_wrapper, ConfigProperty

if TYPE_CHECKING:
    from typing import Tuple

@dearpygui_wrapper('mvAppItemType::Spacing')
class VSpacing(PyGuiBase):
    """Adds vertical spacing."""

    space: int = ConfigProperty(key='count') #: The amount of vertical space.

    def __init__(self, *, name_id: str = None, space: int = 1, show: bool = True):
        super().__init__(name_id, space=space, show=show)

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_spacing(name=self.id, **config)


@dearpygui_wrapper('mvAppItemType::SameLine')
class HAlignNext(PyGuiBase):
    """Places a widget on the same line as the previous widget.
    Can also be used for horizontal spacing."""

    xoffset: float = ConfigProperty() #: offset from containing window
    spacing: float = ConfigProperty() #: offset from previous widget

    def __init__(self, *, name_id: str = None, xoffset: float = 0.0, spacing: float = -1.0, show: bool = True):
        super().__init__(name_id, xoffset=xoffset, spacing=spacing, show=show)

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_same_line(name=self.id, **config)


@dearpygui_wrapper('mvAppItemType::Child')
class ScrollView(PyGuiBase):
    """Adds an embedded child window with optional scollbars."""

    border: bool = ConfigProperty()
    autosize_x: bool = ConfigProperty()
    autosize_y: bool = ConfigProperty()
    menubar: bool = ConfigProperty()

    #: Disable scrollbars (can still scroll with mouse or programmatically).
    no_scrollbar: bool = ConfigProperty()

    #: Allow horizontal scrollbar to appear.
    horizontal_scrollbar: bool = ConfigProperty()

    def __init__(self, *, name_id: str = None, show: bool = True, tooltip: str = '',
                 size: Tuple[int, int] = (0, 0), border: bool = True, autosize_x: bool = False,
                 autosize_y: bool = False, no_scrollbar: bool = False,
                 horizontal_scrollbar: bool = False, menubar: bool = False):

        super().__init__(
            name_id, show=show, tooltip=tooltip, size=size, border=border, autosize_x=autosize_x,
            autosize_y=autosize_y, no_scrollbar=no_scrollbar, horizontal_scrollbar=horizontal_scrollbar,
            menubar=menubar,
        )

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_child(self.id, width=10000)

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

    with Window('window', size=(1000, 300)):
        with child('scroll'):
            Button()



    start_dearpygui()

