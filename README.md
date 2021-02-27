# DearPyGui-Obj
An object-oriented interface for [Dear PyGui](https://github.com/hoffstadt/DearPyGui).

*Dear PyGui* is an excellent Python GUI framework built on top of the [Dear ImGui](https://github.com/ocornut/imgui) immediate-mode lightweight graphical interface library for C++. Dear PyGui itself is mostly a C++/CPython library with a thin scripting layer as it's primary interface.

This project aims to implement a pure-Python interface to *Dear PyGui* that takes full advantage of the Python language to provide a concise and ergonomic API.

## Example Usage
Using *DearPyGui-Obj* is as simple as creating a script like the one below:

``` python
import dearpygui_obj
from dearpygui_obj.window import Window
from dearpygui_obj.basic import Text, Button
from dearpygui_obj.input import InputText, SliderFloat

with Window("Example Window"):
    Text("Hello world!")
    Button("Save").set_callback(lambda sender, data: print("Save Clicked"))
    InputText("string")
    SliderFloat("float")

dearpygui_obj.start_gui()
```

## Installation
This project is currently in the very early planning and implementation stages, and a lot of features still need to be implemented. Even the current name for the project is provisional and may change.

**Requirements**
- Python 3.8 64-bit
- dearpygui 0.6.x

To install, simply copy the `dearpygui_obj` package somewhere where Python can find it. *DearPyGui-Obj* will be available on the Test PyPI in the near future, and on PyPI proper once it has reached a fuller level of feature-completeness.

## Documentation
Documentation can be found [here](https://dearpygui-obj.readthedocs.io/en/latest/index.html).

## License

*DearPyGui-Obj* is licensed under the [MIT License](https://github.com/mwerezak/DearPyGui-Obj/blob/master/LICENSE).
