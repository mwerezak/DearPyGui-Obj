"""Widgets for inputting values."""

from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Generic, Sequence, Tuple

import dearpygui.core as dpgcore
from dearpygui_obj import GuiData
from dearpygui_obj.wrapper import PyGuiObject, dearpygui_wrapper, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional

## Input Boxes

@dearpygui_wrapper('mvAppItemType::InputText')
class InputText(PyGuiObject):
    """A text input box."""

    hint: str = ConfigProperty()
    multiline: bool = ConfigProperty()
    no_spaces: bool = ConfigProperty()
    uppercase: bool = ConfigProperty()
    tab_input: bool = ConfigProperty()
    decimal: bool = ConfigProperty()
    hexadecimal: bool = ConfigProperty()
    readonly: bool = ConfigProperty()
    password: bool = ConfigProperty()
    scientific: bool = ConfigProperty()
    label: str = ConfigProperty()
    on_enter: bool = ConfigProperty()

    def __init__(self, label: str, default_value: str = '', *, name_id: str = None, **config):
        super().__init__(label=label, default_value=default_value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_text(self.id, **dpg_args)

_TInput = TypeVar('_TInput')

class NumberInput(PyGuiObject, Generic[_TInput]):
    """Base class for number input boxes."""
    _default_value: _TInput

    format: str = ConfigProperty()
    on_enter: bool = ConfigProperty()
    step: _TInput = ConfigProperty()
    step_fast: _TInput = ConfigProperty()
    readonly: bool = ConfigProperty()
    label: str = ConfigProperty()

    @ConfigProperty()
    def min_value(self) -> Optional[_TInput]:
        config = self.get_config()
        if not config.get('min_clamped'):
            return None
        return config['min_value']

    @min_value.getconfig
    def min_value(self, value: Optional[_TInput]):
        if value is None:
            return {'min_clamped': False}
        return {'min_clamped': True, 'min_value': value}

    @ConfigProperty()
    def max_value(self) -> Optional[_TInput]:
        config = self.get_config()
        if not config.get('max_clamped'):
            return None
        return config['max_value']

    @max_value.getconfig
    def max_value(self, value: Optional[_TInput]):
        if value is None:
            return {'max_clamped': False}
        return {'max_clamped': True, 'max_value': value}

    def __init__(self, label: str, default_value: _TInput = None, *, name_id: str = None, **config):
        default_value = default_value or self._default_value
        if isinstance(default_value, Sequence):
            default_value = list(default_value)
        super().__init__(label=label, default_value=default_value, name_id=name_id, **config)

@dearpygui_wrapper('mvAppItemType::InputFloat')
class InputFloat(NumberInput[float]):
    """A float input box."""

    _default_value = 0.0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::InputFloat2')
class InputFloat2(NumberInput[Tuple[float, float]]):
    """An input box for 2 floats."""

    _default_value = (0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float2(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::InputFloat3')
class InputFloat3(NumberInput[Tuple[float, float, float]]):
    """An input box for 3 floats."""

    _default_value = (0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float3(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::InputFloat4')
class InputFloat4(NumberInput[Tuple[float, float, float, float]]):
    """An input box for 4 floats."""

    _default_value = (0.0, 0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float4(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::InputInt')
class InputInt(NumberInput[int]):
    """An integer input box."""

    _default_value = 0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::InputInt2')
class InputInt2(NumberInput[Tuple[int, int]]):
    """An input box for 2 ints."""

    _default_value = (0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int2(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::InputInt3')
class InputInt3(NumberInput[Tuple[int, int, int]]):
    """An input box for 3 ints."""

    _default_value = (0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int3(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::InputInt4')
class InputInt4(NumberInput[Tuple[int, int, int, int]]):
    """An input box for 4 ints."""

    _default_value = (0, 0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int4(self.id, **dpg_args)


## Sliders

class SliderInput(PyGuiObject, Generic[_TInput]):
    """Base class for slider types."""
    _default_value: _TInput

    label: str = ConfigProperty()
    min_value: _TInput = ConfigProperty()
    max_value: _TInput = ConfigProperty()
    format: str = ConfigProperty()
    vertical: bool = ConfigProperty()

    #: Control whether a value can be manually entered using CTRL+Click
    no_input: bool = ConfigProperty()

    #: Whether to clamp the value when using manual input. By default CTRL+Click allows going out of bounds.
    clamped: bool = ConfigProperty()

    def __init__(self, label: str, default_value: _TInput = None, *, name_id: str = None, **config):
        default_value = default_value or self._default_value
        if isinstance(default_value, Sequence):
            default_value = list(default_value)
        super().__init__(label=label, default_value=default_value, name_id=name_id, **config)

@dearpygui_wrapper('mvAppItemType::SliderFloat')
class SliderFloat(SliderInput[float]):
    """A slider for a float value.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = 0.0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::SliderFloat2')
class SliderFloat2(SliderInput[Tuple[float, float]]):
    """A slider for 2 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = (0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float2(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::SliderFloat3')
class SliderFloat3(SliderInput[Tuple[float, float, float]]):
    """A slider for 3 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = (0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float3(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::SliderFloat4')
class SliderFloat4(SliderInput[Tuple[float, float, float, float]]):
    """A slider for 4 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = (0.0, 0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float4(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::SliderInt')
class SliderInt(SliderInput[int]):
    """A slider for an integer value.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = 0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::SliderInt2')
class SliderInt2(SliderInput[Tuple[int, int]]):
    """A slider for 2 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = (0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int2(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::SliderInt3')
class SliderInt3(SliderInput[Tuple[int, int, int]]):
    """A slider for 3 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = (0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int3(self.id, **dpg_args)

@dearpygui_wrapper('mvAppItemType::SliderInt4')
class SliderInt4(SliderInput[Tuple[int, int, int, int]]):
    """A slider for 4 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = (0, 0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int4(self.id, **dpg_args)



if __name__ == '__main__':
    from dearpygui.core import *
    from dearpygui_obj.window import Window

    linked_ints = GuiData([0, 3, -1, 2])

    with Window('Test Window') as window:
        t = InputText('InputText')
        t2 = InputText('Deleted')
        f = InputFloat('InputFloat', default_value=4.3)
        f2 = InputFloat2('InputFloat2', tooltip='tooltip')
        i = InputInt('InputInt', data_source = linked_ints)
        i2 = InputInt2('InputInt2', data_source = linked_ints)
        i4 = InputInt4('InputInt4', data_source = linked_ints)
        sf = SliderFloat('SliderFloat')
        sf3 = SliderFloat3('SliderFloat3')
        print(get_item_type(sf.id))
        print(get_item_configuration(sf.id))


    start_dearpygui()