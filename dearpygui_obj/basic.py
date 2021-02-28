from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj.data import ColorRGBA
from dearpygui_obj.wrapper import PyGuiObject, dearpygui_wrapper, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional
    from dearpygui_obj.wrapper import ItemConfigData

## Basic Content

@dearpygui_wrapper('mvAppItemType::Text')
class Text(PyGuiObject):
    """A basic element that displays some text."""

    #: Wrap after this many characters. Set to -1 to disable.
    wrap: int = ConfigProperty()

    #: Display a bullet point with the text.
    bullet: bool = ConfigProperty()

    @ConfigProperty()
    def color(self) -> ColorRGBA:
        """Color of the text."""
        return ColorRGBA.dpg_import(self.get_config()['color'])

    @color.getconfig
    def color(self, value: ColorRGBA) -> ItemConfigData:
        return {'color' : value.dpg_export()}

    def __init__(self, text: str, *, name_id: str = None, **config):
        super().__init__(default_value=text, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_text(self.id, **dpg_args)


@dearpygui_wrapper('mvAppItemType::LabelText')
class LabelText(PyGuiObject):
    """Adds text with a label. Useful for output values when used with a data_source."""

    label: str = ConfigProperty()

    @ConfigProperty()
    def color(self) -> ColorRGBA:
        """Color of the text."""
        return ColorRGBA.dpg_import(self.get_config()['color'])

    @color.getconfig
    def color(self, value: ColorRGBA) -> ItemConfigData:
        return {'color' : value.dpg_export()}

    def __init__(self, label: str, text: str = '', *, name_id: str = None, **config):
        super().__init__(label=label, default_value=text, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_label_text(self.id, **dpg_args)


## Buttons

class ButtonArrow(Enum):
    """Specifies direction for arrow buttons."""
    Left    = 0
    Right   = 1
    Up      = 2
    Down    = 3

@dearpygui_wrapper('mvAppItemType::Button')
class Button(PyGuiObject):
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

    def __init__(self, label: str = '', *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_button(self.id, **dpg_args)



if __name__ == '__main__':
    from dearpygui.core import *
    from dearpygui_obj.window import Window
    from dearpygui_obj.input import SliderFloat

    with Window('Test Window') as window:
        txt = Text('This is some text!', color=ColorRGBA(1.0, 0.2, 0.2))
        print(get_item_configuration(txt.id))
        print(txt.color)

        label = LabelText('Value:')
        slider = SliderFloat('')
        @slider.callback()
        def callback(sender, data):
            print(slider.value)

        b1 = Button('Regular Button')
        @b1.callback()
        def callback(sender, data):
            print(sender, data)

        b2 = Button(arrow=ButtonArrow.Left)
        @b2.callback()
        def callback(sender, data):
            b1.small = not b1.small

    start_dearpygui()

