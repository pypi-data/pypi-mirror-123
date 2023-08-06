# QtDesign
### Overview
QtDesign Widgets are intended to extend the behavior of PySide2 by providing custom widgets that look and behave similarly to native components while allowing additional flexibility when designing an application.

All widgets are designed to work as seamlessly as possible with Qt Designer's widget promotion feature through the use of the `loadUi` method from the [QtdUiTools](src/QtDesign/QtdUiTools.py) module.

### Motivation behind loadUi
One convenient feature of PyQt and Pyside is the ability to rapidly prototype a layout by directly loading a ui file from QtDesigner. PyQt's implementation of this feature allows a ui file to be loaded directly into an existing QWidget. This method allows developers to mimic how their application would work if they were inheriting a compiled version of the widget.

PySide's implementation of this feature unfortunately returns a new QWidget object which makes it awkward to extend the functionality in a way that would mimic a pure python implementation. QtDesign's `loadUi` function was included to mimic the functionality of PyQt's implementation while also automatically including automatic registration of the custom widgets provided by QtDesign.