from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from dearpygui_obj import ItemWrapper, register_item_type, config_property

if TYPE_CHECKING:
    from typing import Optional

class ButtonArrow(Enum):
    Invalid = -1
    Left    = 0
    Right   = 1
    Up      = 2
    Down    = 3



@register_item_type('mvAppItemType::Button')
class Button(ItemWrapper):
    small: bool = config_property()

    @config_property()
    def arrow(config) -> Optional[ButtonArrow]:
        if not config['arrow']:
            return None
        return ButtonArrow(config['direction'])

    @arrow.getconfig
    def arrow(adir: Optional[ButtonArrow]):
        if adir is None:
            return {'arrow': False}
        return {'arrow': True, 'direction': adir.value}

    def _setup_add_item(self, config) -> None:
        gui_core.add_button(self.id, **config)



if __name__ == '__main__':
    from dearpygui.core import *
    from dearpygui_obj.window import Window

    with Window('Test Window') as window:
        b1 = Button('Regular Button')
        @b1.callback()
        def callback(source, data):
            print(source, data)

        b2 = Button(arrow=ButtonArrow.Left)



    start_dearpygui()

