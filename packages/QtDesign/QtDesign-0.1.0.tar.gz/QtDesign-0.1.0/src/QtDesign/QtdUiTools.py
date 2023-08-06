from PySide2 import QtCore, QtUiTools, QtWidgets
from QtDesign import QtdWidgets

import typing


class QDesignLoader(QtUiTools.QUiLoader):

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent=parent)

        self.registerCustomWidget(QtdWidgets.QCard)
        self.registerCustomWidget(QtdWidgets.QRichTabBar)
        self.registerCustomWidget(QtdWidgets.QRichTabWidget)

    def createWidget(self, className: str, parent: typing.Optional[QtWidgets.QWidget] = None, name: str = "") -> QtWidgets.QWidget:
        if parent is None:
            # Instead of creating new instance of base window, use parent as base window instead
            return self.parent()

        else:
            # Add widget as attribute of parent window
            widget = super().createWidget(className, parent=parent, name=name)
            setattr(self.parent(), name, widget)

            return widget


def loadUi(uifile: str, parent: QtWidgets.QWidget, customWidgetTypes: list[object] = []) -> None:
    """
    Loads a ui file into an existing parent widget and automatically registers QtDesign widgets.
    Custom promoted widgets can be registered using the customWidgetTypes argument.
    """

    loader = QDesignLoader(parent)
    for widget in customWidgetTypes:
        loader.registerCustomWidget(widget)

    widget = loader.load(uifile)
    QtCore.QMetaObject.connectSlotsByName(widget)

    return widget
