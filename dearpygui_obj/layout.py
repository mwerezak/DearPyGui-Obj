from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from dearpygui_obj import GuiWrapper, dearpygui_wrapper, config_property

if TYPE_CHECKING:
    pass

@dearpygui_wrapper('mvAppItemType::Spacing')
class VSpacing(GuiWrapper):
    """Adds vertical spacing."""

    space: int = config_property(key='count') #: The amount of vertical space.

    def _setup_add_widget(self, config) -> None:
        gui_core.add_spacing(name=self.id, **config)


@dearpygui_wrapper('mvAppItemType::SameLine')
class HAlignNext(GuiWrapper):
    """Places a widget on the same line as the previous widget.
    Can also be used for horizontal spacing."""

    xoffset: float = config_property() #: offset from containing window
    spacing: float = config_property() #: offset from previous widget

    def _setup_add_widget(self, config) -> None:
        gui_core.add_same_line(name=self.id, **config)


@dearpygui_wrapper('mvAppItemType::Child')
class ScrollView(GuiWrapper):
    """Adds an embedded child window. Will show scrollbars when items do not fit.

    This is a container widget."""

    def _setup_add_widget(self, config) -> None:
        gui_core.add_child(self.id, **config)

    def __enter__(self) -> ScrollView:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.is_container():
            gui_core.end()


if __name__ == '__main__':
    from dearpygui.core import *
    from dearpygui_obj import *
    from dearpygui_obj.window import Window
    from dearpygui_obj.button import Button
    from dearpygui_obj.devtools import *

    with DebugWindow():
        pass

    with DocumentationWindow():
        pass

    with Window('Window'):
        with ScrollView():
            Button()
            HAlignNext(spacing=15)
            Button()
            HAlignNext(spacing=15)
            Button()
            VSpacing(space=5)
            Button()
            Button()
            VSpacing(space=10)
            Button()


    for item in iter_all_items():
        print(item.id, get_item_type(item.id))


    start_dearpygui()

