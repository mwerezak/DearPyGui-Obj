"""An object-oriented Wrapper around DearPyGui 0.6"""

from __future__ import annotations

from warnings import warn
from collections import ChainMap
from typing import TYPE_CHECKING, Callable

import dearpygui.core as gui_core

if TYPE_CHECKING:
    from typing import Any, Optional, Type, Dict, Iterable, Mapping, Union

# DearPyGui's widget name scope is global, so I guess it's okay that this is too.
_ITEM_LOOKUP: Dict[str, GuiWrapper] = {}

# Used to construct the correct type when getting an item
# that was created outside the object wrapper library
_ITEM_TYPES: Dict[str, Callable[..., GuiWrapper]] = {}


def get_item_by_id(name: str) -> GuiWrapper:
    """Retrieve an item using its unique name.

    If the item was created by instantiating a :class:`GuiWrapper` object, this will return that
    object. Otherwise, a new wrapper object will be created for that item and returned. Future calls
    for the same ID will return the same object.

    Raises:
        KeyError: if name refers to an item that is invalid (deleted) or does not exist.
    """
    if not gui_core.does_item_exist(name):
        raise KeyError(f'"{name}" item does not exist')

    item = _ITEM_LOOKUP.get(name)
    if item is not None:
        return item

    ctor = _ITEM_TYPES.get(gui_core.get_item_type(name), GuiWrapper)
    return ctor(name = name)

def iter_all_items() -> Iterable[GuiWrapper]:
    """Iterate all items (*NOT* windows) and yield their wrapper objects."""
    for name in gui_core.get_all_items():
        yield get_item_by_id(name)

def iter_all_windows() -> Iterable[GuiWrapper]:
    """Iterate all windows and yield their wrapper objects."""
    for name in gui_core.get_windows():
        yield get_item_by_id(name)

def get_active_window() -> GuiWrapper:
    """Get the active window."""
    active = gui_core.get_active_window()
    return get_item_by_id(active)

def _register_item(name: str, instance: GuiWrapper) -> None:
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


def dearpygui_wrapper(item_type: str) -> Callable:
    """Associate a :class:`GuiWrapper` class or constructor with a DearPyGui item type.

    This decorator can be applied to a :class:`GuiWrapper` to associate it with a DearPyGui
    item type as returned by :func:`dearpygui.core.get_item_type`. This will let the wrapper object
    library know which constructor to use when :func:`get_item_by_id` is used to get an item that
    does not yet have a wrapper object.

    This constructor may be applied directly to :class:`GuiWrapper` subclasses, or it may be
    applied to any callable that can serve as a constructor. The only requirement is that the
    callable must have a 'name' keyword parameter that takes the unique name used by DearPyGui.
    """
    def decorator(ctor: Callable[..., GuiWrapper]):
        if item_type in _ITEM_TYPES:
            raise ValueError(f'"{item_type}" is already registered to {_ITEM_TYPES[item_type]!r}')
        _ITEM_TYPES[item_type] = ctor
        return ctor
    return decorator

