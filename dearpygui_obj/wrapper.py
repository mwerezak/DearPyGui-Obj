"""The wrapper object system used to provide an object-oriented API for DearPyGui."""

from __future__ import annotations

from collections import ChainMap as chain_map
from typing import TYPE_CHECKING

from dearpygui import core as dpgcore
from dearpygui_obj import (
    _ITEM_TYPES, _generate_id, _register_item, _unregister_item, get_item_by_id, DataValue,
)

if TYPE_CHECKING:
    from typing import Callable, Mapping, Any, Optional, Type, Iterable, Tuple, ChainMap, List


## Type Aliases
if TYPE_CHECKING:
    ItemConfigData = Mapping[str, Any]  #: Alias for GUI item configuration data

    GetValueFunc = Callable[['PyGuiObject'], Any]
    GetConfigFunc = Callable[['PyGuiObject', Any], ItemConfigData]

    #: Alias for GUI callback signature: callback(sender, data)
    PyGuiCallback = Callable[['PyGuiObject', Any], None]

    # Alias for callbacks used by DPG which take a string ID as sender.
    _DPGCallback = Callable[[str, Any], None]


def _dearpygui_wrapper(item_type: str) -> Callable:
    """Associate a :class:`PyGuiObject` class or constructor with a DearPyGui item type.

    This will let :func:`dearpygui_obj.get_item_by_id` know what constructor to use when getting
    an item that was not created by the object library."""
    def decorator(ctor: Callable[..., PyGuiObject]):
        if item_type in _ITEM_TYPES:
            raise ValueError(f'"{item_type}" is already registered to {_ITEM_TYPES[item_type]!r}')
        _ITEM_TYPES[item_type] = ctor
        return ctor
    return decorator

def _wrap_callback(callback: PyGuiCallback) -> _DPGCallback:
    """Wrap a :data:`PyGuiCallback` making it compatible with DPG."""
    def dpg_callback(sender: str, data: Any) -> None:
        return callback(get_item_by_id(sender), data)
    dpg_callback._internal_callback = callback
    return dpg_callback


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
        self.__doc__ = doc

    def __set_name__(self, owner: Type[PyGuiObject], name: str):
        self.owner = owner
        self.name = name

        owner.add_config_property(self)

        if self.key is None:
            self.key = name

        if not self.__doc__:
            self.__doc__ = f"Read or modify the '{self.key}' config field."

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

    def getvalue(self, get_value: GetValueFunc):
        self._get_value = get_value
        self.__doc__ = get_value.__doc__ # use the docstring of the getter, the same way property() works
        return self

    def getconfig(self, get_config: GetConfigFunc):
        self._get_config = get_config
        return self

    ## default implementations
    _get_value: GetValueFunc
    _get_config: GetConfigFunc

    def _get_value(self, instance: PyGuiObject) -> Any:
        return dpgcore.get_item_configuration(instance.id)[self.key]

    def _get_config(self, instance: PyGuiObject, value: Any) -> ItemConfigData:
        return {self.key : value}


