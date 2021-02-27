"""The wrapper object system used to provide an object-oriented API for DearPyGui."""

from __future__ import annotations

from collections import ChainMap as chain_map
from typing import TYPE_CHECKING

from dearpygui import core as dpgcore
from dearpygui_obj import _ITEM_TYPES, _register_item, _unregister_item, get_item_by_id, GuiData

if TYPE_CHECKING:
    from typing import Callable, Mapping, Any, Optional, Union, Type, Iterable, Tuple, ChainMap


## Type Aliases
if TYPE_CHECKING:
    ItemConfigData = Mapping[str, Any]  #: Alias for GUI item configuration data
    GetValueFunc = Callable[['GuiWrapper'], Any]
    GetConfigFunc = Callable[['GuiWrapper', Any], ItemConfigData]
    DataSource = Union[GuiData, str]


def dearpygui_wrapper(item_type: str) -> Callable:
    """Associate a :class:`PyGuiBase` class or constructor with a DearPyGui item type.

    This decorator can be applied to a :class:`PyGuiBase` to associate it with a DearPyGui
    item type as returned by :func:`dearpygui.core.get_item_type`. This will let the wrapper object
    library know which constructor to use when :func:`get_item_by_id` is used to get an item that
    does not yet have a wrapper object.

    This constructor may be applied directly to :class:`PyGuiBase` subclasses, or it may be
    applied to any callable that can serve as a constructor. The only requirement is that the
    callable must have a 'name_id' keyword parameter that takes the unique name used by DearPyGui.
    """
    def decorator(ctor: Callable[..., PyGuiBase]):
        if item_type in _ITEM_TYPES:
            raise ValueError(f'"{item_type}" is already registered to {_ITEM_TYPES[item_type]!r}')
        _ITEM_TYPES[item_type] = ctor
        return ctor
    return decorator

class ConfigProperty:
    """Descriptor used to get or set an item's configuration."""

    def __init__(self,
                 key: Optional[str] = None, *,
                 add_init: bool = True,
                 doc: str = ''):
        """
        key: the config key to get/set with the default implementation.
        add_init: Add a custom keyword parameter if either _set_value() has a custom
            implementation the config key is different from the attribute name.
        doc: custom docstring.
        """
        self.owner = None
        self.key = key
        self.add_init = add_init
        self.__doc__ = doc

    def __set_name__(self, owner: Type[PyGuiBase], name: str):
        self.owner = owner
        self.name = name

        if self.key is None:
            self.key = name

        if not self.__doc__:
            self.__doc__ = f"Read or modify the '{self.key}' config field."

        # add an init parameter if add_init is True and either _set_value() has a custom
        # implementation or the config key is different from the attribute name
        if self.add_init:
            if self.key != name or self._get_config != ConfigProperty._get_config:
                owner.add_init_parameter(name, self._get_config)

    def __get__(self, instance: Optional[PyGuiBase], owner: Type[PyGuiBase]) -> Any:
        """Read the item configuration and return a value."""
        if instance is None:
            return self
        return self._get_value(instance)

    def __set__(self, instance: PyGuiBase, value: Any) -> None:
        config = self._get_config(instance, value)
        dpgcore.configure_item(instance.id, **config)

    def __call__(self, get_value: GetValueFunc):
        """Allows the ConfigProperty itself to be used as a decorator equivalent to :attr:`getvalue`."""
        return self.getvalue(get_value)

    _get_value: GetValueFunc
    _get_config: GetConfigFunc

    def getvalue(self, get_value: GetValueFunc):
        self._get_value = get_value
        self.__doc__ = get_value.__doc__ # use the docstring of the getter, the same way property() works
        return self

    def getconfig(self, get_config: GetConfigFunc):
        self._get_config = get_config
        if self.add_init and self.owner is not None:
            self.owner.add_init_parameter(self.name, self._get_config)
        return self

    ## default implementations

    def _get_value(self, instance: PyGuiBase) -> Any:
        return dpgcore.get_item_configuration(instance.id)[self.key]

    def _get_config(self, instance: PyGuiBase, value: Any) -> ItemConfigData:
        return {self.key : value}


class InitParameter:
    """Used as a decorator to mark methods as init parameter handlers."""
    def __init__(self, name: str):
        self.name = name

