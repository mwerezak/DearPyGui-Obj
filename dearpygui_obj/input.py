"""Widgets for inputting values."""

from __future__ import annotations

from enum import Enum
from abc import ABC
from typing import TYPE_CHECKING, TypeVar, Generic

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.data import ColorRGBA
from dearpygui_obj.wrapper import PyGuiWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional, Tuple

## Input Boxes

@_register_item_type('mvAppItemType::InputText')
class InputText(PyGuiWidget):
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

    def __init__(self, label: str = None, value: str = '', *, name_id: str = None, **config):
        super().__init__(label=label, default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_text(self.id, **dpg_args)

_TInput = TypeVar('_TInput')

class NumberInput(PyGuiWidget, Generic[_TInput]):
    """Base class for number input boxes."""
    value: _TInput
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

    def __init__(self, label: str = None, value: _TInput = None, *, name_id: str = None, **config):
        value = value or self._default_value
        super().__init__(label=label, default_value=value, name_id=name_id, **config)


_TElem = TypeVar('_TElem')

@_register_item_type('mvAppItemType::InputFloat')
class InputFloat(NumberInput[float]):
    """A float input box."""
    _default_value = 0.0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat2')
class InputFloat2(NumberInput[float]):
    """An input box for 2 floats."""
    value: Tuple[float, float]
    _default_value = (0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat3')
class InputFloat3(NumberInput[float]):
    """An input box for 3 floats."""
    value: Tuple[float, float, float]
    _default_value = (0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat4')
class InputFloat4(NumberInput[float]):
    """An input box for 4 floats."""
    value: Tuple[float, float, float, float]
    _default_value = (0.0, 0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float4(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt')
class InputInt(NumberInput[int]):
    """An integer input box."""
    _default_value = 0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt2')
class InputInt2(NumberInput[int]):
    """An input box for 2 ints."""
    value: Tuple[int, int]
    _default_value = (0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt3')
class InputInt3(NumberInput[int]):
    """An input box for 3 ints."""
    value: Tuple[int, int, int]
    _default_value = (0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt4')
class InputInt4(NumberInput[int]):
    """An input box for 4 ints."""
    value: Tuple[int, int, int, int]
    _default_value = (0, 0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int4(self.id, **dpg_args)


## Sliders

class SliderInput(PyGuiWidget, Generic[_TInput]):
    """Base class for slider types."""
    value: _TInput
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

    def __init__(self, label: str = None, value: _TInput = None, *, name_id: str = None, **config):
        value = value or self._default_value
        super().__init__(label=label, default_value=value, name_id=name_id, **config)

@_register_item_type('mvAppItemType::SliderFloat')
class SliderFloat(SliderInput[float]):
    """A slider for a float value.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = 0.0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat2')
class SliderFloat2(SliderInput[float]):
    """A slider for 2 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    value: Tuple[float, float]
    _default_value = (0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat3')
class SliderFloat3(SliderInput[float]):
    """A slider for 3 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    value: Tuple[float, float, float]
    _default_value = (0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat4')
class SliderFloat4(SliderInput[float]):
    """A slider for 4 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    value: Tuple[float, float, float, float]
    _default_value = (0.0, 0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float4(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt')
class SliderInt(SliderInput[int]):
    """A slider for an integer value.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    value: int
    _default_value = 0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt2')
class SliderInt2(SliderInput[int]):
    """A slider for 2 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    value: Tuple[int, int]
    _default_value = (0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt3')
class SliderInt3(SliderInput[int]):
    """A slider for 3 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    value: Tuple[int, int, int]
    _default_value = (0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt4')
class SliderInt4(SliderInput[int]):
    """A slider for 4 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    value: Tuple[int, int, int, int]
    _default_value = (0, 0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int4(self.id, **dpg_args)


## Color

@_register_item_type('mvAppItemType::ColorButton')
class ColorButton(PyGuiWidget):
    """A button that displays and enables copying of color data.

    Clicking and draging the color square will copy the color to be applied on any other color widget."""

    no_border: bool = ConfigProperty()
    no_alpha: bool = ConfigProperty()  #: Don't include alpha channel.
    no_drag_drop: bool = ConfigProperty()

    def __init__(self, color: ColorRGBA = ColorRGBA(1, 0, 1), *, name_id: str = None, **config):
        super().__init__(color=color.dpg_export(), name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_color_button(self.id, **dpg_args)


class ColorFormatMode(Enum):
    """Specifies how color element values are formatted."""
    UInt8 = 0  #: Format as 0-255
    Float = 1  #: Format as 0.0-1.0

@_register_item_type('mvAppItemType::ColorEdit4')
class ColorEdit(PyGuiWidget):
    """A color editing widget.

    Clicking and draging the color square will copy the color to be applied on any other color widget."""

    label: str = ConfigProperty()
    no_alpha: bool = ConfigProperty()  #: Don't include alpha channel.
    no_picker: bool = ConfigProperty()
    no_options: bool = ConfigProperty()
    no_small_preview: bool = ConfigProperty()
    no_inputs: bool = ConfigProperty()
    no_tooltip: bool = ConfigProperty()
    no_label: bool = ConfigProperty()
    no_drag_drop: bool = ConfigProperty()
    alpha_bar: bool = ConfigProperty()
    alpha_preview: bool = ConfigProperty()
    alpha_preview_half: bool = ConfigProperty()
    display_rgb: bool = ConfigProperty()
    display_hsv: bool = ConfigProperty()
    display_hex: bool = ConfigProperty()
    input_rgb: bool = ConfigProperty()
    input_hsv: bool = ConfigProperty()

    @ConfigProperty()
    def color_format(self) -> ColorFormatMode:
        config = self.get_config()
        if config['floats'] and not config['uint8']:
            return ColorFormatMode.Float
        return ColorFormatMode.UInt8

    @color_format.getconfig
    def color_format(self, value: ColorFormatMode):
        if value == ColorFormatMode.UInt8:
            return {'uint8':False, 'floats':True}
        if value == ColorFormatMode.Float:
            return {'uint8':True, 'floats':False}
        raise ValueError('invalid color format mode')

    def __init__(self, label: str = None, value: ColorRGBA = ColorRGBA(1, 0, 1), *, name_id: str = None, **config):
        super().__init__(label=label, default_value=value.dpg_export(), name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_color_edit4(self.id, **dpg_args)


@_register_item_type('mvAppItemType::ColorPicker4')
class ColorPicker(PyGuiWidget):
    """A color picking widget.

    Clicking and draging the color square will copy the color to be applied on any other color widget.
    Right-click allows the style of the color picker to be changed."""

    label: str = ConfigProperty()
    no_alpha: bool = ConfigProperty()
    no_small_preview: bool = ConfigProperty()
    no_inputs: bool = ConfigProperty()
    no_tooltip: bool = ConfigProperty()
    no_label: bool = ConfigProperty()
    no_side_preview: bool = ConfigProperty()
    alpha_bar: bool = ConfigProperty()
    alpha_preview: bool = ConfigProperty()
    alpha_preview_half: bool = ConfigProperty()
    display_rgb: bool = ConfigProperty()
    display_hsv: bool = ConfigProperty()
    display_hex: bool = ConfigProperty()
    picker_hue_bar: bool = ConfigProperty()
    picker_hue_wheel: bool = ConfigProperty()
    input_rgb: bool = ConfigProperty()
    input_hsv: bool = ConfigProperty()

    @ConfigProperty()
    def color_format(self) -> ColorFormatMode:
        config = self.get_config()
        if config['floats'] and not config['uint8']:
            return ColorFormatMode.Float
        return ColorFormatMode.UInt8

    @color_format.getconfig
    def color_format(self, value: ColorFormatMode):
        if value == ColorFormatMode.UInt8:
            return {'uint8':False, 'floats':True}
        if value == ColorFormatMode.Float:
            return {'uint8':True, 'floats':False}
        raise ValueError('invalid color format mode')

    def __init__(self, label: str = None, value: ColorRGBA = ColorRGBA(1, 0, 1), *, name_id: str = None, **config):
        super().__init__(label=label, default_value=value.dpg_export(), name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_color_picker4(self.id, **dpg_args)

