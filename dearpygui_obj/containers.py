from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper import PyGuiObject, ConfigProperty

if TYPE_CHECKING:
    pass


## Menus and Menu Items

@_register_item_type('mvAppItemType::Menu')
class Menu(PyGuiObject):
    """A menu containing :class:`MenuItem` objects.

    While they are often found inside a :class:`.MenuBar`, they are actually a general container
    that can be added anywhere and contain other kinds of widgets (e.g. buttons and text),
    even if it is unusual."""

    label: str = ConfigProperty()

    def __init__(self, label: str = '', *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_menu(self.id, **dpg_args)

    def __enter__(self) -> Menu:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()


@_register_item_type('mvAppItemType::MenuItem')
class MenuItem(PyGuiObject):
    """An item for a :class:`.Menu`."""

    label: str = ConfigProperty()

    #: Keyboard shortcut, e.g. `'CTRL+M'`.
    shortcut: str = ConfigProperty()

    #: If ``True``, draw a checkmark inside the menu item.
    checked: bool = ConfigProperty(key='check')

    def __init__(self, label: str = '', *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_menu_item(self.id, **dpg_args)
