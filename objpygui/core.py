from __future__ import annotations

from warnings import warn
from collections import ChainMap
from typing import TYPE_CHECKING, Callable

import dearpygui.core as gui_core

if TYPE_CHECKING:
    from typing import Any, Optional, Type, Dict, Iterable, Mapping

# DearPyGui's widget name scope is global, so I guess it's okay that this is too.
_ITEM_LOOKUP: Dict[str, ItemWrapper] = {}

# Used to construct the correct type when getting an item
# that was created outside the object wrapper library
_ITEM_TYPES: Dict[str, Callable[..., ItemWrapper]] = {}


def get_item_by_id(name: str) -> ItemWrapper:
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

    ctor = _ITEM_TYPES.get(gui_core.get_item_type(name), ItemWrapper)
    return ctor(name = name)

def iter_all_items() -> Iterable[ItemWrapper]:
    """Iterate all items."""
    for name in gui_core.get_all_items():
        yield get_item_by_id(name)


def _register_item(name: str, instance: ItemWrapper) -> None:
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
    def decorator(ctor: Callable[..., ItemWrapper]):
        print(item_type, ctor)
        if item_type in _ITEM_TYPES:
            raise ValueError(f'"{item_type}" is already registered to {_ITEM_TYPES[item_type]!r}')
        _ITEM_TYPES[item_type] = ctor
        return ctor
    return decorator


class ConfigProperty:
    """Data descriptor that accesses a GuiItem's config.

    Can optionally suppy **fvalue** and **fconfig** converter functions to customize how the
    object's API maps to config keys provided by DearPyGui.

    **fvalue** should be a function that takes a dictionary of config values produced by
    :func:`dearpygui.core.get_item_configuration` and returns the value that is obtained when the
    descriptor is accessed.

    ``fvalue(config)`` is given the configuration of the item as keyword arguments, and should
    output a value that will be returned when the property is accessed.

    ``fconfig(value)`` is given a value, and should produce a dictionary of config items to update.

    Ideally,
    ``get_value(get_config(value)) == value`` and ``get_config(get_value(config)) == config``
    in order for values to be stable.

    If add_parameter is True (the default), a keyword parameter of the same name will be added to
    the class holding this descriptor.
    """
    def __init__(self,
                 name: Optional[str] = None,
                 fvalue: Optional[Callable] = None,
                 fconfig: Optional[Callable] = None,
                 no_init: bool = False):

        self.name = name
        self.fvalue = fvalue
        self.fconfig = fconfig
        self.no_init = no_init

        self.__doc__ = fvalue.__doc__ if fvalue is not None else ''

    def __set_name__(self, owner: Type[ItemWrapper], name: str):
        if self.name is None:
            self.name = name

        if not self.no_init and self.fconfig is not None:
            # use the attribute name for config parameters
            # noinspection PyProtectedMember
            owner.add_keyword_parameter(name, self.fconfig)

    def __get__(self, instance: Optional[ItemWrapper], owner: Type[ItemWrapper]) -> Any:
        if instance is None:
            return self

        config = gui_core.get_item_configuration(instance.id)
        return (
            self.fvalue(config) if self.fvalue is not None
            else config[self.name]
        )

    def __set__(self, instance: ItemWrapper, value: Any) -> None:
        config = (
            self.fconfig(value) if self.fconfig is not None
            else {self.name : value}
        )
        gui_core.configure_item(instance.id, **config)

    def getvalue(self, converter: Callable):
        """Set :attr:`fvalue` using a decorator."""
        self.fvalue = converter
        return self

    def getconfig(self, converter: Callable):
        """Set :attr:`fconfig` using a decorator."""
        self.fconfig = converter
        return self


