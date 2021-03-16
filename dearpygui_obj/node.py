from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, NamedTuple, overload

from dearpygui import core as dpgcore

from dearpygui_obj import _register_item_type, try_get_item_by_id
from dearpygui_obj.wrapper.widget import PyGuiWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional, Iterable, List

__all__ = [
    'NodeEditor',
    'Node',
    'NodeAttribute',
    'NodeLink',
    'NodeAttributeType',
    'input_attribute',
    'output_attribute',
    'static_attribute',
]


class NodeLink(NamedTuple):
    """Holds info about a link between two :class:`.NodeAttribute` objects."""
    input: NodeAttribute
    output: NodeAttribute

def _get_link(end1: NodeAttribute, end2: NodeAttribute) -> Optional[NodeLink]:
    """Creates a NodeLink from an input and an output node.

    If exactly 1 input node and exactly 1 output node was not provided, returns ``None``."""
    endpoints = end1, end2

    inputs = [end for end in endpoints if end.link_behavior == NodeAttributeType.Input]
    if len(inputs) != 1:
        return None

    outputs = [end for end in endpoints if end.link_behavior == NodeAttributeType.Output]
    if len(inputs) != 1:
        return None

    return NodeLink(input=inputs[0], output=outputs[0])

def _get_link_from_ids(id1: str, id2: str) -> Optional[NodeLink]:
    end1 = try_get_item_by_id(id1)
    end2 = try_get_item_by_id(id2)
    if end1 is None or end2 is None:
        return None
    # noinspection PyTypeChecker
    return _get_link(end1, end2)

@_register_item_type('mvAppItemType::NodeEditor')
class NodeEditor(PyGuiWidget):
    """A canvas specific to graph node workflow.

    Should only contain :class:`.Node` objects. Any other kind of widget will not be displayed.
    """

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_node_editor(self.id, **dpg_args)

    def get_all_links(self) -> Iterable[NodeLink]:
        """Get all linkages between any :class:`.NodeAttribute` objects in the editor."""
        for id1, id2 in dpgcore.get_links(self.id):
            link = _get_link_from_ids(id1, id2)
            if link is not None:
                yield link

    def add_link(self, end1: NodeAttribute, end2: NodeAttribute) -> Optional[NodeLink]:
        """Adds a link between two :class:`.NodeAttribute` objects."""
        dpgcore.add_node_link(self.id, end1.id, end2.id)
        return _get_link(end1, end2)

    @overload
    def delete_link(self, end1: NodeAttribute, end2: NodeAttribute) -> None:
        ...
    @overload
    def delete_link(self, link: NodeLink) -> None:
        ...
    def delete_link(self, end1, end2 = None) -> None:
        """Deletes a link between two :class:`.NodeAttribute` objects if it exists."""
        if end2 is None:
            link = end1
            dpgcore.delete_node_link(self.id, link.input.id, link.output.id)
        else:
            dpgcore.delete_node_link(self.id, end1.id, end2.id)

    ## Node and Link Selection

    def get_selected_links(self) -> Iterable[NodeLink]:
        """Get all links in the selected state."""
        for id1, id2 in dpgcore.get_selected_links(self.id):
            link = _get_link_from_ids(id1, id2)
            if link is not None:
                yield link

    def clear_link_selection(self) -> None:
        """Clears all links from being in the selection state."""
        dpgcore.clear_selected_links(self.id)

    def get_selected_nodes(self) -> Iterable[Node]:
        """Get all nodes in the selected state."""
        for node_id in dpgcore.get_selected_nodes(self.id):
            node = try_get_item_by_id(node_id)
            if node is not None:
                yield node

    def clear_node_selection(self) -> None:
        """Clears all nodes from being in the selection state."""
        dpgcore.clear_selected_nodes(self.id)

    def __enter__(self) -> NodeEditor:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dpgcore.end()


@_register_item_type('mvAppItemType::Node')
class Node(PyGuiWidget):
    """A :class:`.NodeEditor` node.

    Should only contain :class:`.NodeAttribute` objects, any other kind of widget will not be
    displayed. Note that :class:`.NodeAttribute` objects may contain any kind or number of widget
    though."""

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

class NodeAttributeType(Enum):
    """Specifies how a :class:`.NodeAttribute` will link to other nodes."""
    Input  = None  #: Input nodes may only link to Output nodes.
    Output = 'output'  #: Output nodes may only link to Input nodes.
    Static = 'static'  #: Static nodes do not link. They are still useful as containers to place widgets inside a node.


def input_attribute(*, name_id: str = None) -> NodeAttribute:
    """Shortcut for ``NodeAttribute(NodeAttributeType.Input)``"""
    return NodeAttribute(NodeAttributeType.Input, name_id=name_id)

def output_attribute(*, name_id: str = None) -> NodeAttribute:
    """Shortcut for ``NodeAttribute(NodeAttributeType.Output)``"""
    return NodeAttribute(NodeAttributeType.Output, name_id=name_id)

def static_attribute(*, name_id: str = None) -> NodeAttribute:
    """Shortcut for ``NodeAttribute(NodeAttributeType.Static)``"""
    return NodeAttribute(NodeAttributeType.Static, name_id=name_id)


@_register_item_type('mvAppItemType::NodeAttribute')
class NodeAttribute(PyGuiWidget):
    """An attachment point for a :class:`.Node`."""

    type: NodeAttributeType
    @ConfigProperty()
    def type(self) -> NodeAttributeType:
        config = self.get_config()
        for mode in NodeAttributeType:
            if mode.value is not None and config.get(mode.value):
                return mode
        return NodeAttributeType.Input

    @type.getconfig
    def link_behavior(self, value: NodeAttributeType):
        return {
            mode.value : (mode == value)  for mode in NodeAttributeType if mode.value is not None
        }

    def __init__(self, type: NodeAttributeType = NodeAttributeType.Input, *, name_id: str = None, **config):
        super().__init__(type=type, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_node_attribute(self.id, **dpg_args)

    def __enter__(self) -> NodeAttribute:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dpgcore.end()
