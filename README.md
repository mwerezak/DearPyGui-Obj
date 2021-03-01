# DearPyGui-Obj
An object-oriented interface for [Dear PyGui](https://github.com/hoffstadt/DearPyGui).

*Dear PyGui* is an excellent Python GUI framework built on top of the [Dear ImGui](https://github.com/ocornut/imgui) immediate-mode lightweight graphical interface library for C++. Dear PyGui itself is mostly a C++/CPython library with a thin scripting layer as it's primary interface.

This project aims to implement a pure-Python interface to Dear PyGui that takes full advantage of the Python language to provide a concise and ergonomic API.

Another goal of DearPyGui-Obj is that the object library should be *fully compatible* with Dear PyGui. This means that any DPG code that executes outside of DearPyGui-Obj should not invalidate or break any part of the object library.

## Documentation
Documentation (on ReadTheDocs) can be found [here](https://dearpygui-obj.readthedocs.io/en/latest/index.html).

## Example Usage
Using *DearPyGui-Obj* is as simple as creating a script like the one below:

``` python
from dearpygui_obj import get_item_by_id, start_gui
from dearpygui_obj.window import Window
from dearpygui_obj.basic import Text, Button
from dearpygui_obj.input import InputText, SliderFloat

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
