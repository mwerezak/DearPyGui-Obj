from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import GuiData
from dearpygui_obj.wrapper import PyGuiBase, dearpygui_wrapper, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional


@dearpygui_wrapper('mvAppItemType::InputText')
class InputText(PyGuiBase):
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

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_text(self.id, **config)


@dearpygui_wrapper('mvAppItemType::InputFloat')
class InputFloat(PyGuiBase):
    """A float input box."""

    format: str = ConfigProperty()
    on_enter: bool = ConfigProperty()
    step: float = ConfigProperty()
    step_fast: float = ConfigProperty()
    readonly: bool = ConfigProperty()
    label: str = ConfigProperty()

    @ConfigProperty
    def min_value(self, config) -> Optional[float]:
        if not config.get('min_clamped'):
            return None
        return config['min_value']

    @min_value.getconfig
    def min_value(self, value: Optional[float]):
        if value is None:
            return {'min_clamped': False}
        return {'min_clamped': True, 'min_value': value}

    @ConfigProperty
    def max_value(self, config) -> Optional[float]:
        if not config.get('max_clamped'):
            return None
        return config['max_value']

    @max_value.getconfig
    def max_value(self, value: Optional[float]):
        if value is None:
            return {'max_clamped': False}
        return {'max_clamped': True, 'max_value': value}

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_float(self.id, **config)

@dearpygui_wrapper('mvAppItemType::InputFloat2')
class InputFloat2(InputFloat):
    """An input box for 2 floats."""
    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_float2(self.id, **config)

@dearpygui_wrapper('mvAppItemType::InputFloat3')
class InputFloat3(InputFloat):
    """An input box for 3 floats."""
    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_float3(self.id, **config)

@dearpygui_wrapper('mvAppItemType::InputFloat4')
class InputFloat4(InputFloat):
    """An input box for 4 floats."""
    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_float4(self.id, **config)


@dearpygui_wrapper('mvAppItemType::InputInt')
class InputInt(PyGuiBase):
    """An integer input box."""
    format: str = ConfigProperty()
    on_enter: bool = ConfigProperty()
    step: int = ConfigProperty()
    step_fast: int = ConfigProperty()
    readonly: bool = ConfigProperty()
    label: str = ConfigProperty()

    @ConfigProperty
    def min_value(self, config) -> Optional[int]:
        if not config.get('min_clamped'):
            return None
        return config['min_value']

    @min_value.getconfig
    def min_value(self, value: Optional[float]):
        if value is None:
            return {'min_clamped': False}
        return {'min_clamped': True, 'min_value': value}

    @ConfigProperty
    def max_value(self, config) -> Optional[int]:
        if not config.get('max_clamped'):
            return None
        return config['max_value']

    @max_value.getconfig
    def max_value(self, value: Optional[float]):
        if value is None:
            return {'max_clamped': False}
        return {'max_clamped': True, 'max_value': value}

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_int(self.id, **config)

@dearpygui_wrapper('mvAppItemType::InputInt2')
class InputInt2(InputInt):
    """An input box for 2 ints."""
    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_int2(self.id, **config)

@dearpygui_wrapper('mvAppItemType::InputInt3')
class InputInt3(InputInt):
    """An input box for 3 ints."""
    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_int3(self.id, **config)

@dearpygui_wrapper('mvAppItemType::InputInt4')
class InputInt4(InputInt):
    """An input box for 4 ints."""
    def _setup_add_widget(self, config) -> None:
        dpgcore.add_input_int4(self.id, **config)


if __name__ == '__main__':
    from dearpygui.core import *
    from dearpygui_obj.window import Window

    linked_ints = GuiData([0, 3, -1, 2])

    with Window('Test Window') as window:
        t = InputText('InputText')
        t2 = InputText('Deleted')
        f = InputFloat('InputFloat', default_value=4.3)
        f2 = InputFloat2('InputFloat2', tip='tooltip')
        i = InputInt('InputInt', data_source = linked_ints)
        i2 = InputInt2('InputInt2', data_source = linked_ints)
        i4 = InputInt4('InputInt4', data_source = linked_ints)

    get_item_type(f2.id)
    print(f2.tip)

    t2.delete()
    print(t2.is_valid)

    start_dearpygui()