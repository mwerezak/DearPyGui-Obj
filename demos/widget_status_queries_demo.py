from __future__ import annotations

from dearpygui_obj import start_gui, stop_gui, set_render_callback
from dearpygui_obj.data import ColorRGBA
from dearpygui_obj.window import Window
from dearpygui_obj.basic import Text, Button, Separator
from dearpygui_obj.input import InputText, SliderFloat
from dearpygui_obj.layout import group_horizontal, LayoutGroup

class StatusFlags(LayoutGroup):
    def __init__(self, target, **config):
        self.target = target
        super().__init__(**config)

        with self:
            with group_horizontal(spacing=5):
                self.visible_label = Text('[visible]')
                self.hovered_label = Text('[hovered]')
                self.focused_label = Text('[focused]')
                self.clicked_label = Text('[clicked]')

            with group_horizontal(spacing=5):
                self.active_label = Text('[active]')
                self.activated_label = Text('[activated]')
                self.deactivated_label = Text('[deactivated]')
                self.edited_label = Text('[edited]')
                self.deact_after_edit_label = Text('[deactivated after edit]')

        self.update()

    @staticmethod
    def _interpolate_colors(from_color, to_color, step):
        values = (
            (1.0 - step)*from_value + step*to_value
            for from_value, to_value in zip(from_color, to_color)
        )
        return ColorRGBA(*values)

    _true_color = ColorRGBA(1, 0, 0)
    _false_color = ColorRGBA(0.2, 0.2, 0.2)

    def _update_color(self, label, value):
        target_color = self._true_color if value else self._false_color
        if value:
            label.color = target_color
        else:
            label.color = self._interpolate_colors(label.color, target_color, 0.1)

    def update(self):
        self._update_color(self.active_label, self.target.active)
        self._update_color(self.visible_label, self.target.is_visible())
        self._update_color(self.hovered_label, self.target.is_hovered())
        self._update_color(self.focused_label, self.target.is_focused())
        self._update_color(self.clicked_label, self.target.was_clicked())

        self._update_color(self.activated_label, self.target.was_activated())
        self._update_color(self.deactivated_label, self.target.was_deactivated())
        self._update_color(self.edited_label, self.target.was_edited())
        self._update_color(self.deact_after_edit_label, self.target.was_deactivated_after_edit())

if __name__ == '__main__':
    with Window("Example Window") as win:
        btn = Button()
        btn_status = StatusFlags(btn)

        Separator()

        textbox = InputText()
        textbox_status = StatusFlags(textbox)

        Separator()

        slider = SliderFloat()
        slider_status = StatusFlags(slider)

    @win.on_close
    def on_close():
        stop_gui()

    @set_render_callback
    def render():
        btn_status.update()
        textbox_status.update()
        slider_status.update()

    start_gui()
