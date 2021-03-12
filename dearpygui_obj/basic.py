from __future__ import annotations

from warnings import warn
from enum import Enum
from typing import TYPE_CHECKING, MutableSequence

import dearpygui.core as dpgcore
from dearpygui_obj import _register_item_type
from dearpygui_obj.data import ColorRGBA, ConfigPropertyColorRGBA
from dearpygui_obj.wrapper.widget import PyGuiWidget, ConfigProperty

if TYPE_CHECKING:
    from typing import Optional, Iterable, Sequence, List
    from dearpygui_obj.wrapper.widget import ItemConfigData

## Basic Content

@_register_item_type('mvAppItemType::Text')
class Text(PyGuiWidget):
    """Just text. A basic element that displays some text."""

    value: str

    #: Wrap after this many characters. Set to -1 to disable.
    wrap: int = ConfigProperty()

    #: Display a bullet point with the text.
    bullet: bool = ConfigProperty()

    color: ColorRGBA = ConfigPropertyColorRGBA()

    def __init__(self, value: str = '', *, name_id: str = None, **config):
        super().__init__(default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_text(self.id, **dpg_args)


@_register_item_type('mvAppItemType::LabelText')
class LabelText(PyGuiWidget):
    """Adds text with a label. Useful for output values when used with a data_source."""

    value: str
    label: str = ConfigProperty()
    color: ColorRGBA = ConfigPropertyColorRGBA()

    def __init__(self, label: str = None, value: str = '', *, name_id: str = None, **config):
        super().__init__(label=label, default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_label_text(self.id, **dpg_args)


@_register_item_type('mvAppItemType::Separator')
class Separator(PyGuiWidget):
    """Adds a horizontal line."""
    def __init__(self, *, name_id: str = None, **config):
        super().__init__(name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_separator(name=self.id, **dpg_args)

## Buttons

class ButtonArrow(Enum):
    """Specifies direction for arrow buttons."""
    Left    = 0
    Right   = 1
    Up      = 2
    Down    = 3

@_register_item_type('mvAppItemType::Button')
class Button(PyGuiWidget):
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

    def __init__(self, label: str = None, *, name_id: str = None, **config):
        super().__init__(label=label, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_button(self.id, **dpg_args)


@_register_item_type('mvAppItemType::Checkbox')
class Checkbox(PyGuiWidget):
    """Simple checkbox widget."""

    value: bool

    label: str = ConfigProperty()

    def __init__(self, label: str = None, value: bool = False, *, name_id: str = None, **config):
        super().__init__(label=label, default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_checkbox(self.id, **dpg_args)

@_register_item_type('mvAppItemType::Selectable')
class Selectable(PyGuiWidget):
    """Text that can be selected, functionally similar to a checkbox."""

    value: bool
    label: str = ConfigProperty()
    span_columns: bool = ConfigProperty()

    def __init__(self, label: str = None, value: bool = False, *, name_id: str = None, **config):
        super().__init__(label=label, default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_selectable(self.id, **dpg_args)



@_register_item_type('mvAppItemType::RadioButtons')
class RadioButtons(PyGuiWidget, MutableSequence[str]):
    """A set of radio buttons.

    This widget can be used as a mutable sequence of labels. Changing the sequence will
    change the radio buttons in the group and their labels.

    The index of the selected button is obtained from the :attr:`value` property.
    """
    value: int

    horizontal: bool = ConfigProperty()

    @ConfigProperty()
    def items(self) -> Sequence[str]:
        """Get or set this widget's items as a sequence."""
        return tuple(self._get_items())

    @items.getconfig
    def items(self, items: Sequence[str]):
        return {'items':list(items)}

    def __init__(self, items: Iterable[str], value: int = 0, *, name_id: str = None, **config):
        super().__init__(items=items, default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_radio_button(self.id, **dpg_args)

    def _get_items(self) -> List[str]:
        return self.get_config()['items']

    def __len__(self) -> int:
        return len(self._get_items())

    def __getitem__(self, idx: int) -> str:
        return self._get_items()[idx]

    def __setitem__(self, idx: int, label: str) -> None:
        items = self._get_items()
        items[idx] = label
        self.set_config(items=items)

    def __delitem__(self, idx: int) -> None:
        items = self._get_items()
        del items[idx]
        self.set_config(items=items)

    def insert(self, idx: int, label: str) -> None:
        items = self._get_items()
        items.insert(idx, label)
        self.set_config(items=items)


class ComboHeightMode(Enum):
    """Specifies the height of a combo box."""
    Small   = 'height_small'   #: Max ~4 items visible.
    Regular = 'height_regular' #: Max ~8 items visible.
    Large   = 'height_large'   #: Max ~20 items visible.
    Largest = 'height_largest' #: As many items visible as possible.

@_register_item_type('mvAppItemType::Combo')
class Combo(PyGuiWidget, MutableSequence[str]):
    """A combo box (drop down).

    Unlike :class:`RadioButtons`, the value of a Combo is one of the item strings,
    not the index.

    Unless specified, none of the items are initially selected and :attr:`value` is an empty string.
    """
    value: str

    label: str = ConfigProperty()
    popup_align_left: bool = ConfigProperty()
    no_arrow_button: bool = ConfigProperty()  #: Don't display the arrow button.
    no_preview: bool = ConfigProperty()  #: Don't display the preview box showing the selected item.

    @ConfigProperty()
    def items(self) -> Sequence[str]:
        """Get or set this widget's items as a sequence."""
        return tuple(self._get_items())

    @items.getconfig
    def items(self, items: Sequence[str]):
        return {'items':list(items)}

    @ConfigProperty(key='height')
    def height_mode(self) -> ComboHeightMode:
        config = self.get_config()
        if config.get('height_small', False):
            return ComboHeightMode.Small
        if config.get('height_regular', False):
            return ComboHeightMode.Regular
        if config.get('height_large', False):
            return ComboHeightMode.Large
        if config.get('height_largest', False):
            return ComboHeightMode.Largest
        warn('could not determine height_mode')
        return ComboHeightMode.Regular # its supposedly the default?

    @height_mode.getconfig
    def height_mode(self, value: ComboHeightMode) -> ItemConfigData:
        return {
            mode.value : (mode == value)  for mode in ComboHeightMode
        }

    def __init__(self, label: str = None, items: Iterable[str] = (), value: str = '', *, name_id: str = None, **config):
        super().__init__(label=label, items=items, default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_combo(self.id, **dpg_args)

    def _get_items(self) -> List[str]:
        return self.get_config()['items']

    def __len__(self) -> int:
        return len(self._get_items())

    def __getitem__(self, idx: int) -> str:
        return self._get_items()[idx]

    def __setitem__(self, idx: int, label: str) -> None:
        items = self._get_items()
        items[idx] = label
        self.set_config(items=items)

    def __delitem__(self, idx: int) -> None:
        items = self._get_items()
        del items[idx]
        self.set_config(items=items)

    def insert(self, idx: int, label: str) -> None:
        items = self._get_items()
        items.insert(idx, label)
        self.set_config(items=items)

@_register_item_type('mvAppItemType::Listbox')
class ListBox(PyGuiWidget, MutableSequence[str]):
    """A scrollable box containing a selection of items.

    The :attr:`value` property produces the index of the selected item."""

    value: int

    label: str = ConfigProperty()
    num_visible: int = ConfigProperty(key='num_items')  #: The number of items to show.

    @ConfigProperty()
    def items(self) -> Sequence[str]:
        """Get or set this widget's items as a sequence."""
        return tuple(self._get_items())

    @items.getconfig
    def items(self, items: Sequence[str]):
        return {'items':list(items)}

    def __init__(self, label: str = None, items: Iterable[str] = (), value: int = 0, *, name_id: str = None, **config):
        super().__init__(label=label, items=items, default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_listbox(self.id, **dpg_args)

    def _get_items(self) -> List[str]:
        return self.get_config()['items']

    def __len__(self) -> int:
        return len(self._get_items())

    def __getitem__(self, idx: int) -> str:
        return self._get_items()[idx]

    def __setitem__(self, idx: int, label: str) -> None:
        items = self._get_items()
        items[idx] = label
        self.set_config(items=items)

    def __delitem__(self, idx: int) -> None:
        items = self._get_items()
        del items[idx]
        self.set_config(items=items)

    def insert(self, idx: int, label: str) -> None:
        items = self._get_items()
        items.insert(idx, label)
        self.set_config(items=items)


@_register_item_type('mvAppItemType::ProgressBar')
class ProgressBar(PyGuiWidget):
    """A progress bar.
    Displays a value given between 0.0 and 1.0."""

    value: float

    overlay_text: str = ConfigProperty(key='overlay') #: Overlayed text.

    def __init__(self, value: float = 0.0, *, name_id: str = None, **config):
        super().__init__(default_value=value, name_id=name_id, **config)

    def _setup_add_widget(self, dpg_args) -> None:
        dpgcore.add_progress_bar(self.id, **dpg_args)
