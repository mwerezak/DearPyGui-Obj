from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from objpygui.core import (
    GuiItem, ConfigProperty, register_item_type
)

if TYPE_CHECKING:
    from typing import Optional, Any, Tuple


@register_item_type('mvAppItemType::InputText')
class InputText(GuiItem):
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

    def _setup_add_item(self, config) -> None:
        gui_core.add_input_text(self.id, **config)


def _min_clamped_value(config):
    if not config.get('min_clamped'):
        return None
    return config['min_value']

def _min_clamped_config(value: Optional[float]):
    if value is None:
        return {'min_clamped' : False}
    return {'min_clamped' : True, 'min_value' : value}

def _max_clamped_value(config):
    if not config.get('max_clamped'):
        return None
    return config['max_value']

def _max_clamped_config(value: Optional[float]):
    if value is None:
        return {'max_clamped' : False}
    return {'max_clamped' : True, 'max_value' : value}


@register_item_type('mvAppItemType::InputFloat')
class InputFloat(GuiItem):
    format: str = ConfigProperty()
    on_enter: bool = ConfigProperty()
    step: float = ConfigProperty()
    step_fast: float = ConfigProperty()
    readonly: bool = ConfigProperty()

    min_value: Optional[float] = ConfigProperty(
        fvalue = _min_clamped_value,
        fconfig = _min_clamped_config,
    )
    
    max_value: Optional[float] = ConfigProperty(
        fvalue = _max_clamped_value,
        fconfig = _max_clamped_config,
    )

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
class InputInt(GuiItem):
    format: str = ConfigProperty()
    on_enter: bool = ConfigProperty()
    step: float = ConfigProperty()
    step_fast: float = ConfigProperty()
    readonly: bool = ConfigProperty()

    min_value: Optional[int] = ConfigProperty(
        fvalue = _min_clamped_value,
        fconfig = _min_clamped_config,
    )

    max_value: Optional[int] = ConfigProperty(
        fvalue = _max_clamped_value,
        fconfig = _max_clamped_config,
    )

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
    from objpygui.core import GuiData
    from objpygui.window import Window

    linked_ints = GuiData([0, 3, -1, 2])

    with Window('Test Window') as window:
        t = InputText('InputText')
        f = InputFloat('InputFloat', default_value=4.3)
        f2 = InputFloat2('InputFloat2', tip='tooltip')
        i = InputInt('InputInt', data_source = linked_ints)
        i2 = InputInt2('InputInt2', data_source = linked_ints)
        i4 = InputInt4('InputInt4', data_source = linked_ints)

    get_item_type(f2.id)
    print(f2.tip)

    from dearpygui.simple import *
    show_documentation()

    # start_dearpygui()