class ItemWrapper:
    """Base class for GUI item wrapper objects."""

    # Store custom keyword parameters
    # This is normally inherited. To prevent this, subclasses can override the attribute with an empty dict.
    _keyword_params = ChainMap()

    @classmethod
    def add_keyword_parameter(cls, name: str, getconfig: Optional[Callable] = None) -> None:
        """Can be used by subclasses to add custom keyword arguments.

        Parameters:
            name: the name of the keyword argument to add.
            getconfig: a function that takes the value of the argument and produces a dictionary
                of config items to be passed to :meth:`_setup_add_item`.
        """

        # setup each subclass's config setup mapping
        config = cls.__dict__.get('_keyword_params')
        if config is None:
            config = cls._keyword_params.new_child({}) # inherit keyword params from parent
            setattr(cls, '_keyword_params', config)
        elif not hasattr(config, 'new_child'):
            setattr(cls, '_keyword_params', ChainMap(config))
        config[name] = getconfig


    label: str = ConfigProperty()
    tip: str = ConfigProperty()
    width: int = ConfigProperty()
    height: int = ConfigProperty()
    show: bool = ConfigProperty()
    enabled: bool = ConfigProperty()

    data_source: Optional[GuiData] = ConfigProperty(
        fvalue = lambda config: GuiData(name=source) if (source := config.get('source')) else None,
        fconfig = lambda value: {'source' : str(value) if value else ''},
    ) #: Accesses the 'source' config key on GUI items.

    def __init__(self,
                 label: Optional[str] = None, *,
                 name: Optional[str] = None,
                 **kwargs: Any):
        """
        Parameters:
            label: optional initial value for the :attr:`label` property.
            name: optional unique name used to identify the GUI item.
                If omitted, a name will be autogenerated.
            **kwargs: all other keyword arguments will be passed to the underlying `add_*()`
                function used by DearPyGui. Subclasses may also specify custom keyword parameters
                using the :meth:`add_config_setup` class method.
        """

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
            self._setup_pre_existing()

        _register_item(self._name, self)

    @classmethod
    def _create_config(cls, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        config = {}
        for name, value in kwargs.items():
            get_config = cls._keyword_params.get(name)
            if get_config is not None:
                config.update(get_config(value))
            else:
                config[name] = value

        return config

    ## Overrides

    def _setup_add_item(self, config: Dict[str, Any]) -> None:
        """This method should be overriden by subclasses to add the wrapped GUI item using
        DearPyGui's ``add_*()`` functions.

        For Example:

        .. code-block:: python

            class Button(ItemWrapper):
                def _setup_add_item(config):
                    dearpygui.core.add_button(**config)

        Parameters:
            config: a dictionary of config data that should be given to DearPyGui.
        """
        pass

    def _setup_pre_existing(self) -> None:
        """This can be overriden by subclasses to setup an object wrapper that has been created
        for a pre-existing GUI item.

        There shouldn't usually be any extra setup required, as subclasses should draw all their
        data from DearPyGui's functions instead of duplicating state that already exists in
        DearPyGui. But it's available just in case.
        """
        pass

    @property
    def id(self) -> str:
        """The unique name used by DearPyGui to reference this GUI item."""
        return self._name

    @property
    def is_valid(self) -> bool:
        """This property is ``False`` if the GUI item has been deleted."""
        return gui_core.does_item_exist(self.id)

    def delete(self) -> None:
        """This method will invalidate the item and all its children."""
        _unregister_item(self.id)
        gui_core.delete_item(self.id)


    ## Callbacks

    def callback(self, data: Optional[Any] = None) -> Callable:
        """A function decorator that sets the item's callback, and optionally, the callback data.

        Example:
            .. code-block:: python

                button = Button()

                @button.callback
                def callback(sender, data):
                    ...
        """
        def decorator(callback: Callable):
            gui_core.set_item_callback(self.id, callback, callback_data=data)
            return callback
        return decorator

    def set_callback(self, callback: Callable) -> None:
        """Set the callback."""
        gui_core.set_item_callback(self.id, callback)

    def get_callback(self) -> Any:
        """Get the callback."""
        return gui_core.get_item_callback(self.id)

    @property
    def callback_data(self) -> Any:
        """Access the callback data."""
        return gui_core.get_item_callback_data(self.id)

    @callback_data.setter
    def callback_data(self, data: Any) -> None:
        gui_core.set_item_callback_data(self.id, data)


    ## Containers/Children

    def is_container(self) -> bool:
        return gui_core.is_item_container(self.id)

    def get_parent(self) -> Optional[ItemWrapper]:
        parent_id = gui_core.get_item_parent(self.id)
        if not parent_id:
            return None
        return get_item_by_id(parent_id)

    def iter_children(self) -> Iterable[ItemWrapper]:
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
        return f'{self.__class__.__name__}({self.name!r})'

    def __str__(self) -> str:
        return self.name

    @property
    def value(self) -> Any:
        return gui_core.get_value(self.name)

    @value.setter
    def value(self, new_value: Any) -> None:
        gui_core.set_value(self.name, new_value)
