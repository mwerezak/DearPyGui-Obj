from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj import ColorRGBA
from dearpygui_obj.wrapper import PyGuiBase, dearpygui_wrapper, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional
    from dearpygui_obj.wrapper import ItemConfigData

## Basic Content

class Text(PyGuiBase):
    """A basic element that displays some text."""

    #: Wrap after this many characters. Set to -1 to disable.
    wrap: int

    #: Display a bullet point with the text.
    bullet: bool

    @ConfigProperty()
    def color(self) -> ColorRGBA:
        """Color of the text."""
        return ColorRGBA.dpg_import(self.get_config()['color'])

    @color.getconfig
    def color(self, value: ColorRGBA) -> ItemConfigData:
        return {'color' : value.dpg_export()}

    def __init__(self, text: str, **kwargs):
        super().__init__(default_value=text, **kwargs)

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_text(self.id, **config)

## Buttons

class ButtonArrow(Enum):
    """Specifies direction for arrow buttons."""
    Left    = 0
    Right   = 1
    Up      = 2
    Down    = 3

@dearpygui_wrapper('mvAppItemType::Button')
class Button(PyGuiBase):
    """A simple button."""

    label: str = ConfigProperty()
    
    #: If ``True``, makes the button a small button. Useful for embedding in text.
    small: bool = ConfigProperty()

    @ConfigProperty()
    def arrow(self) -> Optional[ButtonArrow]:
        """Configure the button as an arrow button.

        If the button is an arrow button, the value will be the arrow direction.
        Otherwise the value will be ``None``.

        Assigning to this property will enable/disable the arrow and/or set the direction."""
        config = self.get_config()
        if not config['arrow']:
            return None
        return ButtonArrow(config['direction'])

    @arrow.getconfig
    def arrow(self, adir: Optional[ButtonArrow]):
        if adir is None:
            return {'arrow': False}
        return {'arrow': True, 'direction': adir.value}

    def _setup_add_widget(self, config) -> None:
        dpgcore.add_button(self.id, **config)



if __name__ == '__main__':
    from dearpygui.core import *
    from dearpygui_obj.window import Window

    with Window('Test Window') as window:
        txt = Text('This is some text!', color=ColorRGBA(1.0, 0.2, 0.2))
        print(get_item_configuration(txt.id))
        print(txt.color)

        b1 = Button('Regular Button')
        @b1.callback()
        def callback(sender, data):
            print(sender, data)

        b2 = Button(arrow=ButtonArrow.Left)
        @b2.callback()
        def callback(sender, data):
            b1.small = not b1.small

    start_dearpygui()

