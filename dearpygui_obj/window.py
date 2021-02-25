from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from dearpygui_obj import GuiWrapper, config_property, dearpygui_wrapper

if TYPE_CHECKING:
    pass

@dearpygui_wrapper('mvAppItemType::Window')
class Window(GuiWrapper):
    """Creates a new window.

    This is a container item that should be used as a context manager. For example:

    .. code-block:: python

        with Window('Example Window'):
            TextInput('Child Input')
            Button('Child Button')

    """

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

    def _setup_add_widget(self, config) -> None:
        gui_core.add_window(self.id, **config)

    def __enter__(self) -> Window:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        gui_core.end()


if __name__ == '__main__':
    from dearpygui.core import *

    from dearpygui_obj import iter_all_windows

    for win in iter_all_windows():
        print(win.id, win.is_container())

    start_dearpygui()

