from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from dearpygui_obj import ItemWrapper, config_property, register_item_type

if TYPE_CHECKING:
    pass

@register_item_type('mvAppItemType::Window')
class Window(ItemWrapper):
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

    def _setup_add_item(self, config) -> None:
        gui_core.add_window(self.id, **config)

    def __enter__(self) -> Window:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        gui_core.end()

## Dev tool windows

@register_item_type('mvAppItemType::DebugWindow')
class DebugWindow(Window):
    """Developer tool, creates a window containing handy GUI debugging tools and info."""
    def _setup_add_item(self, config) -> None:
        gui_core.add_debug_window(self.id, **config)

@register_item_type('mvAppItemType::MetricsWindow')
class MetricsWindow(Window):
    """Developer tool, creates a metrics window."""
    def _setup_add_item(self, config) -> None:
        gui_core.add_metrics_window(self.id, **config)

@register_item_type('mvAppItemType::StyleWindow')
class StyleEditorWindow(Window):
    """Developer tool, creates a window containing a GUI style editor.."""
    def _setup_add_item(self, config) -> None:
        gui_core.add_style_window(self.id, **config)

@register_item_type('mvAppItemType::DocWindow')
class DocumentationWindow(Window):
    """Developer tool, creates a window showing DearPyGui documentation."""
    def _setup_add_item(self, config) -> None:
        gui_core.add_doc_window(self.id, **config)

@register_item_type('mvAppItemType::AboutWindow')
class AboutWindow(Window):
    """Developer tool, creates window containing information about DearPyGui."""
    def _setup_add_item(self, config) -> None:
        gui_core.add_about_window(self.id, **config)



if __name__ == '__main__':
    from dearpygui.core import *

    with StyleEditorWindow() as win:
        pass

    print(get_item_type(win.id))

    start_dearpygui()

