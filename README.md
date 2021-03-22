# DearPyGui-Obj
An object-oriented interface for [Dear PyGui](https://github.com/hoffstadt/DearPyGui).

*Dear PyGui* is an excellent Python GUI framework built on top of the [Dear ImGui](https://github.com/ocornut/imgui) immediate-mode lightweight graphical interface library for C++. Dear PyGui itself is mostly a C++/CPython library with a thin scripting layer as it's primary interface.

This project aims to implement a pure-Python interface to Dear PyGui that takes full advantage of the Python language to provide a concise and ergonomic API.

DearPyGui-Obj aims to be *fully compatible* with Dear PyGui. This means that you can freely mix modules and code that use DearPyGui and DearPyGui-Obj without issues. Wherever possible, widget classes are designed to draw all of their state from DPG so that there is no possibility of invalidation. You can even create instances for widgets that were created from outside of DearPyGui-Obj. 

You'll find that there's a strong correspondence between DearPyGui-Obj and DearPyGui for the most part.
## Documentation
Documentation (on ReadTheDocs) can be found [here](https://dearpygui-obj.readthedocs.io/en/latest/index.html).

## Features
DearPyGui-Obj makes using DPG more concise and intuitive by allowing you to get and set widget properties using attributes. Setting the callback for a
widget is easy using the `callback` decorator.

``` python
import dearpygui_obj
from dearpygui_obj import colors
from dearpygui_obj.widgets import *

with Window('Example'):
    text = Text('Edit me using the controls below!', color=colors.salmon)

    Separator()

    text_input = InputText('text content', text.value)
    text_color = ColorEdit('text color', text.color)

@text_input.callback
def callback():
    text.value = text_input.value

@text_color.callback
def callback():
    text.color = text_color.value

dearpygui_obj.start_gui()
```

DearPyGui aims to provide an easy to use and ergonomic API.
``` python
import dearpygui_obj
from dearpygui_obj import colors
from dearpygui_obj.widgets import *

with Window('Example') as win:
    ## See what config properties a widget has in the REPL
    Button.get_config_properties() # Returns ['arrow', 'enabled', 'height', ...]

    ## There are many small ergonomic improvements to the API of various widgets
    ## For example, setting arrow buttons is just an Enum instead of 
    ## two separate properties.
    btn = Button(arrow=ButtonArrow.Right)

    @btn.callback
    def callback():
        if btn.arrow:
            btn.arrow = None
            btn.label = 'Not an arrow button anymore!'

    ## Colors
    red = Text('This text is red.', color=colors.red) # preset HTML colors
    green = Text('This text is green.', color=colors.from_hex('#00FF00'))

    ## Radio buttons, combo boxes, and list widgets can be edited 
    ## as a MutableSequence
    radio = RadioButtons(['Apple', 'Orange'])
    radio[0] = 'Banana'
    radio.remove('Orange')
    radio.extend(['Pear', 'Grape'])
    del radio[-1]

## Adding widgets after creating the GUI is now a method instead of a keyword.
add_text = Button.add_to(win, 'Add Label')

@add_text.callback
def callback():
    Text.insert_before(add_text, 'Insert before.')  # insert before a widget

## Can set window on close callback after the fact (not possible in DPG 0.6.x)
@win.on_close
def callback():
    dearpygui_obj.stop_gui()

dearpygui_obj.start_gui()
```

## Installation
This project is currently in the early implementation stage, and a lot of features still need to be implemented. Even the current name for the project is provisional and may change.

**Requirements**
- Python 3.8 64-bit
- dearpygui 0.6.x

You can install from [TestPyPI](https://test.pypi.org/project/dearpygui-obj/):
```
pip install -i https://test.pypi.org/simple/ dearpygui-obj
```

Or you can simply copy the `dearpygui_obj` package somewhere where Python can find it. 
DearPyGui-Obj will be available on PyPI proper once it has reached a fuller level of feature-completeness.

## License

*DearPyGui-Obj* is licensed under the [MIT License](https://github.com/mwerezak/DearPyGui-Obj/blob/master/LICENSE).
