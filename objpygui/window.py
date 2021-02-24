from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core

from objpygui.core import GuiItem, ConfigProperty, register_item_type

if TYPE_CHECKING:
    from typing import Optional

@register_item_type('mvAppItemType::Window')
class Window(GuiItem):
    x_pos: int = ConfigProperty()
    y_pos: int = ConfigProperty()
    autosize: bool = ConfigProperty()
    no_resize: bool = ConfigProperty()
    no_title_bar: bool = ConfigProperty()
    no_move: bool = ConfigProperty()
    no_scrollbar: bool = ConfigProperty()
    no_collapse: bool = ConfigProperty()
    horizontal_scrollbar: bool = ConfigProperty()
    no_focus_on_appearing: bool = ConfigProperty()
    no_bring_to_front_on_focus: bool = ConfigProperty()
    menubar: bool = ConfigProperty()
    no_close: bool = ConfigProperty()
    no_background: bool = ConfigProperty()
    label: str = ConfigProperty()

    def __init__(self, label: str, *, name: Optional[str] = None, **config):
        super().__init__(name)
        gui_core.add_window(self._name, label=label, **config)

    def __enter__(self) -> Window:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        gui_core.end()


if __name__ == '__main__':
    from dearpygui.core import *

    with Window('Test Window') as window:
        pass

    print(window.id)



