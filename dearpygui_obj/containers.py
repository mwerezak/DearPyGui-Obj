from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper.widget import Widget, ConfigProperty

if TYPE_CHECKING:
    pass

## Tree Nodes

@_register_item_type('mvAppItemType::TreeNode')
class TreeNode(Widget):
    """A collapsing container with a label."""

    value: bool  #: ``True`` if the header is uncollapsed, otherwise ``False``.

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
    """Similar to :class:`.TreeNode`, but the label is visually emphasized."""

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_collapsing_header(self.id, **dpg_args)

## Tab Container

@_register_item_type('mvAppItemType::TabBar')
class TabBar(Widget):
    """A container that allows switching between different tabs.

    Note:
        This container should only contain :class:`.TabItem` or :class:`.TabButton` elements.
    """

    reorderable: bool = ConfigProperty()

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_tab_bar(self.id, **dpg_args)

    def __enter__(self) -> TabBar:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()


class TabOrderMode(Enum):
    """Specifies the ordering behavior of a tab items."""
    Reorderable = None          #: Default
    Fixed       = 'no_reorder'  #: Disable reordering this tab or having another tab cross over this tab
    Leading     = 'leading'     #: Enforce the tab position to the left of the tab bar (after the tab list popup button)
    Trailing    = 'trailing'    #: Enforce the tab position to the right of the tab bar (before the scrolling buttons)

@_register_item_type('mvAppItemType::TabItem')
class TabItem(Widget):
    """A container whose contents will be displayed when selected in a :class:`.TabBar`.

    Note:
        This widget must be placed inside a :class:`.TabBar` to be visible.
    """

    label: str = ConfigProperty()

    #: Create a button on the tab that can hide the tab.
    closable: bool = ConfigProperty()

    order_mode: TabOrderMode
    @ConfigProperty()
    def order_mode(self) -> TabOrderMode:
        config = self.get_config()
        if config.get('leading'):
            return TabOrderMode.Leading
        if config.get('trailing'):
            return TabOrderMode.Trailing
        if config.get('no_reorder'):
            return TabOrderMode.Fixed
        return TabOrderMode.Reorderable

    @order_mode.getconfig
    def order_mode(self, value: TabOrderMode):
        return {
            mode.value : (mode == value)  for mode in TabOrderMode if mode.value is not None
        }

    #: Disable tooltip
    no_tooltip: bool = ConfigProperty()

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_tab(self.id, **dpg_args)

    def __enter__(self) -> TabItem:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        dpgcore.end()


@_register_item_type('mvAppItemType::TabButton')
class TabButton(Widget):
    """A button that can be added to a :class:`TabBar`.

    Note:
        This widget must be placed inside a :class:`.TabBar` to be visible.
    """

    label: str = ConfigProperty()

    #: Create a button on the tab that can hide the tab.
    closable: bool = ConfigProperty()

    order_mode: TabOrderMode
    @ConfigProperty()
    def order_mode(self) -> TabOrderMode:
        config = self.get_config()
        if config.get('leading'):
            return TabOrderMode.Leading
        if config.get('trailing'):
            return TabOrderMode.Trailing
        if config.get('no_reorder'):
            return TabOrderMode.Fixed
        return TabOrderMode.Reorderable

    @order_mode.getconfig
    def order_mode(self, value: TabOrderMode):
        return {
            mode.value : (mode == value)  for mode in TabOrderMode if mode.value is not None
        }

    #: Disable tooltip
    no_tooltip: bool = ConfigProperty()

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_tab_button(self.id, **dpg_args)


## Menus and Menu Items

@_register_item_type('mvAppItemType::Menu')
class Menu(Widget):
    """A menu containing :class:`.MenuItem` objects.

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
class MenuItem(Widget):
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


## Popups




__all__ = [
    'TreeNode',
    'TreeNodeHeader',
    'TabBar',
    'TabItem',
    'TabButton',
    'TabOrderMode',
    'Menu',
    'MenuItem',
]