class ConfigProperty:
    """Data descriptor used to get or set an item's configuration.

    This class provides a data descriptor API over top of the :func:`configure_item` and
    :func:`get_item_configuration` functions provided by DearPyGui.

    By default, it is used to get or set a single configuration key, which itself defaults to the
    attribute name given to the descriptor.

    This default behavior can be overidden by providing **fvalue** and **fconfig** converter
    methods, analogous to the way normal Python properties work.

    Both **fvalue** and **fconfig** must take exactly two arguments. The first argument for both
    is the :class:`GuiWrapper` instance that holds the descriptor.

    **fvalue** should take as its 2nd argument a dictionary of config values produced by
    :func:`dearpygui.core.get_item_configuration` and returns the value that is obtained when the
    descriptor is accessed.

    **fconfig** should do the reverse. Its 2nd argument should take the value that is being
    assigned to the descriptor, and it should return a dictionary of values that will be supplied to
    :func:`dearpygui.core.configure_item`.

    Ideally,
    ``fvalue(obj, fconfig(obj, value)) == value`` and
    ``fconfig(obj, fvalue(obj, config)) == config``
    should both be satisfied in order for configuration values to be stable.

    Also, if an **fconfig** function is given, adding the descriptor to an :class:`GuiWrapper`
    class will automatically create a custom keyword parameter. This can be prevented using the
    **no_keyword** argument.
    """

    _fvalue: Callable[[GuiWrapper, Mapping[str, Any]], Any]
    _fconfig: Callable[[GuiWrapper, Any], Mapping[str, Any]]

    def __init__(self,
                 fvalue: Optional[Callable] = None,
                 fconfig: Optional[Callable] = None,
                 key: Optional[str] = None,
                 no_keyword: bool = False,
                 doc: str = ''):
        """
        Parameters:
            fvalue: optional function to get a value from configuration.
            fconfig: optional function to get configuration data from an assigned value.
            key: the config key to get/set if **fvalue** and **fconfig** are not provided.
            no_keyword: if ``True``, don't add a custom keyword parameter to the owner of the descriptor.
            doc: custom docstring.
        """

        self.key = key
        self.no_keyword = no_keyword
        self.__doc__ = doc

        self.attr_name = None
        self.owner = None

        self.getvalue(fvalue)
        self.getconfig(fconfig)

    def __set_name__(self, owner: Type[GuiWrapper], name: str):
        self.owner = owner
        self.name = name

        if self.key is None:
            self.key = name

        if not self.__doc__:
            self.__doc__ = f'Access the \'{self.key}\' config property.'

        if not self.no_keyword:
            if self._fconfig is not None:
                owner.add_keyword_parameter(name, self._fconfig)
            elif self.key != name:
                # ensure that keyword parameters still work for config properties
                # that have a different name than the config key
                owner.add_keyword_parameter(name, lambda instance, value: {self.key : value})

    def __get__(self, instance: Optional[GuiWrapper], owner: Type[GuiWrapper]) -> Any:
        """Read the item configuration and return a value."""
        if instance is None:
            return self

        config = gui_core.get_item_configuration(instance.id)
        return (
            self._fvalue(instance, config) if self._fvalue is not None
            else config[self.key]
        )

    def __set__(self, instance: GuiWrapper, value: Any) -> None:
        """Modify the item configuration using the assigned value."""
        config = (
            self._fconfig(instance, value) if self._fconfig is not None
            else {self.key : value}
        )
        gui_core.configure_item(instance.id, **config)

    def __call__(self, fvalue: Callable):
        """Allows the ConfigProperty class itself to be used as a decorator which sets :attr:`fvalue`.

        This enables convenient syntax such as:

        .. code-block:: python

            class Widget(GuiWrapper):
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
            self.owner.add_keyword_parameter(self.name, fconfig)
        return self

config_property = ConfigProperty #: Alias for :class:`ConfigProperty` for use as a decorator.


class GuiWrapper:
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

        If **name** is given as a keyword parameter to ``__init__``, the value passed with that
        parameter will be processed with the function that was added by this method.

        This function should take two arguments, the instance being created and the value passed
        to the custom keyword parameter. It should return a dictionary of config values that will
        be added to the dictionary passed to :meth:`_setup_add_item` when creating the item.

        If the custom keyword parameter has already been added the previous one will be overwritten.

        Parameters:
            name: the name of the keyword argument to add.
            getconfig: a function that produces a dictionary of config items to be passed to
                :meth:`_setup_add_item`.
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

    tooltip: str = config_property(key='tip')
    width: int = config_property()
    height: int = config_property()
    show: bool = config_property()
    enabled: bool = config_property()

    @config_property(key='source')
    def data_source(self, config) -> Optional[GuiData]:
        """Get the :class:`GuiData` used as the data source, if any."""
        source = config.get('source')
        return GuiData(name=source) if source else None

    @data_source.getconfig
    def data_source(self, value: Optional[Union[GuiData, str]]):
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

        if label is not None and hasattr(self, 'label'):
            kwargs['label'] = label

        # at no point should a GuiWrapper object exist for an item that hasn't
        # actually been added, so if the item doesn't exist we need to add it now.
        if not gui_core.does_item_exist(self._name):
            config = self._create_config(kwargs)
            self._setup_add_widget(config)
        else:
            self._setup_preexisting()

        _register_item(self._name, self)

    def _create_config(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        config = {}
        for name, value in kwargs.items():
            get_config = self._keyword_params.get(name)
            if get_config is not None:
                config.update(get_config(self, value))
            else:
                config[name] = value

        return config

    ## Overrides

    def _setup_add_widget(self, config: Dict[str, Any]) -> None:
        """This method should be overriden by subclasses to add the wrapped GUI item using
        DearPyGui's ``add_*()`` functions.

        For example:

        .. code-block:: python

            class Button(GuiWrapper):
                def _setup_add_item(self, config):
                    dearpygui.core.add_button(self.id, **config)

        Parameters:
            config: a dictionary of config data that should be given to DearPyGui.
        """
        pass

    def _setup_preexisting(self) -> None:
        """This can be overriden by subclasses to setup an object wrapper that has been created
        for a pre-existing GUI item.

        There shouldn't usually be any extra setup required, as subclasses should try to draw all
        their data from DearPyGui's functions instead of duplicating state that already exists in
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

            with Window('Example Window'):
                button = Button('Callback Button')

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

    def get_parent(self) -> Optional[GuiWrapper]:
        parent_id = gui_core.get_item_parent(self.id)
        if not parent_id:
            return None
        return get_item_by_id(parent_id)

    def iter_children(self) -> Iterable[GuiWrapper]:
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
