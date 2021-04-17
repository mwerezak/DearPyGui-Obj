from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type, get_item_by_id
from dearpygui_obj.window import Window

if TYPE_CHECKING:
    pass


@_register_item_type('mvAppItemType::DebugWindow')
class DebugWindow(Window):

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    """Developer tool, creates a window containing handy GUI debugging info."""
    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_debug_window(self.id, **dpg_args)
        dpgcore.end()

    @classmethod
    def get_instance(cls):
        """Get the standard instance that is automatically created by DPG."""
        return get_item_by_id('debug##standard')

    @classmethod
    def show_debug(cls) -> None:
        """Show the standard instance that is automatically created by DPG."""
        cls.get_instance().show = True


@_register_item_type('mvAppItemType::MetricsWindow')
class MetricsWindow(Window):
    """Developer tool, creates a metrics window."""

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_metrics_window(self.id, **dpg_args)
        dpgcore.end()

    @classmethod
    def get_instance(cls):
        """Get the standard instance that is automatically created by DPG."""
        return get_item_by_id('metrics##standard')

    @classmethod
    def show_metrics(cls) -> None:
        """Show the standard instance that is automatically created by DPG."""
        cls.get_instance().show = True

@_register_item_type('mvAppItemType::StyleWindow')
class StyleEditorWindow(Window):
    """Developer tool, creates a window containing a GUI style editor.."""

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_style_window(self.id, **dpg_args)
        dpgcore.end()

    @classmethod
    def get_instance(cls):
        """Get the standard instance that is automatically created by DPG."""
        return get_item_by_id('style##standard')

    @classmethod
    def show_style_editor(cls) -> None:
        """Show the standard instance that is automatically created by DPG."""
        cls.get_instance().show = True

@_register_item_type('mvAppItemType::DocWindow')
class DocumentationWindow(Window):
    """Developer tool, creates a window showing DearPyGui documentation."""

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_doc_window(self.id, **dpg_args)
        dpgcore.end()

    @classmethod
    def get_instance(cls):
        """Get the standard instance that is automatically created by DPG."""
        return get_item_by_id('documentation##standard')

    @classmethod
    def show_documentation(cls) -> None:
        """Show the standard instance that is automatically created by DPG."""
        cls.get_instance().show = True

@_register_item_type('mvAppItemType::AboutWindow')
class AboutWindow(Window):
    """Developer tool, creates window containing information about DearPyGui."""

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_about_window(self.id, **dpg_args)
        dpgcore.end()

    @classmethod
    def get_instance(cls):
        """Get the standard instance that is automatically created by DPG."""
        return get_item_by_id('about##standard')

    @classmethod
    def show_about(cls) -> None:
        """Show the standard instance that is automatically created by DPG."""
        cls.get_instance().show = True


__all__ = [
    'DebugWindow',
    'MetricsWindow',
    'StyleEditorWindow',
    'DocumentationWindow',
    'AboutWindow',
]