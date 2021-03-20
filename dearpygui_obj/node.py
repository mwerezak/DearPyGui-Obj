from __future__ import annotations

from enum import Enum
from warnings import warn
from typing import TYPE_CHECKING, NamedTuple, overload

from dearpygui import core as dpgcore

from dearpygui_obj import _register_item_type, try_get_item_by_id, wrap_callback
from dearpygui_obj.wrapper.widget import Widget, ItemWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional, Iterable, Callable
    from dearpygui_obj import PyGuiCallback


class NodeLink(NamedTuple):
    """Holds info about a link between two :class:`.NodeAttribute` objects."""
    input: NodeAttribute   #: The input end of the link.
    output: NodeAttribute  #: The output end of the link.


## While I personally think it is better design to raise an exception here than return None,
## (so that the user can expect they will always have a NodeLink after a successful call to add_link)
## it doesn't seem appropriate to raise an exception for an operation that does not raise an exception
## in DPG. So lets generate warnings instead so at least the user can tell what went wrong.
def _get_link(end1: NodeAttribute, end2: NodeAttribute) -> Optional[NodeLink]:
    endpoints = end1, end2
    input, output = None, None
    for end in endpoints:
        if end.is_input():
            if input is not None:
                warn('attempt to link two node inputs')
                return None
            input = end
        if end.is_output():
            if output is not None:
                warn('attempt to link two node outputs')
                return None
            output = end
    if input is None:
        warn('did not provide a node input')
        return None
    if output is None:
        warn('did not provide a node output')
        return None

    return NodeLink(input=input, output=output)

def _get_link_from_ids(id1: str, id2: str) -> Optional[NodeLink]:
    end1 = try_get_item_by_id(id1)
    end2 = try_get_item_by_id(id2)
    if not isinstance(end1, NodeAttribute) or not isinstance(end2, NodeAttribute):
        warn('item ID does not reference a node attribute')
        return None
    return _get_link(end1, end2)

@_register_item_type('mvAppItemType::NodeEditor')
class NodeEditor(Widget, ItemWidget):
    """A canvas specific to graph node workflow.

    Should only contain :class:`.Node` objects. Any other kind of widget will not be displayed.
    """

    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_node_editor(
            self.id, link_callback=self._on_link, delink_callback=self._on_delink, **dpg_args,
        )

    def __enter__(self) -> NodeEditor:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dpgcore.end()

    ## Links

    def get_all_links(self) -> Iterable[NodeLink]:
        """Get all linkages between any :class:`.NodeAttribute` objects in the editor."""
        for id1, id2 in dpgcore.get_links(self.id):
            link = _get_link_from_ids(id1, id2)
            if link is None:
                warn('dearpygui.core.get_links() produced an invalid link (is there a bug in DPG?)')
            else:
                yield link

    def add_link(self, end1: NodeAttribute, end2: NodeAttribute) -> Optional[NodeLink]:
        """Adds a link between two :class:`.NodeAttribute` objects.

        Returns:
            A :class:`.NodeLink` representing the link that was created, or ``None``
            if the link was invalid.
        """
        dpgcore.add_node_link(self.id, end1.id, end2.id)
        return _get_link(end1, end2)

    @overload
    def delete_link(self, link: NodeLink) -> None:
        ...
    @overload
    def delete_link(self, end1: NodeAttribute, end2: NodeAttribute) -> None:
        ...
    def delete_link(self, end1, end2 = None) -> None:
        """Deletes a link between two :class:`.NodeAttribute` objects if a link exists."""
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
            if link is None:
                warn('dearpygui.core.get_selected_links() produced an invalid link (is there a bug in DPG?)')
            else:
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

    ## Callbacks

    ## workaround for the fact that you can't set the link_callback or delink_callback properties in DPG
    _on_link_callback: Optional[Callable] = None
    _on_delink_callback: Optional[Callable] = None

    def _on_link(self, sender, data) -> None:
        if self._on_link_callback is not None:
            self._on_link_callback(sender, data)

    def _on_delink(self, sender, data) -> None:
        if self._on_delink_callback is not None:
            self._on_delink_callback(sender, data)

    def link_callback(self, callback: Optional[PyGuiCallback]) -> Callable:
        """Set the link callback, can be used as a decorator."""
        if callback is not None:
            callback = wrap_callback(callback)
        self._on_link_callback = callback
        return callback

    def delink_callback(self, callback: Optional[PyGuiCallback]) -> Callable:
        """Set the delink callback, can be used as a decorator."""
        if callback is not None:
            callback = wrap_callback(callback)
        self._on_delink_callback = callback
        return callback


@_register_item_type('mvAppItemType::Node')
class Node(Widget, ItemWidget):
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
    """Shortcut constructor for ``NodeAttribute(NodeAttributeType.Input)``"""
    return NodeAttribute(NodeAttributeType.Input, name_id=name_id)

def output_attribute(*, name_id: str = None) -> NodeAttribute:
    """Shortcut constructor for ``NodeAttribute(NodeAttributeType.Output)``"""
    return NodeAttribute(NodeAttributeType.Output, name_id=name_id)

def static_attribute(*, name_id: str = None) -> NodeAttribute:
    """Shortcut constructor for ``NodeAttribute(NodeAttributeType.Static)``"""
    return NodeAttribute(NodeAttributeType.Static, name_id=name_id)

@_register_item_type('mvAppItemType::NodeAttribute')
class NodeAttribute(Widget, ItemWidget):
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
    def type(self, value: NodeAttributeType):
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

    def is_input(self) -> bool:
        """Shortcut for ``self.type == NodeAttributeType.Input``."""
        return self.type == NodeAttributeType.Input

    def is_output(self) -> bool:
        """Shortcut for ``self.type == NodeAttributeType.Output``."""
        return self.type == NodeAttributeType.Output

    def is_static(self) -> bool:
        """Shortcut for ``self.type == NodeAttributeType.Static``."""
        return self.type == NodeAttributeType.Static


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
