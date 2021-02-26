Core Functionality
==================

.. automodule:: dearpygui_obj

.. contents:: Contents
    :local:

.. rubric:: Summary

.. autosummary:: 
    :nosignatures:

    start_gui
    stop_gui
    is_running
    get_item_by_id
    get_active_window
    iter_all_items
    iter_all_windows
    set_start_callback
    set_exit_callback
    set_render_callback
    get_delta_time
    get_total_time
    enable_vsync
    GuiData

Start/Stop the GUI Engine
-------------------------

.. autofunction:: start_gui

.. autofunction:: stop_gui

.. autofunction:: is_running

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


System-Level Callbacks
----------------------

.. autofunction:: set_start_callback

.. autofunction:: set_exit_callback

.. autofunction:: set_render_callback


Miscellaneous
-------------

.. autofunction:: get_delta_time

.. autofunction:: get_total_time

.. autofunction:: enable_vsync
