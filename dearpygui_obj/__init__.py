"""An object-oriented Wrapper around DearPyGui 0.6"""

from __future__ import annotations

from warnings import warn
from inspect import signature, Parameter
from typing import TYPE_CHECKING

from dearpygui import dearpygui as dpgcore

if TYPE_CHECKING:
    from typing import Dict, Iterable, Optional, Callable, Any, Union
    from dearpygui_obj.wrapper.widget import Widget
    from dearpygui_obj.window import Window

    ## Type Aliases
    PyGuiCallback = Union[
        # accept any of these signatures for callbacks
        Callable[[Widget, Any, Any], None],
        Callable[[Widget, Any], None],
        Callable[[Widget], None],
        Callable[[], None],
    ]

    # signature used by DPG
    _DPGCallback = Callable[[int, Any, Any], None]

# DearPyGui's widget ID scope is global, so I guess it's okay that this is too.
_ITEM_LOOKUP: Dict[int, Widget] = {}

# Used to construct the correct type when getting an item
# that was created outside the object wrapper library
_ITEM_TYPES: Dict[str, Callable[..., Widget]] = {}

# Fallback constructor used when getting a type that isn't registered in _ITEM_TYPES
_default_ctor: Optional[Callable[..., Widget]] = None


def get_item_by_id(widget_id: int) -> Widget:
    """Retrieve an item using its unique name.

    If the item was created by instantiating a :class:`.Widget` object, this will return that
    object. Otherwise, a new wrapper object will be created for that item and returned. Future calls
    for the same ID will return the same object.

    Raises:
        KeyError: if name refers to an item that is invalid (deleted) or does not exist.
    """
    if not dpgcore.does_item_exist(widget_id):
        raise KeyError(f"widget with id={widget_id} does not exist")

    item = _ITEM_LOOKUP.get(widget_id)
    if item is not None:
        return item

    item_type = dpgcore.get_item_type(widget_id) ## WARNING: this will segfault if name does not exist
    return _create_item_wrapper(widget_id, item_type)

def try_get_item_by_id(widget_id: int) -> Optional[Widget]:
    """Retrieve an item using its unique name or ``None``.

    Similar to :func:`.get_item_by_id`, but returns ``None`` if the wrapper object could not be retrieved."""
    if not dpgcore.does_item_exist(widget_id):
        return None

    item = _ITEM_LOOKUP.get(widget_id)
    if item is not None:
        return item

    item_type = dpgcore.get_item_type(widget_id) ## WARNING: this will segfault if name does not exist
    return _create_item_wrapper(widget_id, item_type)

def _create_item_wrapper(widget_id: int, item_type: str) -> Widget:
    ctor = _ITEM_TYPES.get(item_type, _default_ctor)
    if ctor is None:
        raise ValueError(f"could not create wrapper for widget with id={widget_id}: no constructor for item type '{item_type}'")
    return ctor(id=widget_id)

def iter_all_items() -> Iterable[Widget]:
    """Iterate all items and yield their wrapper objects."""
    for widget_id in dpgcore.get_all_items():
        yield get_item_by_id(widget_id)

def iter_all_windows() -> Iterable[Widget]:
    """Iterate all windows and yield their wrapper objects."""
    for window_id in dpgcore.get_windows():
        yield get_item_by_id(window_id)

def get_active_window() -> Widget:
    """Get the active window."""
    active_id = dpgcore.get_active_window()
    return get_item_by_id(active_id)

def _register_item(instance: Widget) -> None:
    item_id = instance.id
    if item_id in _ITEM_LOOKUP:
        warn(f"item with id='{item_id}' already exists in global item registry, overwriting")
    _ITEM_LOOKUP[item_id] = instance

def _unregister_item(widget_id: int, unregister_children: bool = True) -> None:
    _ITEM_LOOKUP.pop(widget_id, None)
    if unregister_children:
        children = dpgcore.get_item_children(widget_id)
        if children is not None:
            for child_id in children:
                _unregister_item(child_id, True)

def _register_item_type(item_type: str) -> Callable:
    """Associate a :class:`.Widget` class or constructor with a DearPyGui item type.

    This will let :func:`.get_item_by_id` know what constructor to use when getting
    an item that was not created by the object library."""
    def decorator(ctor: Callable[..., Widget]):
        if item_type in _ITEM_TYPES:
            raise ValueError(f"'{item_type}' is already registered to {_ITEM_TYPES[item_type]!r}")
        _ITEM_TYPES[item_type] = ctor
        return ctor
    return decorator

def _set_default_ctor(default_ctor: Callable[..., Widget]) -> None:
    global _default_ctor
    if _default_ctor is not None:
        raise ValueError(f"default ctor is already registered to {_default_ctor!r}")
    _default_ctor = default_ctor

_IDGEN_SEQ = 0
def _generate_id(o: Any) -> str:
    global _IDGEN_SEQ

    clsname = o.__class__.__name__
    while dpgcore.does_item_exist(name := clsname + '##' + str(_IDGEN_SEQ)):
        _IDGEN_SEQ += 1
    _IDGEN_SEQ += 1
    return name

## Start/Stop DearPyGui

def start_gui(*, primary_window: Window = None) -> None:
    """Start the GUI engine and show the main window."""
    if primary_window is not None:
        dpgcore.start_dearpygui(primary_window=primary_window.id)
    else:
        dpgcore.start_dearpygui()

def stop_gui() -> None:
    """Stop the GUI engine and exit the main window."""
    dpgcore.stop_dearpygui()

def is_running() -> bool:
    """Get the status of the GUI engine."""
    return dpgcore.is_dearpygui_running()