class PyGuiBase:
    """This is the base class for all GUI item wrapper objects.

    Keyword arguments passed to `__init__` will be given to the :meth:`_setup_add_item` method used to
    add the item to DearPyGui. Subclasses may also specify custom keyword parameters using the
    :meth:`add_init_parameter` class method."""

    ## Custom keyword parameters

    # This is normally inherited. To prevent this, subclasses can override this attribute.
    _init_params: ChainMap[str, GetConfigFunc] = chain_map()

    @classmethod
    def add_init_parameter(cls, name: str, getconfig: GetConfigFunc) -> None:
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
        keyword_params = cls.__dict__.get('_init_params')
        if keyword_params is None:
            # inherit keyword params from parent
            if hasattr(cls._init_params, 'new_child'):
                keyword_params = cls._init_params.new_child({})
            else:
                keyword_params = chain_map({}, cls._init_params)
            setattr(cls, '_init_params', keyword_params)
        keyword_params[name] = getconfig


    def __init__(self, *, name_id: Optional[str] = None, **config: Any):
        """
        Parameters:
            name: optional unique name used by DearPyGui to identify the GUI item.
                If omitted, a name will be autogenerated.
            **config: all other keyword arguments will be used to construct the item config data
                passed to :meth:`_setup_add_widget` when setting up the item.
        """

        if name_id is not None:
            self._name_id = name_id
        else:
            self._name_id = f'{self.__class__.__name__}##{id(self):x}'

        # at no point should a PyGuiBase object exist for an item that hasn't
        # actually been added, so if the item doesn't exist we need to add it now.
        if not dpgcore.does_item_exist(self._name_id):
            config = self._create_config(config)
            self._setup_add_widget(config)
        else:
            self._setup_preexisting()

        _register_item(self._name_id, self)

    # create the item configuration data from __init__ keyword arguments
    def _create_config(self, kwargs: ItemConfigData) -> ItemConfigData:
        config = {}
        for name, value in kwargs.items():
            get_config = self._init_params.get(name)
            if get_config is not None:
                config.update(get_config(self, value))
            else:
                config[name] = value

        return config

    ## Overrides

    def _setup_add_widget(self, config: ItemConfigData) -> None:
        """This method should be overriden by subclasses to add the wrapped GUI item using
        DearPyGui's ``add_*()`` functions.

        For example:

        .. code-block:: python

            class Button(PyGuiBase):
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
        return self._name_id

    @property
    def is_valid(self) -> bool:
        """This property is ``False`` if the GUI item has been deleted."""
        return dpgcore.does_item_exist(self.id)

    def delete(self) -> None:
        """Delete the item, this will invalidate the item and all its children."""
        _unregister_item(self.id)
        dpgcore.delete_item(self.id)

    ## Low level config

    def get_config(self) -> ItemConfigData:
        return dpgcore.get_item_configuration(self.id)

    def set_config(self, config: ItemConfigData) -> None:
        dpgcore.configure_item(self.id, **config)

    ## Callbacks

    def set_callback(self, callback: Callable) -> None:
        """Set the callback used by DearPyGui."""
        dpgcore.set_item_callback(self.id, callback)

    def get_callback(self) -> Any:
        """Get the callback used by DearPyGui."""
        return dpgcore.get_item_callback(self.id)

    @property
    def callback_data(self) -> Any:
        """Get or set the callback data."""
        return dpgcore.get_item_callback_data(self.id)

    @callback_data.setter
    def callback_data(self, data: Any) -> None:
        dpgcore.set_item_callback_data(self.id, data)

    def callback(self, *, data: Optional[Any] = None) -> Callable:
        """A decorator that sets the item's callback, and optionally, the callback data.

        For example:

        .. code-block:: python

            with Window('Example Window'):
                button = Button('Callback Button')

                @button.callback(data='this could also be a callable')
                def callback(sender, data):
                    ...
        """
        def decorator(callback: Callable) -> Callable:
            dpgcore.set_item_callback(self.id, callback, callback_data=data)
            return callback
        return decorator

    ## Parent/Children

    def get_parent(self) -> Optional[PyGuiBase]:
        """Get this item's parent."""
        parent_id = dpgcore.get_item_parent(self.id)
        if not parent_id:
            return None
        return get_item_by_id(parent_id)

    def set_parent(self, parent: PyGuiBase) -> None:
        """Re-parent the item, moving it."""
        dpgcore.move_item(self.id, parent=parent.id)

    def move_up(self) -> None:
        """Move the item up within its parent, if possible."""
        dpgcore.move_item_up(self.id)

    def move_down(self) -> None:
        """Move the item down within its parent, if possible."""
        dpgcore.move_item_down(self.id)

    def move_item_before(self, other: PyGuiBase) -> None:
        """Attempt to place the item before another item, re-parenting it if necessary."""
        dpgcore.move_item(self.id, parent=other.get_parent().id, before=other.id)

    ## Containers

    def is_container(self) -> bool:
        return dpgcore.is_item_container(self.id)

    def iter_children(self) -> Iterable[PyGuiBase]:
        children = dpgcore.get_item_children(self.id)
        if not children:
            return
        for child in children:
            yield get_item_by_id(child)

    def add_child(self, child: PyGuiBase) -> None:
        """Alternative to ``child.set_parent(self)``."""
        dpgcore.move_item(child.id, parent=self.id)

    ## Properties and status

    show: bool = ConfigProperty() #: Enable/disable rendering of the item.

    width: int = ConfigProperty()
    height: int = ConfigProperty()

    @ConfigProperty()
    def size(self) -> Tuple[float, float]:
        """The item's current size as (width, height)."""
        return tuple(dpgcore.get_item_rect_size(self.id))

    @size.getconfig
    def size(self, value: Tuple[float, float]) -> ItemConfigData:
        width, height = value
        return { 'width' : width, 'height' : height }

    @property
    def max_size(self) -> Tuple[float, float]:
        """An item's maximum allowable size as (width, height)."""
        return tuple(dpgcore.get_item_rect_max(self.id))

    @property
    def min_size(self) -> Tuple[float, float]:
        """An item's minimum allowable size as (width, height)."""
        return tuple(dpgcore.get_item_rect_min(self.id))

    tooltip: str = ConfigProperty(key='tip')
    enabled: bool = ConfigProperty()  #: If ``False``, display greyed out text and disable interaction.

    @ConfigProperty(key='source')
    def data_source(self) -> Optional[GuiData]:
        """Get the :class:`GuiData` used as the data source, if any."""
        source = self.get_config().get('source')
        return GuiData(name=source) if source else None

    @data_source.getconfig
    def data_source(self, value: Optional[DataSource]):
        # accept plain string in addition to GuiData
        return {'source' : str(value) if value else ''}

    # these are intentionally not properties, as they are status queries

    def is_visible(self) -> bool:
        """Checks if an item is visible on screen."""
        return dpgcore.is_item_visible(self.id)

    def is_hovered(self) -> bool:
        return dpgcore.is_item_hovered(self.id)

    def is_focused(self) -> bool:
        return dpgcore.is_item_focused(self.id)


import dearpygui_obj

# noinspection PyProtectedMember
if dearpygui_obj._default_ctor is None:
    dearpygui_obj._default_ctor = PyGuiBase