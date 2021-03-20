:orphan:

Deveoper's Guide
================

.. note::

	This is a work in progress.


Constructing GUI Objects
------------------------

.. .. currentmodule:: dearpygui_obj.wrapper

All wrapper objects should have an ``__init__`` signature that roughly conforms to the following convention:

.. code-block:: python

	class WidgetSubclass(Widget):

		## the two '...' in the signature can be any 
		## other parameters the subclass needs.
		def __init__(self, ..., *, ..., name_id: str = None, **config):
			... # do any setup needed before super().__init__()
			super().__init__(name_id=name_id, **config)
			... # do any other setup needed after super().__init__()

Every subclass of :class:`Widget` should provide **name_id** and **\**config.**

**name_id** allows the user to specify the Widget's ID instead of autogenerating it.

**\**config** should collect keyword arguments and use them to set the initial values
of any :class:`ConfigProperty` descriptors that the subclass has.


What to pass to ``super().__init__()``?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The base class Widget's ``__init__`` will accept three types of keyword
arguments, which will be handled in the following order of priority:

1. If the name of an init handler is passed with a value, the value will be 
processed using the handler and the resulting key-value pairs will continue on
to the next two steps.

2. If the name of a :class:`ConfigProperty` is passed with a value, the value
will be used to set the property.

3. If the name of a keyword argument for the underlying DPG ``add_*()`` function
is passed with a value, that value will be given to the corresponding keyword of
the underlying DPG function.

.. important::
	
	Never use **\**config** to collect arguments for DPG's ``add_*()`` functions

While **\**config** can be used to collect keywords that will be given straight
to ``add_*()`` this makes things confusing for the user. People shouldn't have to
go looking into DPG's API reference to figure out what keywords are valid for objects
in this library. Instead, make such arguments explicit:

.. code-block:: python

	class ExampleWidget(Widget):

		example_prop: int = ConfigProperty()

		# don't need an explicit argument for example_prop since it's a
		# ConfigProperty and the user should already know about it.
		def __init__(self, default_value, *, name_id: str = None, **config):
			super().__init__(default_value=default_value, name_id=name_id, **config)

		def _setup_add_widget(self, **kwargs):
			# takes a default_value keyword that is NOT a config property
			dearpygui.core.add_input_float(self.id, **kwargs)

The bottom line of all of this is that when a user sees a class like ExampleWidget
in the above example, they know that they can use **\**config** to set any properties
listed by :meth:`Widget.get_config_properties`, and non-property arguments like
**default_value** are not hidden from them.