def set_start_callback(callback: Callable) -> None:
    """Fires when the main window is started."""
    dpgcore.set_start_callback(callback)  # not wrapped because sender will not be a widget anyways

def set_exit_callback(callback: Callable) -> None:
    """Fires when the main window is exited."""
    dpgcore.set_exit_callback(callback)  # not wrapped because sender will not be a widget anyways

def set_render_callback(callback: Callable) -> None:
    """Fires after rendering each frame."""
    dpgcore.set_render_callback(callback)  # not wrapped because sender will not be a widget anyways

def get_delta_time() -> float:
    """Get the time elapsed since the last frame."""
    return dpgcore.get_delta_time()

def get_total_time() -> float:
    """Get the time elapsed since the application started."""
    return dpgcore.get_total_time()

def enable_vsync(enabled: bool) -> None:
    """Enable or disable vsync"""
    return dpgcore.set_vsync(enabled)

## Value Storage System

def create_value(init_value: Any) -> DataValue:
    """Create a data value

    This can be handy if you need to refer to a value before the widgets that supply the value
    have been added. For example:

    .. code-block:: python

        linked_text = create_value('')
        with Window('Data Example'):
            ## using created value
            TextInput('Text1', data_source = linked_text)
            TextInput('Text2', data_source = linked_text)

            ## directly assign a widget as data source
            text3 = TextInput('Text3', data_source = linked_text)
            TextInput('Text4', data_source = text3)

    """
    proxy = DataValue(None)
    proxy.id = _generate_id(proxy)
    dpgcore.add_value(proxy.id, init_value)
    return proxy


class DataValue:
    """Proxy object for working with Dear PyGui's Value Storage System"""

    id: str

    def __init__(self, data_source: Any):
        self.id = str(data_source)

    def __repr__(self) -> str:
        return f'<{self.__class__.__qualname__}({self.id!r})>'

    def __str__(self) -> str:
        return self.id

    @property
    def value(self) -> Any:
        value = dpgcore.get_value(self.id)
        # need to return an immutable value since modifying the list wont actually change the value in DPG
        # if isinstance(value, list):
        #     value = tuple(value)
        return value

    @value.setter
    def value(self, value: Any) -> None:
        # if isinstance(value, Sequence):
        #     value = list(value)  # DPG only accepts lists for sequence values
        dpgcore.set_value(self.id, value)

## Callbacks

def wrap_callback(callback: PyGuiCallback) -> _DPGCallback:
    """Wraps callbacks that expect ``sender`` to be an object.

    DPG expects callbacks' sender argument to take the sender ID as a string.
    However it is convenient to write callbacks where the sender is an object.

    This can be used to wrap such callbacks, ensuring that the ID is resolved
    into an object before the wrapped callback is invoked.

    Note:
        DearPyGui-Obj will typically wrap callbacks for you so this function
        should only be needed if you are calling DPG functions yourself directly.
    """

    ## This is a workaround for the fact that DPG cannot use Callables as callbacks.
    wrapper_obj = CallbackWrapper(callback)
    def invoke_wrapper(sender, data):
        wrapper_obj(sender, data)
    invoke_wrapper.wrapped = wrapper_obj.wrapped
    return invoke_wrapper

def unwrap_callback(callback: Callable) -> Callable:
    """If the callback was wrapped with :func:`.wrap_callback`, this will unwrap it.

    Otherwise, the callback will just be returned unchanged.
    """
    return getattr(callback, 'wrapped', callback)

class CallbackWrapper:
    """Wraps callbacks that expect ``sender`` to be an object.

    DPG expects callbacks' sender argument to take the sender ID as a string.
    However it is convenient to write callbacks where the sender is an object.

    This can be used to wrap such callbacks, ensuring that the ID is resolved
    into an object before the wrapped callback is invoked.

    Parameters:
        callback: The callback to wrap.
    """

    def __init__(self, callback: PyGuiCallback):
        self.wrapped = callback

        positional = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
        sig = signature(callback)
        arg_count = sum(1 for param in sig.parameters.values() if param.kind in positional)
        if arg_count == 0:
            self._invoke = self._call_noargs
        elif arg_count == 1:
            self._invoke = self._call_sender_only
        else:
            self._invoke = self._call_sender_data

    def __call__(self, sender: str, data: Any) -> None:
        """Invoke the callback.

        Parameters:
            sender: The sender, typically given by DPG.
            data: The callback data, typically given by DPG.
        """
        self._invoke(sender, data)

    @staticmethod
    def _resolve_sender(sender: str) -> Any:
        if dpgcore.does_item_exist(sender):
            if sender in _ITEM_LOOKUP:
                return _ITEM_LOOKUP[sender]

            # warning, this will segfault if sender does not exist!
            sender_type = dpgcore.get_item_type(sender)
            return _create_item_wrapper(sender, sender_type)

    def _call_sender_data(self, sender: Any, data: Any) -> None:
        self.wrapped(self._resolve_sender(sender), data)

    def _call_sender_only(self, sender: Any, data: Any) -> None:
        self.wrapped(self._resolve_sender(sender))

    def _call_noargs(self, sender: Any, data: Any) -> None:
        self.wrapped()  # no need to resolve sender either!

__all__ = [
    'get_item_by_id',
    'try_get_item_by_id',
    'iter_all_items',
    'iter_all_windows',
    'get_active_window',
    'start_gui',
    'stop_gui',
    'is_running',
    'set_start_callback',
    'set_exit_callback',
    'set_render_callback',
    'get_delta_time',
    'get_total_time',
    'enable_vsync',
    'create_value',
    'DataValue',
    'wrap_callback',
    'unwrap_callback',
    'CallbackWrapper',
]