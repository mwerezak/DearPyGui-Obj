from __future__ import annotations

from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type, wrap_callback
from dearpygui_obj.wrapper.widget import Widget, ItemWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional, Tuple, Callable
    from dearpygui_obj import PyGuiCallback
    from dearpygui_obj.wrapper.widget import ItemConfigData


class MainWindow:
    """Container for static functions used to manipulate the main window.

    Attempting to instantiate this class will raise a :class:`TypeError`.
    """

    def __new__(cls):
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


@_register_item_type('mvAppItemType::Window')
class Window(Widget):
    """Creates a new window."""

    label: str = ConfigProperty()
    x_pos: int = ConfigProperty()
    y_pos: int = ConfigProperty()
    autosize: bool = ConfigProperty()

    no_resize: bool = ConfigProperty()
    no_title_bar: bool = ConfigProperty()
    no_move: bool = ConfigProperty()
    no_collapse: bool = ConfigProperty()
    no_focus_on_appearing: bool = ConfigProperty()
    no_bring_to_front_on_focus: bool = ConfigProperty()
    no_close: bool = ConfigProperty()
    no_background: bool = ConfigProperty()

    show_menubar: bool = ConfigProperty(key='menubar')

    #: Disable scrollbars (can still scroll with mouse or programmatically).
    no_scrollbar: bool = ConfigProperty()

    #: Allow horizontal scrollbar to appear.
    horizontal_scrollbar: bool = ConfigProperty()

    pos: Tuple[int, int]
    @ConfigProperty()
    def pos(self) -> Tuple[int, int]:
        """Get or set (x_pos, y_pos) as a tuple."""
        config = self.get_config()
        return config['x_pos'], config['y_pos']

    @pos.getconfig
    def pos(self, value: Tuple[int, int]) -> ItemConfigData:
        width, height = value
        return {'x_pos': width, 'y_pos' : height}

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        """
        Parameters:
             label: window label.
        """
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_window(self.id, on_close=self._on_close, **dpg_args)

    def __enter__(self) -> Window:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()

    ## workaround for the fact that you can't set the on_close callback in DPG
    _on_close_callback: Optional[Callable] = None
    def _on_close(self, sender, data) -> None:
        if self._on_close_callback is not None:
            self._on_close_callback(sender, data)

    def on_close(self, callback: Optional[PyGuiCallback]) -> Callable:
        """Set on_close callback, can be used as a decorator."""
        if callback is not None:
            callback = wrap_callback(callback)
        self._on_close_callback = callback
        return callback

    def resized(self, callback: PyGuiCallback) -> Callable:
        """Set resized callback, can be used as a decorator."""
        dpgcore.set_resize_callback(wrap_callback(callback), handler=self.id)
        return callback


## Menu Bars and Menus

@_register_item_type('mvAppItemType::MenuBar')
class MenuBar(Widget, ItemWidget):
    """A menu bar that can be added to a :class:`.Window`."""

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_menu_bar(self.id, **dpg_args)

    def __enter__(self) -> MenuBar:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()


__all__ = [
    'MainWindow',
    'Window',
    'MenuBar',
]