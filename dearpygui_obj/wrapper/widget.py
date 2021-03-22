"""The wrapper object system used to provide an object-oriented API for DearPyGui."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from dearpygui import core as dpgcore
from dearpygui_obj import (
    _generate_id, _set_default_ctor,
    _register_item, _unregister_item,
    wrap_callback, unwrap_callback,
    get_item_by_id, DataValue,
)

if TYPE_CHECKING:
    from typing import Callable, Mapping, Any, Optional, Type, Iterable, Tuple, Sequence
    from dearpygui_obj import PyGuiCallback

    ## Type Aliases
    ItemConfigData = Mapping[str, Any]  #: Alias for GUI item configuration data

    GetValueFunc = Callable[['Widget'], Any]
    GetConfigFunc = Callable[['Widget', Any], ItemConfigData]


## WIDGET WRAPPERS

class ConfigProperty:
    """Descriptor used to get or set an item's configuration."""

    def __init__(self,
                 key: Optional[str] = None, *,
                 no_init: bool = False,
                 doc: str = ''):
        """
        Parameters:
            key: the config key to get/set with the default implementation.
            no_init: If ``True``, don't receive initial value from the widget constructor.
            doc: custom docstring.
        """
        self.owner = None
        self.key = key
        self.no_init = no_init
        self.__doc__ = doc

    def __set_name__(self, owner: Type[Widget], name: str):
        self.owner = owner
        self.name = name

        if self.key is None:
            self.key = name

        if not self.__doc__:
            self.__doc__ = f"Read or modify the '{self.key}' config property."

    def __get__(self, instance: Optional[Widget], owner: Type[Widget]) -> Any:
        if instance is None:
            return self
        return self.fvalue(instance)

    def __set__(self, instance: Widget, value: Any) -> None:
        config = self.fconfig(instance, value)
        dpgcore.configure_item(instance.id, **config)

    def __call__(self, fvalue: GetValueFunc):
        """Allows the ConfigProperty itself to be used as a decorator equivalent to :attr:`getvalue`."""
        return self.getvalue(fvalue)

    def getvalue(self, fvalue: GetValueFunc):
        self.fvalue = fvalue
        self.__doc__ = fvalue.__doc__ # use the docstring of the getter, the same way property() works
        return self

    def getconfig(self, fconfig: GetConfigFunc):
        self.fconfig = fconfig
        return self

    ## default implementations
    fvalue: GetValueFunc
    fconfig: GetConfigFunc

    def fvalue(self, instance: Widget) -> Any:
        return dpgcore.get_item_configuration(instance.id)[self.key]

    def fconfig(self, instance: Widget, value: Any) -> ItemConfigData:
        return {self.key : value}



