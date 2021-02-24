from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from dearpygui_obj import ItemWrapper, register_item_type, config_property

if TYPE_CHECKING:
    from typing import Optional

class ButtonArrow(Enum):
    """Specifies direction for arrow buttons."""
    Left    = 0
    Right   = 1
    Up      = 2
    Down    = 3

@register_item_type('mvAppItemType::Button')
class Button(ItemWrapper):
    small: bool = config_property()

    @config_property()
    def arrow(config) -> Optional[ButtonArrow]:
        """Configure the button as an arrow button.

        If the button is an arrow button, the value will be the arrow direction.
        Otherwise the value will be ``None``.

        Assigning to this property will enable/disable the arrow and/or set the direction."""
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
