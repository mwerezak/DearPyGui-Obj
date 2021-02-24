from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from objpygui.core import GuiItem, ConfigProperty, register_item_type

if TYPE_CHECKING:
    from typing import Optional

class ButtonArrow(Enum):
    Invalid = -1
    Left    = 0
    Right   = 1
    Up      = 2
    Down    = 3

def _arrow_get_value(**config):
    if not config['arrow']:
        return None
    return ButtonArrow(config['direction'])

def _arrow_get_config(arrow):
    if arrow is None:
        return {'arrow' : False}
    return {'arrow' : True, 'direction' : arrow.value}

@register_item_type('mvAppItemType::Button')
class Button(GuiItem):
    small: bool = ConfigProperty()
    arrow: Optional[ButtonArrow] = ConfigProperty(
        get_value = _arrow_get_value,
        get_config = _arrow_get_config,
    )

    def _setup_add_item(self, config) -> None:
        gui_core.add_button(self.id, **config)



if __name__ == '__main__':
    from dearpygui.core import *
    from objpygui.window import Window

    with Window('Test Window') as window:
        Button('Regular Button')
        Button(arrow=ButtonArrow.Left)

    start_dearpygui()

