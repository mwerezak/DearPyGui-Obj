"""An object-oriented Wrapper around DearPyGui 0.6"""

from __future__ import annotations

from warnings import warn
from collections import ChainMap
from typing import TYPE_CHECKING, Callable

import dearpygui.core as gui_core

if TYPE_CHECKING:
    from typing import Any, Optional, Type, Dict, Iterable, Mapping, Union

# DearPyGui's widget name scope is global, so I guess it's okay that this is too.
_ITEM_LOOKUP: Dict[str, ItemWrapper] = {}

# Used to construct the correct type when getting an item
# that was created outside the object wrapper library
_ITEM_TYPES: Dict[str, Callable[..., ItemWrapper]] = {}


def get_item_by_id(name: str) -> ItemWrapper:
    """Retrieve an item using its unique name.

    This function will create wrapper objects for GUI items that were not created using the object
    wrapper library.

    An attempt is made to ensure that calling this function on the same name will produce the same object.

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
    """Iterate all GUI items."""
    for name in gui_core.get_all_items():
        yield get_item_by_id(name)


def _register_item(name: str, instance: ItemWrapper) -> None:
    if name in _ITEM_LOOKUP:
        warn(f'item with name "{name}" already exists in global item registry, overwriting')
    _ITEM_LOOKUP[name] = instance

def _unregister_item(name: str, unregister_children: bool = True) -> None:
    _ITEM_LOOKUP.pop(name, None)
    if unregister_children:
        children = gui_core.get_item_children(name)
        if children is not None:
            for child_name in children:
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

    **fconfig** should be a function that does the reverse. It should produce a dictionary of
    values that will be supplied to :func:`dearpygui.core.configure_item`.

    Ideally,
    ``fvalue(fconfig(value)) == value`` and ``fconfig(fvalue(config)) == config``
    in order for configuration values to be stable.

    If **no_keyword** is ``False`` (the default) and **fconfig** is provided, a keyword parameter of
    the same name will be added to the class using **fconfig** to process it's value.
    """

    _fvalue: Callable[[Mapping[str, Any]], Any]
    _fconfig: Callable[[Any], Mapping[str, Any]]

    def __init__(self,
                 fvalue: Optional[Callable] = None,
                 fconfig: Optional[Callable] = None,
                 name: Optional[str] = None,
                 no_keyword: bool = False,
                 doc: str = ''):

        self.name = name
        self.no_keyword = no_keyword
        self.__doc__ = doc

        self.attr_name = None
        self.owner = None

        self.getvalue(fvalue)
        self.getconfig(fconfig)

    def __set_name__(self, owner: Type[ItemWrapper], name: str):
        self.owner = owner
        self.attr_name = name

        if self.name is None:
            self.name = name

        if not self.__doc__:
            self.__doc__ = f'Access the \'{self.name}\' config property.'

        if not self.no_keyword and self._fconfig is not None:
            owner.add_keyword_parameter(self.attr_name, self._fconfig)

    def __get__(self, instance: Optional[ItemWrapper], owner: Type[ItemWrapper]) -> Any:
        if instance is None:
            return self

        config = gui_core.get_item_configuration(instance.id)
        return (
            self._fvalue(config) if self._fvalue is not None
            else config[self.name]
        )

    def __set__(self, instance: ItemWrapper, value: Any) -> None:
        config = (
            self._fconfig(value) if self._fconfig is not None
            else {self.name : value}
        )
        gui_core.configure_item(instance.id, **config)

    def __call__(self, fvalue: Callable):
        """Allows the ConfigProperty itself to be used as a decorator which sets :attr:`fvalue`.

        This enables convenient syntax such as:

        .. code-block:: python

            class Widget(ItemWrapper):
                @config_property
                def property_name(config):
                    ...

        """
        self.getvalue(fvalue)
        return self

    def getvalue(self, fvalue: Callable):
        """Set :attr:`fvalue` using a decorator."""
        self._fvalue = fvalue
        if fvalue is not None:
            self.__doc__ = fvalue.__doc__ # use the docstring of the getter, the same way property() works
        return self

    def getconfig(self, fconfig: Callable):
        """Set :attr:`fconfig` using a decorator."""
        self._fconfig = fconfig
        if not self.no_keyword and self.owner is not None and fconfig is not None:
            self.owner.add_keyword_parameter(self.attr_name, fconfig)
        return self

config_property = ConfigProperty #: Convenience constructor for :class:`ConfigProperty`

