from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core

if TYPE_CHECKING:
    from typing import Any, Optional


class GuiData:
    def __init__(self, name: str, init_value: Optional[Any] = None):
        self.name = name
        if init_value is not None:
            gui_core.add_value(self.name, init_value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name})'

    def __str__(self) -> str:
        return self.name

    @property
    def value(self) -> Any:
        return gui_core.get_value(self.name)

    @value.setter
    def value(self, new_value: Any) -> None:
        gui_core.set_value(self.name, new_value)