class Widget(ABC):
    """This is the abstract base class for all GUI item wrapper objects.

    Keyword arguments passed to ``__init__`` will be used to set the initial values of any
    config properties that belong to the class. Any left over keywords will be passed to the
    :meth:`_setup_add_widget` method to be given to DPG.

    You can find out what config properties there are using the
    :meth:`get_config_properties` method.

    It's important that any subclasses can be instantiated with only the **name_id**
    argument being passed to ``__init__``. This allows :func:`.get_item_by_id` to work.

    Parameters:
        name_id: optionally specify the unique widget ID.
    """

    @classmethod
    def _get_config_properties(cls) -> Mapping[str, ConfigProperty]:
        config_properties = cls.__dict__.get('_config_properties')
        if config_properties is None:
            config_properties = {}
            for name in dir(cls):
                value = getattr(cls, name)
                if isinstance(value, ConfigProperty):
                    config_properties[name] = value
            setattr(cls, '_config_properties', config_properties)
        return config_properties

    @classmethod
    def get_config_properties(cls) -> Sequence[str]:
        """Get the names of configuration properties as a list.

        This can be useful to check which attributes are configuration properties
        and therefore can be given as keywords to ``__init__``."""
        return list(cls._get_config_properties().keys())

    def __init__(self, *, name_id: Optional[str] = None, **kwargs: Any):
        if name_id is not None:
            self._name_id = name_id
        else:
            self._name_id = _generate_id(self)

        if dpgcore.does_item_exist(self.id):
            self._setup_preexisting()
        else:
            # at no point should a Widget object exist for an item that hasn't
            # actually been added, so if the item doesn't exist we need to add it now.

            # labels are handled specially because they are very common
            if 'label' in kwargs and kwargs['label'] is None:
                kwargs['label'] = self.id

            # subclasses will pass both config values and keywords to _setup_add_widget()
            # separate them now
            config_props = self._get_config_properties()
            config_args = {}
            for name, value in list(kwargs.items()):
                prop = config_props.get(name)
                if prop is not None and not prop.no_init:
                    config_args[prop] = kwargs.pop(name)

            # just keywords left in kwargs
            self._setup_add_widget(kwargs)

            config_data = {}
            for prop, value in config_args.items():
                config_data.update(prop.fconfig(self, value))

            dpgcore.configure_item(self.id, **config_data)

        _register_item(self.id, self)

    def __repr__(self) -> str:
        return f'<{self.__class__.__qualname__}({self.id!r})>'

    def __str__(self) -> str:
        return self.id

    def __eq__(self, other: Any) -> bool:
        """Two wrapper objects are considered equal if their IDs are equal."""
        if isinstance(other, Widget):
            return self.id == other.id
        return super().__eq__(other)

    ## Overrides

    @abstractmethod
    def _setup_add_widget(self, dpg_args: Mapping[str, Any]) -> None:
        """This should create the widget using DearPyGui's ``add_*()`` functions."""

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

    def set_config(self, **config: Any) -> None:
        dpgcore.configure_item(self.id, **config)

    ## Callbacks

    def set_callback(self, callback: PyGuiCallback) -> None:
        """Set the callback used by DearPyGui."""
        dpgcore.set_item_callback(self.id, wrap_callback(callback))

    def get_callback(self) -> PyGuiCallback:
        """Get the callback used by DearPyGui."""
        dpg_callback = dpgcore.get_item_callback(self.id)
        return unwrap_callback(dpg_callback)

    @property
    def callback_data(self) -> Any:
        """Get or set the callback data."""
        return dpgcore.get_item_callback_data(self.id)

    @callback_data.setter
    def callback_data(self, data: Any) -> None:
        dpgcore.set_item_callback_data(self.id, data)

    def callback(self, _cb: PyGuiCallback = None, *, data: Optional[Any] = None) -> Callable:
        """A decorator that sets the item's callback, and optionally, the callback data.

        For example:

        .. code-block:: python

            with Window('Example Window'):
                button = Button('Callback Button')

                # don't need callback data!
                @button.callback
                def callback(sender):
                    ...

                # if data is a callable, it is invoked each time the callback fires
                # and the result is supplied to the callback.
                @button.callback(data='this could also be a callable')
                def callback(sender, data):
                    ...

        """
        def decorator(callback: PyGuiCallback) -> PyGuiCallback:
            dpgcore.set_item_callback(self.id, wrap_callback(callback), callback_data=data)
            return callback

        if _cb is not None:  # in case people forget the "()"
            return decorator(_cb)
        return decorator

    ## Containers

    def is_container(self) -> bool:
        """Checks if DPG considers this item to be a container."""
        return dpgcore.is_item_container(self.id)

    def iter_children(self) -> Iterable[ItemWidget]:
        """Iterates all of the item's children."""
        children = dpgcore.get_item_children(self.id)
        if not children:
            return
        for child in children:
            yield get_item_by_id(child)

    def add_child(self, child: ItemWidget) -> None:
        """Alternative to :meth:`set_parent`."""
        dpgcore.move_item(child.id, parent=self.id)

    ## Other properties and status

    #: The content of the tooltip that is shown when the widget is hovered.
    #: To remove the tooltip, assign an empty string.
    tooltip: str = ConfigProperty(key='tip')

    enabled: bool = ConfigProperty()  #: If not enabled, display greyed out text and disable interaction.

    @property
    def active(self) -> bool:
        """Get whether the item is being interacted with."""
        return dpgcore.is_item_active(self.id)

    show: bool = ConfigProperty() #: Enable/disable rendering of the item.

    width: int = ConfigProperty()
    height: int = ConfigProperty()

    size: Tuple[float, float]
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


