from __future__ import annotations
from typing import Tuple, List

from dearpygui import core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper.widget import PyGuiWidget, ConfigProperty

__all__ = [
    'NodeEditor',
    'Node',
    'NodeAttribute',
]

@_register_item_type('mvAppItemType::NodeEditor')
class NodeEditor(PyGuiWidget):
    """A canvas specific to graph node workflow."""

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_node_editor(self.id, **dpg_args)

    def get_selected_links(self) -> List[List[str]]:
        """Get all links in the selected state."""
        return dpgcore.get_selected_links(self.id)

    def clear_selected_links(self) -> None:
        """Clears all links from being in the selection state."""
        dpgcore.clear_selected_links(self.id)

    def get_selected_nodes(self) -> List[str]:
        """Get all nodes in the selected state."""
        return dpgcore.get_selected_nodes(self.id)

    def clear_selected_nodes(self) -> None:
        """Clears all nodes from being in the selection state."""
        dpgcore.clear_selected_nodes(self.id)

    def get_links(self) -> List[List[str]]:
        """Gets all linkages for all nodes in the editor."""
        return dpgcore.get_links(self.id)

    def add_node_link(self, node1: NodeAttribute, node2: NodeAttribute) -> None:
        """Adds a node link between nodes."""
        dpgcore.add_node_link(self.id, node1.id, node2.id)

    def delete_node_link(self, node1: NodeAttribute, node2: NodeAttribute) -> None:
        """Deletes a node link if it exist."""
        dpgcore.delete_node_link(self.id, node1.id, node2.id)

    def __enter__(self) -> NodeEditor:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dpgcore.end()

@_register_item_type('mvAppItemType::Node')
class Node(PyGuiWidget):
    """A NodeEditor node."""

    label: str = ConfigProperty()
    draggable: bool = ConfigProperty()

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_node(self.id, **dpg_args)

    def __enter__(self) -> Node:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dpgcore.end()

@_register_item_type('mvAppItemType::NodeAttribute')
class NodeAttribute(PyGuiWidget):
    """Arbitrary attribute."""

    output: bool = ConfigProperty()
    static: bool = ConfigProperty()

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_node_attribute(self.id, **dpg_args)

    def __enter__(self) -> NodeAttribute:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dpgcore.end()