class ItemWrapper:
    """This is the base class for all GUI item wrapper objects.

    Keyword arguments passed to `__init__` will be given to the :meth:`_setup_add_item` method used to
    add the item to DearPyGui. Subclasses may also specify custom keyword parameters using the
    :meth:`add_keyword_parameter` class method."""

    ## Custom keyword parameters

    # This is normally inherited. To prevent this, subclasses can override this attribute.
    _keyword_params = ChainMap()

    @classmethod
    def add_keyword_parameter(cls, name: str, getconfig: Optional[Callable] = None) -> None:
        """Can be used by subclasses to add custom keyword parameters.

        If a custom keyword parameter is given to ``__init__``, the value will be processed with the
        function that was added by this method. This function should return a dictionary of config
        values that will be added to the dictionary passed to :meth:`_setup_add_item` when creating
        the item.

        If the custom keyword parameter has already been added the previous one will be overwritten.

        Parameters:
            name: the name of the keyword argument to add.
            getconfig: a function that takes the value of the argument and produces a dictionary
                of config items to be passed to :meth:`_setup_add_item`.
        """

        # setup each subclass's config setup mapping
        config = cls.__dict__.get('_keyword_params')
        if config is None:
            # inherit keyword params from parent
            if hasattr(cls._keyword_params, 'new_child'):
                config = cls._keyword_params.new_child({})
            else:
                config = ChainMap({}, cls._keyword_params)
            setattr(cls, '_keyword_params', config)
        config[name] = getconfig

    ## Common GUI item properties

    label: str = config_property()
    tip: str = config_property()
    width: int = config_property()
    height: int = config_property()
    show: bool = config_property()
    enabled: bool = config_property()

    @config_property(name='source')
    def data_source(config) -> Optional[GuiData]:
        """Get the :class:`GuiData` used as the data source, if any."""
        source = config.get('source')
        return GuiData(name=source) if source else None

    @data_source.getconfig
    def data_source(value: Optional[Union[GuiData, str]]):
        # accept plain string in addition to GuiData
        return {'source' : str(value) if value else ''}


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
                function used by DearPyGui. If the item has any custom config parameters, these will
                be used to process the keyword argument values.
        """

        if name is not None:
            self._name = name
        else:
            self._name = f'{label or self.__class__.__name__}##{id(self):x}'

        if label is not None:
            kwargs['label'] = label

        # at no point should a ItemWrapper object exist for an item that hasn't
        # actually been added, so if the item doesn't exist we need to add it now.
        if not gui_core.does_item_exist(self._name):
            config = self._create_config(kwargs)
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

        For example:

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

    ## item/name reference

    @property
    def id(self) -> str:
        """The unique name used by DearPyGui to reference this GUI item."""
        return self._name

    @property
    def is_valid(self) -> bool:
        """This property is ``False`` if the GUI item has been deleted."""
        return gui_core.does_item_exist(self.id)

    def delete(self) -> None:
        """Delete the item, this will invalidate the item and all its children."""
        _unregister_item(self.id)
        gui_core.delete_item(self.id)


    ## Callbacks

    def set_callback(self, callback: Callable) -> None:
        """Set the callback used by DearPyGui."""
        gui_core.set_item_callback(self.id, callback)

    def get_callback(self) -> Any:
        """Get the callback used by DearPyGui."""
        return gui_core.get_item_callback(self.id)

    @property
    def callback_data(self) -> Any:
        """Get or set the callback data."""
        return gui_core.get_item_callback_data(self.id)

    @callback_data.setter
    def callback_data(self, data: Any) -> None:
        gui_core.set_item_callback_data(self.id, data)

    def callback(self, data: Optional[Any] = None) -> Callable:
        """A convenience decorator that sets the item's callback, and optionally, the callback data.

        For example:

        .. code-block:: python

            button = Button()

            @button.callback('some data')
            def callback(sender, data):
                ...
        """
        def decorator(callback: Callable):
            gui_core.set_item_callback(self.id, callback, callback_data=data)
            return callback
        return decorator


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

    For example:

    .. code-block:: python

        linked_text = GuiData('')

        with Window('Data Example'):
            TextInput('Text1', data_source = linked_text)
            TextInput('Text2', data_source = linked_text)
    """

    def __init__(self, value: Optional[Any] = None, name: Optional[str] = None):
        """If a value is provided, then the value is created in DearPyGui's Value Storage system.
        Otherwise, it is assumed that the object is another reference to an already existing value.

        Note:
            If the GuiData's name does not reference a value that exists, attempts to
            manipulate the value will also fail silently, and attempts to retrieve the value will
            produce ``None``.

            DearPyGui does not provide a function like :func:`does_item_exist` for values so it is
            impossible to detect this.

        Parameters:
            value: the value to store. If not provided, this will create a reference an existing
                value instead of creating a new value.
            name: The name of the value in the Value Storage system.
                If not provided, a name will be autogenerated. Must be given if **value** is not provided.
        """
        #: The unique name identifying the value in the Value Storage system.
        self.name = name or f'{id(self):x}'

        if value is not None:
            gui_core.add_value(self.name, value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name!r})'

    def __str__(self) -> str:
        return self.name

    @property
    def value(self) -> Any:
        """Get or set the value's... value."""
        return gui_core.get_value(self.name)

    @value.setter
    def value(self, new_value: Any) -> None:
        gui_core.set_value(self.name, new_value)