class PyGuiObject:
    """This is the base class for all GUI item wrapper objects.

    Keyword arguments passed to ``__init__`` will be used to set the initial values of any
    :class:`ConfigProperty` descriptors added with :meth:`add_config_property`. Any left over
    keywords will be passed to the :meth:`_setup_add_widget` method to be given to DPG.

    It's important that PyGuiObject and subclasses can be instantiated with only the **name_id**
    argument being passed to ``__init__``. This allows :func:`.get_item_by_id` to work.

    Parameters:
        name_id: optionally specify the unique widget ID.
    """

    # subclasses can prevent inheritance of this by overriding it's value with a new mapping.
    _config_properties: ChainMap[str, ConfigProperty] = chain_map()

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
        if name_id is not None:
            self._name_id = name_id
        else:
            self._name_id = _generate_id(self)

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

            if 'label' in config and not config['label']:
                config['label'] = self.id

            for name, value in config.items():
                setattr(self, name, value)

        _register_item(self.id, self)

    def __repr__(self) -> str:
        return f'<{self.__class__.__qualname__}({self.id!r})>'

    def __str__(self) -> str:
        return self.id

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

    def set_callback(self, callback: PyGuiCallback) -> None:
        """Set the callback used by DearPyGui."""
        dpgcore.set_item_callback(self.id, wrap_callback(callback))

    def get_callback(self) -> PyGuiCallback:
        """Get the callback used by DearPyGui."""
        dpg_callback = dpgcore.get_item_callback(self.id)
        # this ensures we get the correct callback whether it is a wrapped callback
        # or something that was set from outside the object library
        return getattr(dpg_callback, '_internal_callback', dpg_callback)

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
        def decorator(callback: PyGuiCallback) -> PyGuiCallback:
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
        """Checks if DPG considers this item to be a container."""
        return dpgcore.is_item_container(self.id)

    def iter_children(self) -> Iterable[PyGuiObject]:
        """Iterates all of the item's children."""
        children = dpgcore.get_item_children(self.id)
        if not children:
            return
        for child in children:
            yield get_item_by_id(child)

    def add_child(self, child: PyGuiObject) -> None:
        """Alternative to :meth:`set_parent`."""
        dpgcore.move_item(child.id, parent=self.id)

    def create_child(self, child_type: Type[PyGuiObject], *args, **kwargs) -> PyGuiObject:
        """Add a child item after the container has already been setup.

        Not all child types are supported. Which ones are is entirely up to DearPyGui."""
        return child_type(*args, parent=self.id, **kwargs)

    ## Data and Values

    @ConfigProperty(key='source')
    def data_source(self) -> DataValue:
        """Get the :class:`GuiData` used as the data source, if any."""
        source_id = self.get_config().get('source') or self.id
        return DataValue(source_id)

    @data_source.getconfig
    def data_source(self, source: Optional[Any]):
        # accept plain string in addition to GuiData
        return {'source' : str(source) if source is not None else ''}

    @property
    def value(self) -> Any:
        # get_value(self.id) doesn't work if a data source has been set,
        # so we have to go through data_source to get the widget's value
        return self.data_source.value

    @value.setter
    def value(self, value: Any) -> None:
        self.data_source.value = value

    ## Other properties and status

    tooltip: str = ConfigProperty(key='tip')
    enabled: bool = ConfigProperty()  #: If not enabled, display greyed out text and disable interaction.

    @property
    def active(self) -> bool:
        """Get whether the item is being interacted with."""
        return dpgcore.is_item_active(self.id)

    show: bool = ConfigProperty() #: Enable/disable rendering of the item.

    width: int = ConfigProperty()
    height: int = ConfigProperty()

    @ConfigProperty()
    def size(self) -> Tuple[float, float]:
        """The item's current size as ``(width, height)``."""
        return tuple(dpgcore.get_item_rect_size(self.id))

    @size.getconfig
    def size(self, value: Tuple[float, float]) -> ItemConfigData:
        width, height = value
        return { 'width' : width, 'height' : height }

    @property
    def max_size(self) -> Tuple[float, float]:
        """An item's maximum allowable size as ``(width, height)``."""
        return tuple(dpgcore.get_item_rect_max(self.id))

    @property
    def min_size(self) -> Tuple[float, float]:
        """An item's minimum allowable size as ``(width, height)``."""
        return tuple(dpgcore.get_item_rect_min(self.id))

    # these are intentionally not properties, as they are status queries

    def is_visible(self) -> bool:
        """Checks if an item is visible on screen."""
        return dpgcore.is_item_visible(self.id)

    def is_hovered(self) -> bool:
        """Checks if an item is hovered."""
        return dpgcore.is_item_hovered(self.id)

    def is_focused(self) -> bool:
        """Checks if an item is focused."""
        return dpgcore.is_item_focused(self.id)

    def was_clicked(self) -> bool:
        """Checks if an item was just clicked (this frame?)"""
        return dpgcore.is_item_clicked(self.id)

    def was_activated(self) -> bool:
        """Checks if an item just became active (this frame?)"""
        return dpgcore.is_item_activated(self.id)

    def was_deactivated(self) -> bool:
        """Checks if an item just stopped being active (this frame?)."""
        return dpgcore.is_item_deactivated(self.id)

    def was_edited(self) -> bool:
        """Checks if an item was just edited (this frame?)"""
        return dpgcore.is_item_edited(self.id)

    def was_deactivated_after_edit(self) -> bool:
        """Checks if an item was edited and deactivated (this frame?)."""
        return dpgcore.is_item_deactivated_after_edit(self.id)


import dearpygui_obj

# noinspection PyProtectedMember
if dearpygui_obj._default_ctor is None:
    dearpygui_obj._default_ctor = PyGuiObject