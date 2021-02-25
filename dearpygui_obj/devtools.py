from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from dearpygui_obj import dearpygui_wrapper
from dearpygui_obj.window import Window

if TYPE_CHECKING:
    pass


@dearpygui_wrapper('mvAppItemType::DebugWindow')
class DebugWindow(Window):
    """Developer tool, creates a window containing handy GUI debugging info."""
    def _setup_add_widget(self, config) -> None:
        gui_core.add_debug_window(self.id, **config)

@dearpygui_wrapper('mvAppItemType::MetricsWindow')
class MetricsWindow(Window):
    """Developer tool, creates a metrics window."""
    def _setup_add_widget(self, config) -> None:
        gui_core.add_metrics_window(self.id, **config)

@dearpygui_wrapper('mvAppItemType::StyleWindow')
class StyleEditorWindow(Window):
    """Developer tool, creates a window containing a GUI style editor.."""
    def _setup_add_widget(self, config) -> None:
        gui_core.add_style_window(self.id, **config)

@dearpygui_wrapper('mvAppItemType::DocWindow')
class DocumentationWindow(Window):
    """Developer tool, creates a window showing DearPyGui documentation."""
    def _setup_add_widget(self, config) -> None:
        gui_core.add_doc_window(self.id, **config)

@dearpygui_wrapper('mvAppItemType::AboutWindow')
class AboutWindow(Window):
    """Developer tool, creates window containing information about DearPyGui."""
    def _setup_add_widget(self, config) -> None:
        gui_core.add_about_window(self.id, **config)
