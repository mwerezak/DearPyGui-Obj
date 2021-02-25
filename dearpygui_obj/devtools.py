from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from dearpygui_obj import register_item_type
from dearpygui_obj.window import Window

if TYPE_CHECKING:
    pass


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
