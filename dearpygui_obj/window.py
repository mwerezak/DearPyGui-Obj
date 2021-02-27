from __future__ import annotations

from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj.wrapper import PyGuiBase, dearpygui_wrapper, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional, Tuple, Callable
    from dearpygui_obj.wrapper import ItemConfigData


class MainWindow:
    """Container for static functions used to manipulate the main window.

    Attempting to instantiate this class will raise a :class:`TypeError`.
    """

    def __new__(cls, *args, **kwargs):
        raise TypeError('this class may not be instantiated')

    @staticmethod
    def set_title(title: str) -> None:
        dpgcore.set_main_window_title(title)

    @staticmethod
    def set_pos(x: int, y: int) -> None:
        dpgcore.set_main_window_pos(x, y)

    @staticmethod
    def allow_resize(enabled: bool):
        dpgcore.set_main_window_resizable(enabled)

    @staticmethod
    def set_size(width: int, height: int):
        dpgcore.set_main_window_size(width, height)

    @staticmethod
    def get_size() -> Tuple[int, int]:
        return tuple(dpgcore.get_main_window_size())

    @staticmethod
    def set_primary_window(window: Optional[Window]) -> None:
        """Set a window as the primary window, or remove the primary window.

        When a window is set as the primary window it will fill the entire viewport.

        If any other window was already set as the primary window, it will be unset.
        """
        if window is not None:
            dpgcore.set_primary_window(window.id, True)
        else:
            dpgcore.set_primary_window('', False)

    @staticmethod
    def set_resize_callback(callback: Callable):
        """Set a callback for when the main viewport is resized."""
        dpgcore.set_resize_callback(callback, handler='')

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
        dpgcore.enable_docking(**kwargs)


@dearpygui_wrapper('mvAppItemType::Window')
class Window(PyGuiBase):
    """Creates a new window.

    This is a container item that should be used as a context manager. For example:

    .. code-block:: python

        with Window('Example Window'):
            TextInput('Child Input')
            Button('Child Button')

    """

    label: str = ConfigProperty()
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

    @ConfigProperty()
    def pos(self) -> Tuple[int, int]:
        """Get or set (x_pos, y_pos) as a tuple."""
        config = self.get_config()
        return config['x_pos'], config['y_pos']

    @pos.getconfig
    def pos(self, value: Tuple[int, int]) -> ItemConfigData:
        width, height = value
        return {'x_pos': width, 'y_pos' : height}

    _on_close: Optional[Callable] = None

    def __init__(self, label: str, *, name_id: str = None, size: Tuple[int, int] = (-1, -1),
                 pos: Tuple[int, int] = (200, 200), autosize: bool = False, no_resize: bool = False,
                 no_title_bar: bool = False, no_move: bool = False, no_scrollbar: bool = False,
                 no_collapse: bool = False, horizontal_scrollbar: bool = False,
                 no_focus_on_appearing: bool = False, no_bring_to_front_on_focus: bool = False,
                 menubar: bool = False, no_close: bool = False, no_background: bool = False,
                 show: bool = True):

        super().__init__(
            name_id, label=label, size=size, pos=pos, autosize=autosize, no_resize=no_resize,
            no_title_bar=no_title_bar, no_move=no_move, no_scrollbar=no_scrollbar, no_collapse=no_collapse,
            horizontal_scrollbar=horizontal_scrollbar, no_focus_on_appearing=no_focus_on_appearing,
            no_bring_to_front_on_focus=no_bring_to_front_on_focus, menubar=menubar, no_close=no_close,
            no_background=no_background, show=show, on_close=self._handle_on_close,
        )

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_window(self.id, **config)

    def __enter__(self) -> Window:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()

    def _handle_on_close(self, sender, data) -> None:
        if self._on_close is not None:
            self._on_close(sender, data)

    def on_close(self, callback: Callable) -> Callable:
        """Set on_close callback, can be used as a decorator."""
        self._on_close = callback
        return callback

    def resized(self, callback: Callable) -> Callable:
        """Set resized callback, can be used as a decorator."""
        dpgcore.set_resize_callback(callback, handler=self.id)
        return callback

if __name__ == '__main__':
    from dearpygui.core import *

    from dearpygui_obj import iter_all_windows

    for win in iter_all_windows():
        print(win.id, win.is_container())

    start_dearpygui()

