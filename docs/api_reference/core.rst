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
    dearpygui_wrapper
    GuiWrapper
    config_property
    ConfigProperty
    GuiData
    ~dearpygui_obj.window.Window

Get/Iterate Items
-----------------

.. autofunction:: get_item_by_id

.. autofunction:: get_active_window

.. autofunction:: iter_all_items

.. autofunction:: iter_all_windows


Item Wrapper
------------

.. autodecorator:: dearpygui_wrapper

.. autoclass:: GuiWrapper
    :members:
    :undoc-members:

    .. automethod:: _setup_add_widget
    .. automethod:: _setup_preexisting

Item Configuration
------------------

.. autofunction:: config_property

    For example:

    .. code-block:: python

        class ExampleWidget(GuiWrapper):
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
--------------------

.. autoclass:: GuiData
    :members:
    :undoc-members:

Windows
-------

.. automodule:: dearpygui_obj.window

.. autoclass:: Window
    :members:
    :undoc-members:
