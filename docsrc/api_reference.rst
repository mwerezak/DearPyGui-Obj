API Reference
=============

.. automodule:: dearpygui_obj

.. contents:: Contents
    :local:

Core Functionality
------------------

Get/Iterate Items
^^^^^^^^^^^^^^^^^

.. autofunction:: get_item_by_id

.. autofunction:: iter_all_items


Item Wrapper Class
^^^^^^^^^^^^^^^^^^

.. autoclass:: ItemWrapper
    :members:
    :undoc-members:

    .. automethod:: _setup_add_item
    .. automethod:: _setup_pre_existing

Item Configuration
^^^^^^^^^^^^^^^^^^

.. autofunction:: config_property

.. autoclass:: ConfigProperty
    :members:
    :undoc-members:
    :special-members: __get__, __set__, __call__


Value Storage System
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: GuiData
    :members:
    :undoc-members:

Windows
^^^^^^^

.. automodule:: dearpygui_obj.window

.. autoclass:: Window
    :members:
    :undoc-members:


Basic Items
-----------

.. autosummary:: 
    :nosignatures:

    ~dearpygui_obj.button.Button
    ~dearpygui_obj.inputbox.InputText
    ~dearpygui_obj.inputbox.InputFloat
    ~dearpygui_obj.inputbox.InputFloat2
    ~dearpygui_obj.inputbox.InputFloat3
    ~dearpygui_obj.inputbox.InputFloat4
    ~dearpygui_obj.inputbox.InputInt
    ~dearpygui_obj.inputbox.InputInt2
    ~dearpygui_obj.inputbox.InputInt3
    ~dearpygui_obj.inputbox.InputInt4

Buttons
^^^^^^^

.. automodule:: dearpygui_obj.button

.. autoclass:: Button
    :members:
    :undoc-members:

.. autoclass:: ButtonArrow
    :members:
    :undoc-members:

Input Boxes
^^^^^^^^^^^

.. automodule:: dearpygui_obj.inputbox

.. autoclass:: InputText
    :members:
    :undoc-members:

.. autoclass:: InputFloat
    :members:
    :undoc-members:

.. autoclass:: InputFloat2
    :members:
    :undoc-members:

.. autoclass:: InputFloat3
    :members:
    :undoc-members:

.. autoclass:: InputFloat4
    :members:
    :undoc-members:

.. autoclass:: InputInt
    :members:
    :undoc-members:

.. autoclass:: InputInt2
    :members:
    :undoc-members:

.. autoclass:: InputInt3
    :members:
    :undoc-members:

.. autoclass:: InputInt4
    :members:
    :undoc-members: