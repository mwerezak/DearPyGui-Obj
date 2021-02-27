Wrapper Object System
=====================

.. automodule:: dearpygui_obj.wrapper

.. rubric:: Summary

.. autosummary:: 
    :nosignatures:

    dearpygui_wrapper
    PyGuiObject
    ConfigProperty

PyGuiObject
---------

.. autodecorator:: dearpygui_wrapper

.. autoclass:: PyGuiObject
    :members:
    :undoc-members:

    .. automethod:: _setup_add_widget
    .. automethod:: _setup_preexisting

Item Configuration
------------------

.. autoclass:: ConfigProperty
    :members:
    :undoc-members:
    :special-members: __get__, __set__, __call__

    .. TODO rewrite this

    .. By default, this class is used to get or set a single configuration key, which itself defaults to the
    .. attribute name given to the descriptor.

    .. This default behavior can be overidden by providing **fvalue** and **fconfig** converter
    .. methods, analogous to the way normal Python properties work.

    .. Both **fvalue** and **fconfig** must take exactly two arguments. The first argument for both
    .. is the :class:`PyGuiObject` instance that holds the descriptor.

    .. **fvalue** should take a dictionary of config values produced by
    .. :func:`dearpygui.core.get_item_configuration` and returns the value that is obtained when the
    .. descriptor is accessed.

    .. **fconfig** should do the reverse. Its 2nd argument should take the value that is being
    .. assigned to the descriptor, and it should return a dictionary of values that will be supplied to
    .. :func:`dearpygui.core.configure_item`.

    .. Ideally,
    .. ``fvalue(obj, fconfig(obj, value)) == value`` and
    .. ``fconfig(obj, fvalue(obj, config)) == config``
    .. should both be satisfied in order for configuration values to be stable.

    .. Also, if an **fconfig** function is given, adding the descriptor to an :class:`PyGuiObject`
    .. class will automatically create a custom keyword parameter. This can be prevented using the
    .. **no_keyword** argument.

    This class can be used directly or as a decorator. For example:

    .. code-block:: python

        class ExampleWidget(PyGuiObject):
            simple_config_example: int = ConfigProperty()

            @ConfigProperty()
            def custom_config_example(config) -> str:
                ...
            @custom_config_example.getconfig
            def custom_config_example(value: str) -> Dict[str, Any]:
                ...

         with Window('Example Window'):
             wid = ExampleWidget('Label')
             wid.simple_config_example = 3
             print('config value:', wid.custom_config_example)