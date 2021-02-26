Wrapper Object System
=====================

.. automodule:: dearpygui_obj.wrapper

.. rubric:: Summary

.. autosummary:: 
    :nosignatures:

    dearpygui_wrapper
    PyGuiWrapper
    config_property
    ConfigProperty

PyGuiWrapper
------------

.. autodecorator:: dearpygui_wrapper

.. autoclass:: PyGuiWrapper
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