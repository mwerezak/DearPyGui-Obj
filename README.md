# DearPyGui-Obj
An object-oriented interface for [Dear PyGui](https://github.com/hoffstadt/DearPyGui).

*Dear PyGui* is an excellent Python GUI framework built on top of the [Dear ImGui](https://github.com/ocornut/imgui) immediate-mode lightweight graphical interface library for C++. Dear PyGui itself is mostly a C++/CPython library with a thin scripting layer as it's primary interface.

This project aims to implement a pure-Python interface to Dear PyGui that takes full advantage of the Python language to provide a concise and ergonomic API.

DearPyGui-Obj aims to be *fully compatible* with Dear PyGui. This means that you can freely mix modules and code that use DearPyGui and DearPyGui-Obj without issues. Wherever possible, widget classes are designed to draw all of their state from DPG so that there is no possibility of invalidation. You can even create instances for widgets that were created from outside of DearPyGui-Obj. 

You'll find that there's a strong correspondence between DearPyGui-Obj and DearPyGui for the most part.
## Documentation
Documentation (on ReadTheDocs) can be found [here](https://dearpygui-obj.readthedocs.io/en/latest/index.html).

## Example Usage
Using *DearPyGui-Obj* is as simple as creating a script like the one below:

``` python
from dearpygui_obj import start_gui
from dearpygui_obj.widgets import *

with Window("Example Window") as win:
    Text("Hello world!")
    textbox = InputText("string")
    slider = SliderFloat("float")
    
    btn = Button("Save")
    @btn.callback()
    def callback(sender, data):
        textbox.value = str(slider.value)

start_gui()
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
