from __future__ import annotations

from abc import ABC, abstractmethod
from collections import ChainMap as chain_map
from typing import TYPE_CHECKING, Optional, Type, ChainMap

from dearpygui import core as dpgcore

from dearpygui_obj import _generate_id

if TYPE_CHECKING:
    from typing import Any, Callable, Mapping
    from dearpygui_obj.drawing import DrawingCanvas

    DrawConfigData = Mapping[str, Any]
    GetDrawValueFunc = Callable[['DrawCommand'], Any]
    GetDrawConfigFunc = Callable[['DrawCommand', Any], DrawConfigData]


class DrawProperty:
    """Descriptor used to get or set a draw command's configuration."""

    def __init__(self,
                 key: Optional[str] = None, *,
                 doc: str = ''):
        """
        Parameters:
            key: the config key to get/set with the default implementation.
            doc: custom docstring.
        """
        self.owner = None
        self.key = key
        self.__doc__ = doc

    def __set_name__(self, owner: Type[DrawCommand], name: str):
        self.owner = owner
        self.name = name

        owner.add_draw_property(self)

        if self.key is None:
            self.key = name

        if not self.__doc__:
            self.__doc__ = f"Read or modify the '{self.key}' config field."

    def __get__(self, instance: Optional[DrawCommand], owner: Type[DrawCommand]) -> Any:
        if instance is None:
            return self
        return self.get_value(instance)

    def __set__(self, instance: DrawCommand, value: Any) -> None:
        config = self.get_config(instance, value)
        dpgcore.modify_draw_command(instance.canvas.id, instance.id, **config)

    def __call__(self, get_value: GetDrawValueFunc):
        """Allows the ConfigProperty itself to be used as a decorator equivalent to :attr:`getvalue`."""
        return self.getvalue(get_value)

    def getvalue(self, get_value: GetDrawValueFunc):
        self.get_value = get_value
        self.__doc__ = get_value.__doc__ # use the docstring of the getter, the same way property() works
        return self

    def getconfig(self, get_config: GetDrawConfigFunc):
        self.get_config = get_config
        return self

    ## default implementations
    get_value: GetDrawValueFunc
    get_config: GetDrawConfigFunc

    def get_value(self, instance: DrawCommand) -> Any:
        return dpgcore.get_draw_command(instance.canvas.id, instance.id)[self.key]

    def get_config(self, instance: DrawCommand, value: Any) -> DrawConfigData:
        return {self.key : value}


class DrawCommand(ABC):
    """Base class for drawing commands."""

    # subclasses can prevent inheritance of this by overriding it's value with a new mapping.
    _draw_properties: ChainMap[str, DrawProperty] = chain_map()

    @classmethod
    def add_draw_property(cls, prop: DrawProperty) -> None:
        draw_properties = cls.__dict__.get('_draw_properties')
        if draw_properties is None:
            # inherit keyword params from parent
            if hasattr(cls._draw_properties, 'new_child'):
                draw_properties = cls._draw_properties.new_child({})
            else:
                draw_properties = chain_map({}, cls._draw_properties)
            setattr(cls, '_draw_properties', draw_properties)
        draw_properties[prop.name] = prop

    def __init__(self, canvas: DrawingCanvas, *args, tag_id: str = None, **kwargs: Any):
        self._canvas = canvas
        if tag_id is not None:
            self._tag_id = tag_id
        else:
            self._tag_id = _generate_id(self)

        draw_data = {}
        for prop, value in zip(self._draw_properties.values(), args):
            draw_data.update(prop.get_config(self, value))

        for name, value in kwargs.items():
            prop = self._draw_properties.get(name)
            if prop is not None:
                draw_data.update(prop.get_config(self, value))

        self._draw_internal(draw_data)

    @abstractmethod
    def _draw_internal(self, draw_args: Mapping[str, Any]) -> None:
        """This should execute the draw using DearPyGui's ``draw_*()`` functions."""

    @property
    def id(self) -> str:
        return self._tag_id

    @property
    def canvas(self) -> DrawingCanvas:
        return self._canvas

    def delete(self) -> None:
        dpgcore.delete_draw_command(self.canvas.id, self.id)

    def get_config(self) -> DrawConfigData:
        return dpgcore.get_draw_command(self.canvas.id, self.id)

    def set_config(self, **config: Any) -> None:
        dpgcore.modify_draw_command(self.canvas.id, self.id, **config)

    def bring_to_front(self) -> None:
        dpgcore.bring_draw_command_to_front(self.canvas.id, self.id)

    def send_to_back(self) -> None:
        dpgcore.send_draw_command_to_back(self.canvas.id, self.id)

    def move_forward(self) -> None:
        dpgcore.bring_draw_command_forward(self.canvas.id, self.id)

    def move_back(self) -> None:
        dpgcore.send_draw_command_back(self.canvas.id, self.id)