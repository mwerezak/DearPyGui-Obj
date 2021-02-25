from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from dearpygui_obj import ItemWrapper, dearpygui_wrapper

if TYPE_CHECKING:
    pass


@dearpygui_wrapper('mvAppItemType::Child')
class ScrollView(ItemWrapper):
    """Adds an embedded child window. Will show scrollbars when items do not fit.

    This is a container item."""

    def _setup_add_item(self, config) -> None:
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
            Button()
            Button()
            Button()
            Button()
            Button()


    for item in iter_all_items():
        print(item.id, get_item_type(item.id))

    start_dearpygui()

