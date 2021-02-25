API Reference
=============

.. automodule:: dearpygui_obj

.. contents:: Contents
    :local:

Core Functionality
------------------

.. autosummary:: 
    :nosignatures:

    get_item_by_id
    get_active_window
    iter_all_items
    iter_all_windows

    ItemWrapper
    ConfigProperty
    GuiData

Get/Iterate Items
^^^^^^^^^^^^^^^^^

.. autofunction:: get_item_by_id

.. autofunction:: get_active_window

.. autofunction:: iter_all_items

.. autofunction:: iter_all_windows


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

    For example:

    .. code-block:: python

        class ExampleWidget(ItemWrapper):
            simple_config_example: int = config_property()
            @config_property()
            def custom_config_example(config) -> str:
                ...
            @custom_config_example.getconfig
            def custom_config_example(value: str) -> Dict[str, Any]:
                ...
         with Window('Example Window'):
             wid = ExampleWidget('Label')
             wid.simple_config_example = 3
             print('config value:', wid.custom_config_example)

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

Layout
------

.. automodule:: dearpygui_obj.layout

.. autosummary:: 
    :nosignatures:

    ScrollView

.. autoclass:: ScrollView
    :members:
    :undoc-members:



Developer Tools
---------------

.. automodule:: dearpygui_obj.devtools

DearPyGui-Obj constains several useful developer tools which can help debug GUI applications.

.. autosummary:: 
    :nosignatures:

    DebugWindow
    MetricsWindow
    StyleEditorWindow
    DocumentationWindow
    AboutWindow

.. autoclass:: DebugWindow

.. autoclass:: MetricsWindow

.. autoclass:: StyleEditorWindow

.. autoclass:: DocumentationWindow

.. autoclass:: AboutWindow