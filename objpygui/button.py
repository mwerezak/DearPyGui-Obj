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

@register_item_type('mvAppItemType::Button')
class Button(GuiItem):
    small: bool = ConfigProperty()

    _is_arrow: bool = ConfigProperty('arrow')
    _arrow_dir: int = ConfigProperty('direction')

    def __init__(self, label: str, *,
                 name: Optional[str] = None,
                 arrow: Optional[ButtonArrow] = None,
                 **config):

        super().__init__(name)
        gui_core.add_button(self.id, label=label, **config)
        self.arrow = arrow

    @property
    def arrow(self) -> Optional[ButtonArrow]:
        if not self._is_arrow:
            return None
        return ButtonArrow(self._arrow_dir)

    @arrow.setter
    def arrow(self, adir: Optional[ButtonArrow]) -> None:
        if adir is None:
            self._is_arrow = False
        else:
            self._is_arrow = True
            self._arrow_dir = adir.value


if __name__ == '__main__':
    from dearpygui.core import *
    from objpygui.window import Window

    with Window('Test Window') as window:
        button = Button('Test', arrow=ButtonArrow.Up)

    print(get_item_type(button.id))


