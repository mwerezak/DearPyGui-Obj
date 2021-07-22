"""Widgets for inputting values."""

from __future__ import annotations

from enum import Enum

from typing import TYPE_CHECKING, TypeVar, Generic, Tuple

from dearpygui import dearpygui as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper.widget import Widget, ItemWidgetMx, ValueWidgetMx, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional

## Input Boxes

@_register_item_type('mvAppItemType::InputText')
class InputText(Widget, ItemWidgetMx, ValueWidgetMx[str]):
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

    def __init__(self, label: str = None, value: str = '', **config):
        super().__init__(label=label, default_value=value, **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_text(self.id, **dpg_args)


## Kind of went overboard with the type checking here...
## probably would have been good enough just to drop annotations for number inputs

## Two type parameters are required because of how DPG multi-inputs work
_TElem = TypeVar('_TElem')
_TInput = TypeVar('_TInput')

# noinspection PyAbstractClass
class NumberInput(Generic[_TElem, _TInput], Widget, ItemWidgetMx, ValueWidgetMx[_TInput]):
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

    def __init__(self, label: str = None, value: _TInput = None, **config):
        value = value or self._default_value
        super().__init__(label=label, default_value=value, **config)


@_register_item_type('mvAppItemType::InputFloat')
class InputFloat(NumberInput[float, float]):
    """A float input box."""
    _default_value = 0.0

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_float(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat2')
class InputFloat2(NumberInput[float, Tuple[float, float]]):
    """An input box for 2 floats."""
    _default_value = (0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_float2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat3')
class InputFloat3(NumberInput[float, Tuple[float, float, float]]):
    """An input box for 3 floats."""
    _default_value = (0.0, 0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_float3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputFloat4')
class InputFloat4(NumberInput[float, Tuple[float, float, float, float]]):
    """An input box for 4 floats."""
    _default_value = (0.0, 0.0, 0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_float4(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt')
class InputInt(NumberInput[int, int]):
    """An integer input box."""
    _default_value = 0

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_int(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt2')
class InputInt2(NumberInput[int, Tuple[int, int]]):
    """An input box for 2 ints."""
    _default_value = (0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_int2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt3')
class InputInt3(NumberInput[int, Tuple[int, int, int]]):
    """An input box for 3 ints."""
    _default_value = (0, 0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_int3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::InputInt4')
class InputInt4(NumberInput[int, Tuple[int, int, int, int]]):
    """An input box for 4 ints."""
    _default_value = (0, 0, 0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_input_int4(self.id, **dpg_args)


## Sliders

# noinspection PyAbstractClass
class SliderInput(Generic[_TElem, _TInput], Widget, ItemWidgetMx, ValueWidgetMx[_TInput]):
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

    def __init__(self, label: str = None, value: _TElem = None, **config):
        value = value or self._default_value
        super().__init__(label=label, default_value=value, **config)

@_register_item_type('mvAppItemType::SliderFloat')
class SliderFloat(SliderInput[float, float]):
    """A slider for a float value.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = 0.0

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_slider_float(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat2')
class SliderFloat2(SliderInput[float, Tuple[float, float]]):
    """A slider for 2 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_slider_float2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat3')
class SliderFloat3(SliderInput[float, Tuple[float, float, float]]):
    """A slider for 3 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_slider_float3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderFloat4')
class SliderFloat4(SliderInput[float, Tuple[float, float, float, float]]):
    """A slider for 4 float values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0, 0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_slider_float4(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt')
class SliderInt(SliderInput[int, int]):
    """A slider for an integer value.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = 0

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_slider_int(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt2')
class SliderInt2(SliderInput[int, Tuple[int, int]]):
    """A slider for 2 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_slider_int2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt3')
class SliderInt3(SliderInput[int, Tuple[int, int, int]]):
    """A slider for 3 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_slider_int3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::SliderInt4')
class SliderInt4(SliderInput[int, Tuple[int, int, int, int]]):
    """A slider for 4 integer values.

    If not disabled using the :attr:`no_input` property, the slider can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0, 0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_slider_int4(self.id, **dpg_args)


## Drag Input Boxes

# noinspection PyAbstractClass
class DragInput(Generic[_TElem, _TInput], Widget, ItemWidgetMx, ValueWidgetMx[_TInput]):
    """Base class for drag input boxes."""
    value: _TInput  #: The inputted value.
    _default_value: _TInput

    label: str = ConfigProperty()
    min_value: _TElem = ConfigProperty()
    max_value: _TElem = ConfigProperty()
    format: str = ConfigProperty()  #: number format

    #: Control whether a value can be manually entered using CTRL+Click
    no_input: bool = ConfigProperty()

    #: Whether to clamp the value when using manual input. By default CTRL+Click allows going out of bounds.
    clamped: bool = ConfigProperty()

    def __init__(self, label: str = None, value: _TElem = None, **config):
        value = value or self._default_value
        super().__init__(label=label, default_value=value, **config)

@_register_item_type('mvAppItemType::DragFloat')
class DragFloat(DragInput[float, float]):
    """A drag input for a float value.

    If not disabled using the :attr:`no_input` property, the drag input can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""

    _default_value = 0.0

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_drag_float(self.id, **dpg_args)

@_register_item_type('mvAppItemType::DragFloat2')
class DragFloat2(DragInput[float, Tuple[float, float]]):
    """A drag input for 2 float values.

    If not disabled using the :attr:`no_input` property, the drag input can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_drag_float2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::DragFloat3')
class DragFloat3(DragInput[float, Tuple[float, float, float]]):
    """A drag input for 3 float values.

    If not disabled using the :attr:`no_input` property, the drag input can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_drag_float3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::DragFloat4')
class DragFloat4(DragInput[float, Tuple[float, float, float, float]]):
    """A drag input for 4 float values.

    If not disabled using the :attr:`no_input` property, the drag input can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0.0, 0.0, 0.0, 0.0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_drag_float4(self.id, **dpg_args)

@_register_item_type('mvAppItemType::DragInt')
class DragInt(DragInput[int, int]):
    """A drag input for an integer value.

    If not disabled using the :attr:`no_input` property, the drag input can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = 0

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_drag_int(self.id, **dpg_args)

@_register_item_type('mvAppItemType::DragInt2')
class DragInt2(DragInput[int, Tuple[int, int]]):
    """A drag input for 2 integer values.

    If not disabled using the :attr:`no_input` property, the drag input can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_drag_int2(self.id, **dpg_args)

@_register_item_type('mvAppItemType::DragInt3')
class DragInt3(DragInput[int, Tuple[int, int, int]]):
    """A drag input for 3 integer values.

    If not disabled using the :attr:`no_input` property, the drag input can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_drag_int3(self.id, **dpg_args)

@_register_item_type('mvAppItemType::DragInt4')
class DragInt4(DragInput[int, Tuple[int, int, int, int]]):
    """A drag input for 4 integer values.

    If not disabled using the :attr:`no_input` property, the drag input can be CTRL+Clicked to turn it
    into an input box for manual input of a value."""
    _default_value = (0, 0, 0, 0)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_drag_int4(self.id, **dpg_args)

## Color
from dearpygui_obj.data import ColorRGBA, ConfigPropertyColorRGBA, import_color_from_dpg, export_color_to_dpg

@_register_item_type('mvAppItemType::ColorButton')
class ColorButton(Widget, ItemWidgetMx):
    """A button that displays and enables copying of color data.

    Clicking and draging the color square will copy the color to be applied on any other color widget.

    While it has color "value", this is not a :class:`.ValueWidgetMx`!
    """
    color: ColorRGBA = ConfigPropertyColorRGBA(no_init=True)  #: The color to copy on drag-and-drop.
    no_border: bool = ConfigProperty()
    no_alpha: bool = ConfigProperty()  #: Don't include alpha channel.
    no_drag_drop: bool = ConfigProperty()

    def __init__(self, color: ColorRGBA = ColorRGBA(1, 0, 1), **config):
        super().__init__(color=export_color_to_dpg(color), **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_color_button(self.id, **dpg_args)

class ColorFormatMode(Enum):
    """Specifies how color element values are formatted."""
    UInt8 = 0  #: Format as 0-255
    Float = 1  #: Format as 0.0-1.0

@_register_item_type('mvAppItemType::ColorEdit4')
class ColorEdit(Widget, ItemWidgetMx, ValueWidgetMx[ColorRGBA]):
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

    def __init__(self, label: str = None, value: ColorRGBA = ColorRGBA(1, 0, 1), **config):
        super().__init__(label=label, default_value=export_color_to_dpg(value), **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_color_edit4(self.id, **dpg_args)

    def __get_value__(self) -> ColorRGBA:
        return import_color_from_dpg(super().__get_value__())

    def __set_value__(self, color: ColorRGBA) -> None:
        super().__set_value__(export_color_to_dpg(color))


@_register_item_type('mvAppItemType::ColorPicker4')
class ColorPicker(Widget, ItemWidgetMx, ValueWidgetMx[ColorRGBA]):
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

    def __init__(self, label: str = None, value: ColorRGBA = ColorRGBA(1, 0, 1), **config):
        super().__init__(label=label, default_value=export_color_to_dpg(value), **config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_color_picker4(self.id, **dpg_args)

    def __get_value__(self) -> ColorRGBA:
        return import_color_from_dpg(super().__get_value__())

    def __set_value__(self, color: ColorRGBA) -> None:
        super().__set_value__(export_color_to_dpg(color))

## Date/Time
from datetime import date, time
from dearpygui_obj.data import import_date_from_dpg, import_time_from_dpg

class DatePickerMode(Enum):
    """The picking mode shown in a :class:`.DatePicker`."""
    Day   = 0
    Month = 1
    Year  = 2

@_register_item_type('mvAppItemType::DatePicker')
class DatePicker(Widget, ItemWidgetMx, ValueWidgetMx[date]):
    """A date picker widget.
    Warning:
        Setting the :attr:`value` property currently does not work. This is an issue with DPG 0.6.
        Attempting to do so will raise a :class:`.NotImplementedError`.
    """

    value: date

    mode: DatePickerMode
    @ConfigProperty(key='level')
    def mode(self) -> DatePickerMode:
        """The current picking mode."""
        config = self.get_config()
        return DatePickerMode(config['level'])

    @mode.getconfig
    def mode(self, level: DatePickerMode):
        return {'level' : level.value}

    def __init__(self, **config):
        super().__init__(**config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_date_picker(self.id, **dpg_args)

    def __get_value__(self) -> date:
        return import_date_from_dpg(super().__get_value__())

    def __set_value__(self, value: date) -> None:
        raise NotImplementedError('not supported in Dear PyGui 0.6')


class TimePickerFormat(Enum):
    """The time format used by :class:`.TimePicker`."""
    Hour12 = False
    Hour24 = True

@_register_item_type('mvAppItemType::TimePicker')
class TimePicker(Widget, ValueWidgetMx[time]):
    """A time picker widget.
    Warning:
        Setting the :attr:`value` property currently does not work. This is an issue with DPG 0.6.
        Attempting to do so will raise a :class:`.NotImplementedError`.
    """

    format: TimePickerFormat
    @ConfigProperty(key='hour24')
    def mode(self) -> TimePickerFormat:
        """The current picking mode."""
        config = self.get_config()
        return TimePickerFormat(config['hour24'])

    @mode.getconfig
    def mode(self, format: TimePickerFormat):
        return {'hour24' : format.value}

    def __init__(self, **config):
        super().__init__(**config)

    def __setup_add_widget__(self, dpg_args) -> None:
        dpgcore.add_time_picker(self.id, **dpg_args)

    def __get_value__(self) -> time:
        return import_time_from_dpg(super().__get_value__())

    def __set_value__(self, value: time) -> None:
        raise NotImplementedError('not supported in Dear PyGui 0.6')


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

    'DragFloat',
    'DragFloat2',
    'DragFloat3',
    'DragFloat4',
    'DragInt',
    'DragInt2',
    'DragInt3',
    'DragInt4',

    'ColorButton',
    'ColorFormatMode',
    'ColorEdit',
    'ColorPicker',

    'DatePickerMode',
    'DatePicker',
]