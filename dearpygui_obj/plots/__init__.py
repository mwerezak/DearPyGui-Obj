from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import dearpygui.core as dpgcore

from dearpygui_obj import _register_item_type
from dearpygui_obj.wrapper.widget import Widget, ItemWidget, ValueWidget, ConfigProperty

if TYPE_CHECKING:
    pass


@_register_item_type('mvAppItemType::SimplePlot')
class SimplePlot(Widget, ItemWidget, ValueWidget[Sequence[float]]):
    """A simple plot to visualize a sequence of float values."""

    label: str = ConfigProperty()

    #: Overlays text (similar to a plot title).
    title: str = ConfigProperty(key='overlay')

    minscale: float = ConfigProperty()
    maxscale: float = ConfigProperty()
    histogram: bool = ConfigProperty()

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_simple_plot(self.id, **dpg_args)


__all__ = [
    'SimplePlot',
]
