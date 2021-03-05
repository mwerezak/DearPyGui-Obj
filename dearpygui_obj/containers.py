from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper import PyGuiWidget, ConfigProperty

if TYPE_CHECKING:
    pass

## Tree Nodes

@_register_item_type('mvAppItemType::TreeNode')
class TreeNode(PyGuiWidget):
    """A collapsing container with a label."""

    value: bool  #: ``True`` if the header is uncollapsed.

    label: str = ConfigProperty()
    closable: bool = ConfigProperty()
    default_open: bool = ConfigProperty()
    bullet: bool = ConfigProperty()  #: Display a bullet instead of arrow.

    #: If ``True``, a double click is needed to toggle
    open_on_double_click: bool = ConfigProperty()

    #: If ``True``, the user must click on the arrow/bullet to toggle
    open_on_arrow: bool = ConfigProperty()

    #: If ``True``, the header is always open and cannot be collapsed,
    #: and the arrow/bullet not shown (use as a convenience for leaf nodes).
    is_leaf: bool = ConfigProperty(key='leaf')

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        config.setdefault('show', True)  # workaround for DPG 0.6
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_tree_node(self.id, **dpg_args)

    def __enter__(self) -> TreeNode:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()


@_register_item_type('mvAppItemType::CollapsingHeader')
class TreeNodeHeader(TreeNode):
    """Similar to :class:`TreeNode`, but the label is visually emphasized."""

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_collapsing_header(self.id, **dpg_args)


## Menus and Menu Items

@_register_item_type('mvAppItemType::Menu')
class Menu(PyGuiWidget):
    """A menu containing :class:`MenuItem` objects.

    While they are often found inside a :class:`.MenuBar`, they are actually a general container
    that can be added anywhere and contain other kinds of widgets (e.g. buttons and text),
    even if it is unusual."""

    label: str = ConfigProperty()

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_menu(self.id, **dpg_args)

    def __enter__(self) -> Menu:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()


@_register_item_type('mvAppItemType::MenuItem')
class MenuItem(PyGuiWidget):
    """An item for a :class:`.Menu`."""

    label: str = ConfigProperty()

    #: Keyboard shortcut, e.g. `'CTRL+M'`.
    shortcut: str = ConfigProperty()

    #: If ``True``, a checkmark is shown if the item's :attr:`value` is ``True``.
    enable_check: bool = ConfigProperty(key='check')

    def __init__(self, label: str = None, value: bool = None, *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)
        if value is not None:
            self.value = value

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_menu_item(self.id, **dpg_args)
