from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core

from objpygui import ItemWrapper, config_property, register_item_type

if TYPE_CHECKING:
    from typing import Optional

@register_item_type('mvAppItemType::Window')
class Window(ItemWrapper):
    x_pos: int = config_property()
    y_pos: int = config_property()
    autosize: bool = config_property()
    no_resize: bool = config_property()
    no_title_bar: bool = config_property()
    no_move: bool = config_property()
    no_scrollbar: bool = config_property()
    no_collapse: bool = config_property()
    horizontal_scrollbar: bool = config_property()
    no_focus_on_appearing: bool = config_property()
    no_bring_to_front_on_focus: bool = config_property()
    menubar: bool = config_property()
    no_close: bool = config_property()
    no_background: bool = config_property()

    def _setup_add_item(self, config) -> None:
        gui_core.add_window(self.id, **config)

    def __enter__(self) -> Window:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        gui_core.end()


if __name__ == '__main__':
    from dearpygui.core import *

    with Window('Test Window') as window:
        pass
    print(window.label)

    start_dearpygui()

