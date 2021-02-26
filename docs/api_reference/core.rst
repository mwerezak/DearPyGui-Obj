Core Functionality
==================

.. automodule:: dearpygui_obj

.. contents:: Contents
    :local:

.. rubric:: Summary

.. autosummary:: 
    :nosignatures:

    get_item_by_id
    get_active_window
    iter_all_items
    iter_all_windows
    GuiData

Get/Iterate Items
-----------------

.. autofunction:: get_item_by_id

.. autofunction:: get_active_window

.. autofunction:: iter_all_items

.. autofunction:: iter_all_windows


Value Storage System
--------------------

.. autoclass:: GuiData
    :members:
    :undoc-members:

    .. note::

        If the GuiData's name does not reference a value that exists, attempts to
        manipulate the value will also fail silently, and attempts to retrieve the value will
        produce ``None``.

        DearPyGui does not provide a function like :func:`does_item_exist` for values so it is
        impossible to detect this.


