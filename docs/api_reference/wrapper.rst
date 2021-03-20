Widget Objects
==============

.. automodule:: dearpygui_obj.wrapper.widget

.. rubric:: Summary

.. autosummary:: 
    :nosignatures:

    Widget
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

    **Containers**

    .. autosummary::
        :nosignatures:

        is_container
        iter_children
        add_child

    **Data and Values**

    .. autosummary::
        :nosignatures:

        data_source
        value

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

    .. automethod:: _setup_add_widget
    .. automethod:: _setup_preexisting


.. autoclass:: DefaultWidget
    :members:
    :undoc-members:


ItemWidget
----------

.. autoclass:: ItemWidget
    :members:
    :undoc-members:


ConfigProperty
--------------

.. autoclass:: ConfigProperty
    :members:
    :undoc-members:
    :special-members: __get__, __set__, __call__

