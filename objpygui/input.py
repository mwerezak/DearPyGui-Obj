from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from objpygui import (
    ItemWrapper, config_property, register_item_type
)

if TYPE_CHECKING:
    from typing import Optional, Any


@register_item_type('mvAppItemType::InputText')
class InputText(ItemWrapper):
    hint: str = config_property()
    multiline: bool = config_property()
    no_spaces: bool = config_property()
    uppercase: bool = config_property()
    tab_input: bool = config_property()
    decimal: bool = config_property()
    hexadecimal: bool = config_property()
    readonly: bool = config_property()
    password: bool = config_property()
    scientific: bool = config_property()
    label: str = config_property()
    on_enter: bool = config_property()

    def _setup_add_item(self, config) -> None:
        gui_core.add_input_text(self.id, **config)


@register_item_type('mvAppItemType::InputFloat')
class InputFloat(ItemWrapper):
    format: str = config_property()
    on_enter: bool = config_property()
    step: float = config_property()
    step_fast: float = config_property()
    readonly: bool = config_property()

    @config_property
    def min_value(config) -> Optional[float]:
        if not config.get('min_clamped'):
            return None
        return config['min_value']

    @min_value.getconfig
    def min_value(value: Optional[float]):
        if value is None:
            return {'min_clamped': False}
        return {'min_clamped': True, 'min_value': value}

    @config_property
    def max_value(config) -> Optional[float]:
        if not config.get('max_clamped'):
            return None
        return config['max_value']

    @max_value.getconfig
    def max_value(value: Optional[float]):
        if value is None:
            return {'max_clamped': False}
        return {'max_clamped': True, 'max_value': value}

    def _setup_add_item(self, config) -> None:
        gui_core.add_input_float(self.id, **config)

@register_item_type('mvAppItemType::InputFloat2')
class InputFloat2(InputFloat):
    def _setup_add_item(self, config) -> None:
        gui_core.add_input_float2(self.id, **config)

@register_item_type('mvAppItemType::InputFloat3')
class InputFloat3(InputFloat):
    def _setup_add_item(self, config) -> None:
        gui_core.add_input_float3(self.id, **config)

@register_item_type('mvAppItemType::InputFloat4')
class InputFloat4(InputFloat):
    def _setup_add_item(self, config) -> None:
        gui_core.add_input_float4(self.id, **config)


@register_item_type('mvAppItemType::InputInt')
class InputInt(ItemWrapper):
    format: str = config_property()
    on_enter: bool = config_property()
    step: float = config_property()
    step_fast: float = config_property()
    readonly: bool = config_property()

    @config_property
    def min_value(config) -> Optional[int]:
        if not config.get('min_clamped'):
            return None
        return config['min_value']

    @min_value.getconfig
    def min_value(value: Optional[float]):
        if value is None:
            return {'min_clamped': False}
        return {'min_clamped': True, 'min_value': value}

    @config_property
    def max_value(config) -> Optional[int]:
        if not config.get('max_clamped'):
            return None
        return config['max_value']

    @max_value.getconfig
    def max_value(value: Optional[float]):
        if value is None:
            return {'max_clamped': False}
        return {'max_clamped': True, 'max_value': value}

    def _setup_add_item(self, config) -> None:
        gui_core.add_input_int(self.id, **config)

@register_item_type('mvAppItemType::InputInt2')
class InputInt2(InputInt):
    def _setup_add_item(self, config) -> None:
        gui_core.add_input_int2(self.id, **config)

@register_item_type('mvAppItemType::InputInt3')
class InputInt3(InputInt):
    def _setup_add_item(self, config) -> None:
        gui_core.add_input_int3(self.id, **config)

@register_item_type('mvAppItemType::InputInt4')
class InputInt4(InputInt):
    def _setup_add_item(self, config) -> None:
        gui_core.add_input_int4(self.id, **config)


if __name__ == '__main__':
    from dearpygui.core import *
    from objpygui import GuiData
    from objpygui.window import Window

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