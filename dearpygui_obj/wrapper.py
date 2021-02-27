"""The wrapper object system used to provide an object-oriented API for DearPyGui."""

from __future__ import annotations

import inspect
from collections import ChainMap as chain_map
from typing import TYPE_CHECKING

from dearpygui import core as dpgcore
from dearpygui_obj import _ITEM_TYPES, _register_item, _unregister_item, get_item_by_id, GuiData

if TYPE_CHECKING:
    from typing import (
        Callable, Mapping, Any, Optional, Union, Type, Iterable, Tuple, ChainMap, List
    )


## Type Aliases
if TYPE_CHECKING:
    ItemConfigData = Mapping[str, Any]  #: Alias for GUI item configuration data
    GetValueFunc = Callable[['GuiWrapper'], Any]
    GetConfigFunc = Callable[['GuiWrapper', Any], ItemConfigData]
    DataSource = Union[GuiData, str]


def dearpygui_wrapper(item_type: str) -> Callable:
    """Associate a :class:`PyGuiObject` class or constructor with a DearPyGui item type.

    This will let :func:`dearpygui_obj.get_item_by_id` know what constructor to use when getting
    an item that was not created by the object library."""
    def decorator(ctor: Callable[..., PyGuiObject]):
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
        Parameters:
            key: the config key to get/set with the default implementation.
            add_init: If ``True``, add an init argument handler to the owner type.
            doc: custom docstring.
        """
        self.owner = None
        self.key = key
        self.add_init = add_init
        self.__doc__ = doc

    def __set_name__(self, owner: Type[PyGuiObject], name: str):
        self.owner = owner
        self.name = name

        owner.add_config_property(self)

        if self.key is None:
            self.key = name

        if not self.__doc__:
            self.__doc__ = f"Read or modify the '{self.key}' config field."

        # add an init parameter if add_init is True and either _set_value() has a custom
        # implementation or the config key is different from the attribute name
        if self.add_init:
            if self.key != name or self._get_config != ConfigProperty._get_config:
                owner.add_init_handler(name, self._get_config)

    def __get__(self, instance: Optional[PyGuiObject], owner: Type[PyGuiObject]) -> Any:
        if instance is None:
            return self
        return self._get_value(instance)

    def __set__(self, instance: PyGuiObject, value: Any) -> None:
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
            self.owner.add_init_handler(self.name, self._get_config)
        return self

    ## default implementations

    def _get_value(self, instance: PyGuiObject) -> Any:
        return dpgcore.get_item_configuration(instance.id)[self.key]

    def _get_config(self, instance: PyGuiObject, value: Any) -> ItemConfigData:
        return {self.key : value}

def dpg_setup_func(setup_func: Callable) -> Callable:
    """Decorator used to supply a setup function to :meth:`PyGuiObject.set_dpg_setup_func`"""
    def decorator(cls: Type[PyGuiObject]):
        cls.set_dpg_setup_func(setup_func)
        return cls
    return decorator


class PyGuiObject:
    """This is the base class for all GUI item wrapper objects.

    Keyword arguments passed to ``__init__`` will be given to the :meth:`_setup_add_item` method used to
    add the item to DearPyGui. Subclasses may also specify custom keyword parameters using the
    :meth:`add_init_handler` class method."""

    @classmethod
    def set_dpg_setup_func(cls, setup_func: Callable) -> None:
        cls._dpg_setup_func = setup_func

        setup_sig = inspect.signature(setup_func)
        cls._dpg_setup_keywords = [
            name for name, param in setup_sig.parameters.items()
            if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        ]

    # These are normally inherited. To prevent this, subclasses can override the attributes.
    _init_handlers: ChainMap[str, GetConfigFunc] = chain_map()
    _config_properties: ChainMap[str, ConfigProperty] = chain_map()

    @classmethod
    def add_init_handler(cls, name: str, getconfig: GetConfigFunc) -> None:
        """Add init parameter handlers.

        Parameters:
            name: the name of the init parameter to add.
            getconfig: a function that produces a dictionary of config key-value pairs to be passed
                to :meth:`_setup_add_item`.
        """

        # setup each subclass's config setup mapping
        init_handlers = cls.__dict__.get('_init_handlers')
        if init_handlers is None:
            # inherit keyword params from parent
            if hasattr(cls._init_handlers, 'new_child'):
                init_handlers = cls._init_handlers.new_child({})
            else:
                init_handlers = chain_map({}, cls._init_handlers)
            setattr(cls, '_init_handlers', init_handlers)
        init_handlers[name] = getconfig

    @classmethod
    def add_config_property(cls, prop: ConfigProperty) -> None:
        config_properties = cls.__dict__.get('_config_properties')
        if config_properties is None:
            # inherit keyword params from parent
            if hasattr(cls._config_properties, 'new_child'):
                config_properties = cls._config_properties.new_child({})
            else:
                config_properties = chain_map({}, cls._config_properties)
            setattr(cls, '_config_properties', config_properties)
        config_properties[prop.name] = prop

    @classmethod
    def get_config_properties(cls) -> List[str]:
        """Get the names of configuration properties as a list.

        This can be useful to check which attributes are configuration properties
        and therefore can be given as keywords to ``__init__``."""
        return list(cls._config_properties.keys())

    def __init__(self, *, name_id: Optional[str] = None, **kwargs: Any):
        """

        Parameters:
            name_id: optionally specify the object's ID instead of autogenerating it.
            \**kwargs: initial values for config properties and keyword arguments for DPG.
        """
        if name_id is not None:
            self._name_id = name_id
        else:
            self._name_id = f'{self.__class__.__name__}##{id(self):x}'

        if dpgcore.does_item_exist(self.id):
            self._setup_preexisting()
        else:
            # at no point should a PyGuiObject object exist for an item that hasn't
            # actually been added, so if the item doesn't exist we need to add it now.

            # set config properties after adding the widget
            config = {}
            for name, value in list(kwargs.items()):
                if name in self._config_properties:
                    config[name] = kwargs.pop(name)

            self._setup_add_widget(kwargs)

            for name, value in config.items():
                setattr(self, name, value)

        _register_item(self.id, self)

    # def _process_init_handlers(self, init_args):
    #     for name, value in init_args:
    #         handler = self._init_handlers.get(name)
    #         if handler is not None:
    #             yield from handler(self, value).items()
    #         else:
    #             yield name, value

    ## Overrides

    def _setup_add_widget(self, dpg_args: Mapping[str, Any]) -> None:
        """This should create the widget using DearPyGui's ``add_*()`` functions."""
        pass

    def _setup_preexisting(self) -> None:
        """This can be overriden by subclasses to setup an object wrapper that has been created
        for a pre-existing GUI item.

        Since we want to avoid duplicating state that already exists in DearPyGui, this method
        should rarely be needed."""
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

    def get_parent(self) -> Optional[PyGuiObject]:
        """Get this item's parent."""
        parent_id = dpgcore.get_item_parent(self.id)
        if not parent_id:
            return None
        return get_item_by_id(parent_id)

    def set_parent(self, parent: PyGuiObject) -> None:
        """Re-parent the item, moving it."""
        dpgcore.move_item(self.id, parent=parent.id)

    def move_up(self) -> None:
        """Move the item up within its parent, if possible."""
        dpgcore.move_item_up(self.id)

    def move_down(self) -> None:
        """Move the item down within its parent, if possible."""
        dpgcore.move_item_down(self.id)

    def move_item_before(self, other: PyGuiObject) -> None:
        """Attempt to place the item before another item, re-parenting it if necessary."""
        dpgcore.move_item(self.id, parent=other.get_parent().id, before=other.id)

    ## Containers

    def is_container(self) -> bool:
        return dpgcore.is_item_container(self.id)

    def iter_children(self) -> Iterable[PyGuiObject]:
        children = dpgcore.get_item_children(self.id)
        if not children:
            return
        for child in children:
            yield get_item_by_id(child)

    def add_child(self, child: PyGuiObject) -> None:
        """Alternative to ``child.set_parent(self)``."""
        dpgcore.move_item(child.id, parent=self.id)

    ## Data and Values

    @ConfigProperty(key='source')
    def data_source(self) -> Optional[GuiData]:
        """Get the :class:`GuiData` used as the data source, if any."""
        source = self.get_config().get('source')
        return GuiData(name=source) if source else None

    @data_source.getconfig
    def data_source(self, value: Optional[DataSource]):
        # accept plain string in addition to GuiData
        return {'source' : str(value) if value else ''}

    @property
    def value(self) -> Any:
        return dpgcore.get_value(self.id)

    @value.setter
    def value(self, new_value: Any) -> None:
        dpgcore.set_value(self.id, new_value)

    ## Other properties and status

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
    dearpygui_obj._default_ctor = PyGuiObject