Wrapper Object System
=====================

.. automodule:: dearpygui_obj.wrapper.widget

.. rubric:: Summary

.. autosummary:: 
    :nosignatures:

    PyGuiWidget
    DefaultWidget
    ConfigProperty

PyGuiWidget
-----------

.. autoclass:: PyGuiWidget
    :members:
    :undoc-members:

    **Item Existence**

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

    **Parent/Children**

    .. autosummary::
        :nosignatures:

        get_parent
        set_parent
        move_up
        move_down
        move_item_before

    **Containers**

    .. autosummary::
        :nosignatures:

        is_container
        iter_children
        add_child
        create_child

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


ConfigProperty
--------------

.. autoclass:: ConfigProperty
    :members:
    :undoc-members:
    :special-members: __get__, __set__, __call__

