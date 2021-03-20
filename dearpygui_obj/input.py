"""Widgets for inputting values."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, TypeVar, Generic, Tuple

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.data import ColorRGBA, ConfigPropertyColorRGBA, dpg_import_color, dpg_export_color
from dearpygui_obj.wrapper.widget import Widget, ItemWidget, ValueWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional

## Input Boxes

@_register_item_type('mvAppItemType::InputText')
class InputText(Widget, ItemWidget, ValueWidget[str]):
    """A text input box."""

    value: str  #: The inputted text.

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


## Kind of went overboard with the type checking here...
## probably would have been good enough just to drop annotations for number inputs

## Two type parameters are required because of how DPG multi-inputs work
_TElem = TypeVar('_TElem')
_TInput = TypeVar('_TInput')

# noinspection PyAbstractClass
class NumberInput(Widget, ItemWidget, ValueWidget[_TInput], Generic[_TElem, _TInput]):
    """Base class for number input boxes."""
    value: _TInput  #: The inputted value.
    _default_value: _TInput

    format: str = ConfigProperty()
    on_enter: bool = ConfigProperty()
    step: _TElem = ConfigProperty()
    step_fast: _TElem = ConfigProperty()
    readonly: bool = ConfigProperty()
    label: str = ConfigProperty()

    min_value: Optional[_TElem]
    @ConfigProperty()
    def min_value(self) -> Optional[_TElem]:
        config = self.get_config()
        if not config.get('min_clamped'):
            return None
        return config['min_value']

    @min_value.getconfig
    def min_value(self, value: Optional[_TElem]):
        if value is None:
            return {'min_clamped': False}
        return {'min_clamped': True, 'min_value': value}

    max_value: Optional[_TElem]
    @ConfigProperty()
    def max_value(self) -> Optional[_TElem]:
        config = self.get_config()
        if not config.get('max_clamped'):
            return None
        return config['max_value']

    @max_value.getconfig
    def max_value(self, value: Optional[_TElem]):
        if value is None:
            return {'max_clamped': False}
        return {'max_clamped': True, 'max_value': value}

    def __init__(self, label: str = None, value: _TInput = None, *, name_id: str = None, **config):
        value = value or self._default_value
        super().__init__(label=label, default_value=value, name_id=name_id, **config)


@_register_item_type('mvAppItemType::InputFloat')
class InputFloat(NumberInput[float, float]):
    """A float input box."""
    _default_value = 0.0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat2')
class InputFloat2(NumberInput[float, Tuple[float, float]]):
    """An input box for 2 floats."""
    _default_value = (0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat3')
class InputFloat3(NumberInput[float, Tuple[float, float, float]]):
    """An input box for 3 floats."""
    _default_value = (0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat4')
class InputFloat4(NumberInput[float, Tuple[float, float, float, float]]):
    """An input box for 4 floats."""
    _default_value = (0.0, 0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_float4(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt')
class InputInt(NumberInput[int, int]):
    """An integer input box."""
    _default_value = 0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt2')
class InputInt2(NumberInput[int, Tuple[int, int]]):
    """An input box for 2 ints."""
    _default_value = (0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt3')
class InputInt3(NumberInput[int, Tuple[int, int, int]]):
    """An input box for 3 ints."""
    _default_value = (0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt4')
class InputInt4(NumberInput[int, Tuple[int, int, int, int]]):
    """An input box for 4 ints."""
    _default_value = (0, 0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_input_int4(self.id, **dpg_args)


## Sliders

# noinspection PyAbstractClass
class SliderInput(Widget, ItemWidget, ValueWidget[_TInput], Generic[_TElem, _TInput]):
    """Base class for slider types."""
    value: _TInput  #: The inputted value.
    _default_value: _TInput

    label: str = ConfigProperty()
    min_value: _TElem = ConfigProperty()
    max_value: _TElem = ConfigProperty()
    format: str = ConfigProperty()  #: number format
    vertical: bool = ConfigProperty()

    #: Control whether a value can be manually entered using CTRL+Click
    no_input: bool = ConfigProperty()

    #: Whether to clamp the value when using manual input. By default CTRL+Click allows going out of bounds.
    clamped: bool = ConfigProperty()

    def __init__(self, label: str = None, value: _TElem = None, *, name_id: str = None, **config):
        value = value or self._default_value
        super().__init__(label=label, default_value=value, name_id=name_id, **config)

@_register_item_type('mvAppItemType::SliderFloat')
class SliderFloat(SliderInput[float, float]):
    """A slider for a float value.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = 0.0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat2')
