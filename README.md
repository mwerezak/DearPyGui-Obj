# DearPyGui-Obj
An object-oriented interface for [Dear PyGui](https://github.com/hoffstadt/DearPyGui).

*Dear PyGui* is an excellent Python GUI framework built on top of the [Dear ImGui](https://github.com/ocornut/imgui) immediate-mode lightweight graphical interface library for C++. Dear PyGui itself is mostly a C++/CPython library with a thin scripting layer as it's primary interface.

This project aims to implement a pure-Python interface to Dear PyGui that takes full advantage of the Python language to provide a concise and ergonomic API.

## Documentation
Documentation (on ReadTheDocs) can be found [here](https://dearpygui-obj.readthedocs.io/en/latest/index.html).

## Features
DearPyGui-Obj makes using DPG more concise and intuitive by allowing you to get and set widget properties using attributes. Setting the callback for a
widget is easy using the `callback` decorator.

#### Widget Objects

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

#### Ergonomic API
``` python
import dearpygui_obj
from dearpygui_obj import colors
from dearpygui_obj.widgets import *

with Window('Example') as win:
    ## See what config properties a widget has in the REPL
    Button.get_config_properties() # Returns ['arrow', 'enabled', 'height', ...]

    ## There are small ergonomic improvements to the API of various widgets
    ## For example, setting arrow buttons is just an Enum instead of two
    ## separate properties
    btn = Button(arrow=ButtonArrow.Right)

    @btn.callback
    def callback():
        if btn.arrow:
            btn.arrow = None
            btn.label = 'Not an arrow button anymore!'

    ## Colors
    red = Text('This text is red.', color=colors.red) # preset HTML colors
    green = Text('This text is green.', color=colors.from_hex('#00FF00'))

    ## Radio buttons, combo boxes, and list widgets are mutable sequences
    radio = RadioButtons(['Apple', 'Orange'])
    radio[0] = 'Banana'
    radio.remove('Orange')
    radio.extend(['Pear', 'Grape'])
    del radio[-1]

## You can add widgets after creating the GUI using methods instead of keywords
add_text = Button.add_to(win, 'Add Label')  # add to the end of a container

@add_text.callback
def callback():
    Text.insert_before(add_text, 'Insert before.')  # insert before a widget

dearpygui_obj.start_gui()
```

#### Plots and Data Series

``` python
import dearpygui_obj
from dearpygui_obj.widgets import *
from dearpygui_obj.plots.dataseries import *

with Window('Example') as win:
    data = [ (-1, -9), (1, -4), (3, 11), (4, 5), (9, 7) ]
    lineseries = LineSeries('example', data)

    ## plot data series are mutable sequences!
    last = lineseries[-1]
    print(last.x, last.y)      # elements are named tuples
    lineseries.append((10, 2)) # but methods will accept any compatible sequence

    ## can also access and modify data as individual 1D sequences,
    ## as long as the length does not change
    print(lineseries.y[0])  # prints -9
    lineseries.y[2] += 1
    lineseries.y[3:5] = (7, 5)
    lineseries.x = [1, 2, 3, 4, 5, 6]  # even supports assignment
    #lineseries.x = [1, 2, 3]  # TypeError: cannot change length of individual DataSeries field

    plot = Plot()
    plot.add_dataseries(lineseries)

dearpygui_obj.start_gui()
```

#### Drawing API
This is the same dynamic drawing example given in the DPG Wiki. You can compare 
it with the [original code](https://github.com/hoffstadt/DearPyGui/wiki/Drawing-API#modification).

``` python
import dearpygui_obj
from dearpygui_obj import colors
from dearpygui_obj.widgets import *

counter = 0
modifier = 2

with Window("Tutorial", size=(800, 800)):
    canvas = DrawingCanvas(size=(700, 700))
    circle = canvas.draw_circle((0, 0), 5, colors.from_rgba8(255, 255, 255))

@dearpygui_obj.set_render_callback
def on_render():
    global counter, modifier

    counter += 1
    if counter < 300:
        modifier += 1
    elif counter < 600:
        modifier -= 1
    else:
        counter = 0
        modifier = 2

    circle.center = (15 + modifier*1.25, 15 + modifier*1.25)
    circle.color = colors.from_rgba8(
        255 - modifier*.8, 255 - modifier*.8, 255 - modifier*.3,
    )
    circle.radius = 15 + modifier/2
    circle.segments = round(35-modifier/10)

dearpygui_obj.start_gui()
```

#### Using DearPyGui-Obj With Existing Dear PyGui Code
DearPyGui-Obj aims to be fully *backwards compatible* with Dear PyGui. This means that you can freely mix code that uses both DearPyGui and DearPyGui-Obj without issues. Wherever possible, widget classes are designed to draw all of their state from DPG so that there is no possibility of invalidation. You can even create object instances for existing widgets that were created in vanilla DearPyGui.

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
