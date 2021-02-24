from __future__ import annotations

from warnings import warn
from typing import TYPE_CHECKING, Callable

import dearpygui.core as gui_core

if TYPE_CHECKING:
    from typing import Any, Optional, Type, Dict, Iterable

# DearPyGui's widget name scope is global, so I guess it's okay that this is too.
_ITEM_LOOKUP: Dict[str, GuiItem] = {}

# Used to construct the correct type when getting an item
# that was created outside the object wrapper library
_ITEM_TYPES: Dict[str, Callable[..., GuiItem]] = {}


def get_item_by_id(name: str) -> GuiItem:
    """Retrieve an item using its unique name.

    This function can be used to create wrapper objects for DearPyGui items that were not created
    using the object wrapper library. An attempt is made to ensure that subsequent calls for the
    same name produce a reference to the same object.

    Raises:
        KeyError: if name refers to an item that is invalid (deleted) or does not exist.
    """
    if not gui_core.does_item_exist(name):
        raise KeyError(f'"{name}" item does not exist')

    item = _ITEM_LOOKUP.get(name)
    if item is not None:
        return item

    ctor = _ITEM_TYPES.get(gui_core.get_item_type(name), GuiItem)
    return ctor(name = name)

def iter_all_items() -> Iterable[GuiItem]:
    """Iterate all items."""
    for name in gui_core.get_all_items():
        yield get_item_by_id(name)


def _register_item(name: str, instance: GuiItem) -> None:
    if name in _ITEM_LOOKUP:
        warn(f'item with name "{name}" already exists in global item registry, overwriting')
    _ITEM_LOOKUP[name] = instance

def _unregister_item(name: str, unregister_children: bool = True) -> None:
    _ITEM_LOOKUP.pop(name, None)
    if unregister_children:
        for child_name in gui_core.get_item_children(name):
            _unregister_item(child_name, True)


def register_item_type(item_type: str) -> Callable:
    """This decorator is applied to a GuiItem constructor in order to register it with a DearPyGui
    item type as returned by dearpygui.core.get_item_type(). Constructors that are registered in
    this way are used by get_item_by_id() to create new instances when getting an item that was
    created outside of the object wrapper library.

    Constructors that are registered using this decorator are must have an __init__ that takes a
    'name' keyword parameter, which is used to supply the DearPyGui widget ID.
    """
    def decorator(ctor: Callable[..., GuiItem]):
        if item_type in _ITEM_TYPES:
            raise ValueError(f'"{item_type}" is already registered to {_ITEM_TYPES[item_type]!r}')
        _ITEM_TYPES[item_type] = ctor
        return ctor
    return decorator


_Callback = Callable[[str, Any], None]  # Type alias for DearPyGui callbacks

def _generate_id(o: GuiItem) -> str:
    return o.__class__.__qualname__ + '@' + hex(id(o))

class ConfigProperty:
    def __init__(self, name: Optional[str] = None):
        self.name = name

    def __set_name__(self, owner: Type[GuiItem], name: str):
        if self.name is None:
            self.name = name

    def __get__(self, instance: Optional[GuiItem], owner: Type[GuiItem]) -> Any:
        if instance is None:
            return self
        return gui_core.get_item_configuration(instance.id)[self.name]

    def __set__(self, instance: GuiItem, value: Any) -> None:
        gui_core.configure_item(instance.id, **{self.name : value})

class GuiItem:
    """Base class for GUI Items."""

    # TODO: data sources and callbacks
    # std::string source = "";
    # std::string before = "";
    # mvCallable callback = nullptr;
    # mvCallableData callback_data = nullptr;

    width: int = ConfigProperty()
    height: int = ConfigProperty()
    show: bool = ConfigProperty()
    enabled: bool = ConfigProperty()

    def __init__(self, name: Optional[str]):
        self._name = name or _generate_id(self)
        _register_item(self._name, self)

    @property
    def id(self) -> str:
        """The unique name used by DearPyGui to reference this GUI item."""
        return self._name

    @property
    def is_valid(self) -> bool:
        return gui_core.does_item_exist(self.id)

    def delete(self) -> None:
        """This will invalidate an item and all its children."""
        _unregister_item(self.id)
        gui_core.delete_item(self.id)


    ## Callbacks

    @property
    def callback(self) -> _Callback:
        return gui_core.get_item_callback(self.id)

    @callback.setter
    def callback(self, callback: _Callback) -> None:
        gui_core.set_item_callback(self.id, callback)

    @property
    def callback_data(self) -> Any:
        return gui_core.get_item_callback_data(self.id)

    @callback_data.setter
    def callback_data(self, data: Any) -> None:
        gui_core.set_item_callback_data(self.id, data)

    # in case you want to set callback and data on the same line
    def set_callback(self, callback: _Callback, data: Any) -> GuiItem:
        gui_core.set_item_callback(self.id, callback, callback_data=data)
        return self

    ## Containers/Children

    def is_container(self) -> bool:
        return gui_core.is_item_container(self.id)

    def get_parent(self) -> Optional[GuiItem]:
        parent_id = gui_core.get_item_parent(self.id)
        if not parent_id:
            return None
        return get_item_by_id(parent_id)

    def iter_children(self) -> Iterable[GuiItem]:
        children = gui_core.get_item_children(self.id)
        if not children:
            return
        for child in children:
            yield get_item_by_id(child)


