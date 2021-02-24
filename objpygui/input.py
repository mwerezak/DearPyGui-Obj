from __future__ import annotations
from typing import TYPE_CHECKING

import dearpygui.core as gui_core
from objpygui.core import GuiItem, ConfigProperty, register_item_type

if TYPE_CHECKING:
    from typing import Optional, Any


class InputItem(GuiItem):
    def __init__(self, label: str, *,
                 source: Optional[Any] = None,
                 name: Optional[str] = None,
                 **config):

        super().__init__(name)
        source = str(source) if source is not None else ''
        gui_core.add_input_text(self.id, label=label, source=source, **config)


@register_item_type('mvAppItemType::InputText')
class InputText(InputItem):
    default_value: str = ConfigProperty()
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
    on_enter: bool = ConfigProperty()
    label: str = ConfigProperty()






if __name__ == '__main__':
    from dearpygui.core import *
    from objpygui.window import Window
    from objpygui.core import GuiData

    data = GuiData('data', '')

    with Window('Test Window') as window:
        InputText('Input', source=data)
        InputText('Input', source=data)




