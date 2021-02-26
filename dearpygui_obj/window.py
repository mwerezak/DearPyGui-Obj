from __future__ import annotations

from typing import TYPE_CHECKING

import dearpygui.core as dpyguicore
from dearpygui_obj.wrapper import PyGuiWrapper, dearpygui_wrapper, config_property

if TYPE_CHECKING:
    from typing import Optional, Tuple, Callable


class MainWindow:
    """Container for static functions used to manipulate the main window."""

    def __new__(cls, *args, **kwargs):
        raise TypeError('this class may not be instantiated')

    @staticmethod
    def set_title(title: str) -> None:
        dpyguicore.set_main_window_title(title)

    @staticmethod
    def set_pos(x: int, y: int) -> None:
        dpyguicore.set_main_window_pos(x, y)

    @staticmethod
    def allow_resize(enabled: bool):
        dpyguicore.set_main_window_resizable(enabled)

    @staticmethod
    def set_size(width: int, height: int):
        dpyguicore.set_main_window_size(width, height)

    @staticmethod
    def get_size() -> Tuple[int, int]:
        return tuple(dpyguicore.get_main_window_size())

    @staticmethod
    def set_primary_window(window: Optional[Window]) -> None:
        """Sets a window as the primary window, or removes the primary window.

        When a window is set as the primary window it will fill the entire viewport.
        """
        if window is not None:
            dpyguicore.set_primary_window(window.id, True)
        else:
            dpyguicore.set_primary_window('', False)

    @staticmethod
    def set_resize_callback(callback: Callable):
        """Set a callback for when the main viewport is resized."""
        dpyguicore.set_resize_callback(callback, handler='')

    @staticmethod
    def enable_docking(**kwargs):
        """Enable docking and set docking options.

        Note:
            Once docking is enabled, it cannot be disabled.

        Keyword Arguments:
            shift_only: if ``True``, hold down shift for docking.
                If ``False``, dock by dragging window titlebars.
            dock_space: if ``True``, windows will be able to dock
                with the main window viewport.
        """
        dpyguicore.enable_docking(**kwargs)


@dearpygui_wrapper('mvAppItemType::Window')
class Window(PyGuiWrapper):
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
        dpyguicore.add_window(self.id, **config)

    def __enter__(self) -> Window:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpyguicore.end()

    def resized(self, callback: Callable):
        """Set resized callback, can be used as a decorator."""
        dpyguicore.set_resize_callback(callback, handler=self.id)
        return callback

if __name__ == '__main__':
    from dearpygui.core import *

    from dearpygui_obj import iter_all_windows

    for win in iter_all_windows():
        print(win.id, win.is_container())

    start_dearpygui()