# noinspection PyAbstractClass
class ItemWidget(ABC):
    """Mixin class for all widgets that can belong to containers.

    This mixin class is used to mark :class:`.Widget` subtypes that can belong to a container
    (currently this includes all DPG widgets except for :class:`.Window`).
    It provides its subtypes with methods to move widgets between different containers (re-parent)
    or within their own container.

    Typically when widgets are instantiated they are added to a container based on context.
    This behavior is a result of DPG's container stack and it makes it simple to create
    declarative-style GUIs.

    If you need to add a new widget directly to a specific parent container, or just prefer a more
    OOP-style of specifying a widget's parent, you can use the :meth:`add_to` and :meth:`add_before`
    constructor methods."""

    @property
    @abstractmethod
    def id(self) -> str:
        ...

    @abstractmethod
    def __init__(self, *args, parent: str, **kwargs):
        ...

    def get_parent(self) -> Optional[Widget]:
        """Get this item's parent."""
        parent_id = dpgcore.get_item_parent(self.id)
        if not parent_id:
            return None
        return get_item_by_id(parent_id)

    def set_parent(self, parent: Widget) -> None:
        """Re-parent the item, moving it."""
        dpgcore.move_item(self.id, parent=parent.id)

    def move_up(self) -> None:
        """Move the item up within its parent, if possible."""
        dpgcore.move_item_up(self.id)

    def move_down(self) -> None:
        """Move the item down within its parent, if possible."""
        dpgcore.move_item_down(self.id)

    def move_item_before(self, other: ItemWidget) -> None:
        """Attempt to place the item before another item, re-parenting it if necessary."""
        dpgcore.move_item(self.id, parent=other.get_parent().id, before=other.id)

    @classmethod
    def add_to(cls, parent: Widget, *args: Any, **kwargs: Any) -> Any:
        """Create a widget and add it to the given *parent* instead of using context.

        Returns:
            the newly created widget.
        """
        return cls(*args, parent=parent.id, **kwargs)

    @classmethod
    def insert_before(cls, sibling: ItemWidget, *args: Any, **kwargs: Any) -> Any:
        """Create a widget and insert it before the given *sibling* widget.

        Returns:
            the newly created widget.
        """
        return cls(*args, parent=sibling.get_parent().id, before=sibling.id, **kwargs)


_TValue = TypeVar('_TValue')

class ValueWidget(ABC, Generic[_TValue]):
    """Mixin for all widgets that use the DPG value system.

    The use of the :attr:`value` property depends on the specific kind of widget.

    ValueWidgets can be linked together or to a :class:`.DataValue` by setting the
    :attr:`data_source` config property.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        ...

    @abstractmethod
    def get_config(self) -> ItemConfigData:
        ...

    data_source: DataValue
    @ConfigProperty(key='source')
    def data_source(self) -> DataValue:
        """Get or set the data source.

        When retrieved, a :class:`.DataValue` referencing the data source will be produced.

        If a widget object or a :class:`.DataValue` is assigned as the data source, this widget will
        become linked to the provided source. Otherwise, if ``None`` is assigned, this widget will
        have its own value."""
        source_id = self.get_config().get('source') or self.id
        return DataValue(source_id)

    @data_source.getconfig
    def data_source(self, source: Optional[Any]):
        # accept plain string in addition to GuiData
        return {'source' : str(source) if source is not None else ''}

    value: _TValue
    @property
    def value(self) -> _TValue:
        """Get or set the widget's value."""
        return self._get_value()

    @value.setter
    def value(self, v: _TValue) -> None:
        self._set_value(v)

    # these are here to make it easier for subclasses to override the value property.
    def _get_value(self) -> _TValue:
        return self.data_source.value

    def _set_value(self, v: _TValue) -> None:
        self.data_source.value = v


class DefaultWidget(Widget, ItemWidget):
    """Fallback type used when getting a widget that does not have a wrapper class.

    When :func:`.get_item_by_id` is called to retrieve an item whose widget type does not
    have a wrapper object class associated with it, an instance of this type is created as
    a fallback."""

    def _setup_add_widget(self, dpg_args: Mapping[str, Any]) -> None:
        pass


_set_default_ctor(DefaultWidget)