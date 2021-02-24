from __future__ import annotations

from warnings import warn
from typing import TYPE_CHECKING, Callable, ChainMap

import dearpygui.core as gui_core

if TYPE_CHECKING:
    from typing import Any, Optional, Type, Dict, Iterable, Union

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
        print(item_type, ctor)
        if item_type in _ITEM_TYPES:
            raise ValueError(f'"{item_type}" is already registered to {_ITEM_TYPES[item_type]!r}')
        _ITEM_TYPES[item_type] = ctor
        return ctor
    return decorator

def add_init_parameter(name: str, getconfig: Optional[Callable] = None):
    """Convenience decorator that calls the add_init_parameter() class method."""
    def decorator(cls: Type[GuiItem]):
        cls.add_init_parameter(name, getconfig)
        return cls
    return decorator

class ConfigProperty:
    """Data descriptor that accesses a GuiItem's config.

    Can optionally apply converters to customize the object's API:

    get_value(**config) is given the configuration of the item as keyword arguments, and should
    output a value that will be returned when the property is accessed.

    config_conv(value) is given a value, and should produce a dictionary of config items to update.

    Ideally,
    get_value(**get_config(value)) == value and get_config(get_value(**config)) == config
    in order for values to be stable.

    If add_parameter is True (the default), a keyword parameter of the same name will be added to
    the class holding this descriptor.
    """
    def __init__(self,
                 name: Optional[str] = None,
                 get_value: Optional[Callable] = None,
                 get_config: Optional[Callable] = None,
                 add_parameter: bool = True):

        self.name = name
        self.get_value = get_value or self._default_get_value
        self.get_config = get_config or self._default_get_config
        self.add_parameter = add_parameter

    def __set_name__(self, owner: Type[GuiItem], name: str):
        if self.name is None:
            self.name = name
        if self.add_parameter:
            # always use the attribute name for init parameters
            owner.add_init_parameter(name, self.get_config)

    def __get__(self, instance: Optional[GuiItem], owner: Type[GuiItem]) -> Any:
        if instance is None:
            return self
        return self.get_value(**gui_core.get_item_configuration(instance.id))

    def __set__(self, instance: GuiItem, value: Any) -> None:
        gui_core.configure_item(instance.id, **self.get_config(value))

    def _default_get_value(self, **config: Any) -> Any:
        return config[self.name]

    def _default_get_config(self, value: Any) -> Dict[str, Any]:
        return { self.name: value }

    def getvalue(self, converter: Callable):
        """Set get_value using a decorator."""
        self.get_value = converter

    def getconfig(self, converter: Callable):
        """Set setting get_config using a decorator."""
        self.get_config = converter


class GuiItem:
    """Base class for GUI Items."""
    label: str = ConfigProperty()
    tip: str = ConfigProperty()
    width: int = ConfigProperty()
    height: int = ConfigProperty()
    show: bool = ConfigProperty()
    enabled: bool = ConfigProperty()

    data: Union[GuiData, str] = ConfigProperty(
        get_value = lambda **config: GuiData(config['source']),
        get_config = lambda value: {'source' : str(value)},
    )

    _config_setup: ChainMap[str, Callable] = ChainMap[str, Callable]()

    @classmethod
    def add_init_parameter(cls, name: str, getconfig: Optional[Callable] = None) -> None:
        # setup each subclass's config setup mapping
        config = cls.__dict__.get('_config_setup')
        if config is None:
            config = cls._config_setup.new_child({}) # inherit properties from parent
            setattr(cls, '_config_setup', config)
        config[name] = getconfig

    def __init__(self,
                 label: Optional[str] = None, *,
                 name: Optional[str] = None,
                 **kwargs: Any):

        if name is not None:
            self._name = name
        else:
            self._name = f'{label or self.__class__.__name__}##{id(self):x}'

        if not gui_core.does_item_exist(self._name):
            config = self._create_config(kwargs)
            if label is not None:
                config['label'] = label

            # at no point should a GuiItem object exist for an item that hasn't
            # actually been added, so it is important to call this in __init__
            self._setup_add_item(config)
        else:
            self._setup_prexisting()

        _register_item(self._name, self)

    @classmethod
    def _create_config(cls, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        config = {}
        for name, value in kwargs.items():
            if name not in cls._config_setup:
                raise KeyError(f'{cls} does not have config parameter "{name}"')

            get_config = cls._config_setup[name]
            if get_config is not None:
                config.update(get_config(value))
            else:
                config[name] = value

        return config

    ## Overrides

    # This should be overriden to add the item using the given config.
    def _setup_add_item(self, config: Dict[str, Any]) -> None:
        pass

    # There shouldn't usually be any extra setup required, as members should draw from the
    # DearPyGui functions instead of duplicating state. But this can be overriden in case.
    def _setup_prexisting(self) -> None:
        pass

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

    def callback(self, data: Optional[Any]) -> Callable:
        """A function decorator that sets the item's callback, and optionally, the callback data."""
        def decorator(callback: Callable):
            gui_core.set_item_callback(self.id, callback, callback_data=data)
            return callback
        return decorator

    def set_callback(self, callback: Callable) -> None:
        gui_core.set_item_callback(self.id, callback)

    def get_callback(self) -> Any:
        return gui_core.get_item_callback(self.id)

    @property
    def callback_data(self) -> Any:
        return gui_core.get_item_callback_data(self.id)

    @callback_data.setter
    def callback_data(self, data: Any) -> None:
        gui_core.set_item_callback_data(self.id, data)


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


class GuiData:
    """Manipulate DearPyGui Value Storage.

    If an init_value provided, then the value is created in DearPyGui's Value Storage system.
    Otherwise, it is assumed that the object is another reference to an already existing value.

    Note that as of DearPyGui 0.6, if the initial attempt to create the value fails, attempts to
    manipulate the value will also fail silently, and attempts to retrieve the value will produce
    None. This appears to be undocumented implementation details of DearPyGui.
    """
    def __init__(self, value: Optional[Any] = None, name: Optional[str] = None):
        self.name = name or f'{id(self):x}'
        if value is not None:
            gui_core.add_value(self.name, value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name})'

    def __str__(self) -> str:
        return self.name

    @property
    def value(self) -> Any:
        return gui_core.get_value(self.name)

    @value.setter
    def value(self, new_value: Any) -> None:
        gui_core.set_value(self.name, new_value)