class SliderFloat2(SliderInput[float, Tuple[float, float]]):
    """A slider for 2 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat3')
class SliderFloat3(SliderInput[float, Tuple[float, float, float]]):
    """A slider for 3 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat4')
class SliderFloat4(SliderInput[float, Tuple[float, float, float, float]]):
    """A slider for 4 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0, 0.0, 0.0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_float4(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt')
class SliderInt(SliderInput[int, int]):
    """A slider for an integer value.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = 0

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt2')
class SliderInt2(SliderInput[int, Tuple[int, int]]):
    """A slider for 2 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt3')
class SliderInt3(SliderInput[int, Tuple[int, int, int]]):
    """A slider for 3 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt4')
class SliderInt4(SliderInput[int, Tuple[int, int, int, int]]):
    """A slider for 4 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0, 0, 0)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_slider_int4(self.id, **dpg_args)


## Color

@_register_item_type('mvAppItemType::ColorButton')
class ColorButton(Widget, ItemWidget):
    """A button that displays and enables copying of color data.

    Clicking and draging the color square will copy the color to be applied on any other color widget.

    While it has color "value", this is not a :class:`.ValueWidget`!
    """
    color: ColorRGBA = ConfigPropertyColorRGBA(no_init=True)  #: The color to copy on drag-and-drop.
    no_border: bool = ConfigProperty()
    no_alpha: bool = ConfigProperty()  #: Don't include alpha channel.
    no_drag_drop: bool = ConfigProperty()

    def __init__(self, color: ColorRGBA = ColorRGBA(1, 0, 1), *, name_id: str = None, **config):
        super().__init__(color=dpg_export_color(color), name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_color_button(self.id, **dpg_args)

class ColorFormatMode(Enum):
    """Specifies how color element values are formatted."""
    UInt8 = 0  #: Format as 0-255
    Float = 1  #: Format as 0.0-1.0

@_register_item_type('mvAppItemType::ColorEdit4')
class ColorEdit(Widget, ItemWidget, ValueWidget[ColorRGBA]):
    """A color editing widget.

    Clicking and draging the color square will copy the color to be applied on any other color widget."""

    value: ColorRGBA  #: The inputted color.

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

    color_format: ColorFormatMode
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
        super().__init__(label=label, default_value=dpg_export_color(value), name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_color_edit4(self.id, **dpg_args)

    def _get_value(self) -> ColorRGBA:
        return dpg_import_color(super()._get_value())

    def _set_value(self, color: ColorRGBA) -> None:
        super()._set_value(dpg_export_color(color))


@_register_item_type('mvAppItemType::ColorPicker4')
class ColorPicker(Widget, ItemWidget, ValueWidget[ColorRGBA]):
    """A color picking widget.

    Clicking and draging the color square will copy the color to be applied on any other color widget.
    Right-click allows the style of the color picker to be changed."""

    value: ColorRGBA  #: The picked color.

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

    color_format: ColorFormatMode
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
        super().__init__(label=label, default_value=dpg_export_color(value), name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_color_picker4(self.id, **dpg_args)

    def _get_value(self) -> ColorRGBA:
        return dpg_import_color(super()._get_value())

    def _set_value(self, color: ColorRGBA) -> None:
        super()._set_value(dpg_export_color(color))



__all__ = [
    'InputText',
    'InputFloat',
    'InputFloat2',
    'InputFloat3',
    'InputFloat4',
    'InputInt',
    'InputInt2',
    'InputInt3',
    'InputInt4',
    'SliderFloat',
    'SliderFloat2',
    'SliderFloat3',
    'SliderFloat4',
    'SliderInt',
    'SliderInt2',
    'SliderInt3',
    'SliderInt4',
    'ColorButton',
    'ColorFormatMode',
    'ColorEdit',
    'ColorPicker',
]