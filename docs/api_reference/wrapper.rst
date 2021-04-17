Widget Objects
==============

.. automodule:: dearpygui_obj.wrapper.widget

.. contents:: Contents
    :local:

.. rubric:: Summary

.. autosummary:: 
    :nosignatures:

    Widget
    ContainerWidget
    ContainerFinalizedError
    ItemWidget
    DefaultWidget
    ConfigProperty

Widget
------

.. autoclass:: Widget
    :members:
    :undoc-members:
    :special-members: __eq__

    **ID and Existence**

    .. autosummary::
        :nosignatures:

        id
        is_valid
        delete

    **Callbacks**
    
    .. autosummary::
        :nosignatures:

        callback
        get_callback
        set_callback
        callback_data

    **Other Properties and Status**

    .. autosummary::
        :nosignatures:

        show
        width
        height
        size
        max_size
        min_size
        tooltip
        enabled
        is_visible
        is_hovered
        is_focused

    .. automethod:: __setup_add_widget__
    .. automethod:: __setup_preexisting__


.. autoclass:: DefaultWidget
    :members:
    :undoc-members:


ContainerWidget
---------------

.. autoclass:: ContainerWidget
    :members:
    :undoc-members:
    :special-members: __enter__, __exit__

    .. .. automethod:: __finalize__


.. autoexception:: ContainerFinalizedError

ItemWidget
----------

.. autoclass:: ItemWidget
    :members:
    :undoc-members:


ValueWidget
-----------

.. autoclass:: ValueWidget
    :members:
    :undoc-members:

ConfigProperty
--------------

.. autoclass:: ConfigProperty
    :members:
    :undoc-members:
    :special-members: __get__, __set__, __call__

