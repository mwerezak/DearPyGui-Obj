from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import dearpygui.core as dpgcore
from dearpygui_obj.wrapper.widget import Widget, ItemWidget, ContainerWidget

if TYPE_CHECKING:
    from typing import Any

class UserWidget(Widget, ItemWidget, ABC):
    """An abstract base class that is used to create custom widgets.

    This class provides a way to create custom widgets that are composed of other widgets.
    This can be useful for creating custom complex controls that you want to use like a single widget.

    Note that while the user widget is actually a container (it has to be, to hold the user's custom
    content), it not meant to be used as a :class:`.ContainerWidget`. It does not have any of the
    container widget methods like :meth:`.ContainerWidget.add_child` and cannot be used as a context
    manager.

    This makes it ideal for custom controls whose contents are 'closed' and not meant to have
    abitrary additional widgets added to them as children.
    For custom 'open' containers, see :class:`.UserContainer` (not implemented yet).

    By default, any positional arguments passed to ``__init__()`` and any keyword arguments
    that are not reserved by :class:`Widget` or :class:`ItemWidget` will be passed to the
    :meth:`__setup_content__` method.

    This method should be overriden in subclasses to actually create the contents of the custom
    widget. Furthermore, it is a good practice that subclasses define their own signature for
    :meth:`__setup_widget__` that narrows down the
    arguments to the ones they actually need."""

    def __init__(self, *args: Any, parent: str = 'None', before: str = None, name_id: str = None, **kwargs: Any):
        super().__init__(parent=parent, before=before, name_id=name_id)
        self.__setup_content__(*args, **kwargs)
        dpgcore.end()

    def __setup_add_widget__(self, dpg_args) -> None:
        for kw in ('before', 'parent'):
            if dpg_args[kw] is None:
                del dpg_args[kw]

        dpgcore.add_group(self.id, **dpg_args)

    @abstractmethod
    def __setup_content__(self, *args, **kwargs) -> None:
        """The contents of the UserWidget should be added here."""
        ...


class UserContainer(Widget, ItemWidget, ContainerWidget[Any], ABC):
    """An abstract base class that is used to create custom containers.

    This class is not yet implemented, as it requires adding to the parent stack which
    is not yet available in DPG 0.6."""

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError

__all__ = [
    'UserWidget',
]