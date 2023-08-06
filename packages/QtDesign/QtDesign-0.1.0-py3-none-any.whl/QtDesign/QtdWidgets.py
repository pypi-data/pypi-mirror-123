from PySide2 import QtCore, QtGui, QtWidgets

import typing


class QCard(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        # Create button widget for card interactions
        self.__push_button = QtWidgets.QPushButton(self)
        self.__push_button.move(self.geometry().bottomRight() - self.__push_button.geometry().bottomRight())
        self.__push_button.setFixedSize(self.size())

    def pushButton(self) -> QtWidgets.QPushButton:
        return self.__push_button

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.__push_button.setFixedSize(self.size())

class QRichTabBar(QtWidgets.QTabBar):
    def __init__(self, parent):
        super().__init__(parent)

    def setTabText(self, index: int, text: str):
        label = QtWidgets.QLabel(self)
        label.setText(text)
        label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.setTabButton(index, QtWidgets.QTabBar.LeftSide, label)

    def tabText(self, index: int):
        doc = QtGui.QTextDocument()
        doc.setHtml(self.tabButton(index, QtWidgets.QTabBar.LeftSide).text())
        return doc.toPlainText()

class QRichTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._tabBar = QRichTabBar(self)
        self.setTabBar(self._tabBar)

    @typing.overload
    def addTab(self, widget: QtWidgets.QWidget, arg__2: str) -> int: ...
    @typing.overload
    def addTab(self, widget: QtWidgets.QWidget, icon: QtGui.QIcon, label: str) -> int: ...

    def addTab(self, *args, **kwargs) -> int:
        index = super().addTab(*args, **kwargs)
        text = super().tabText(index)
        super().setTabText(index, "")
        self._tabBar.setTabText(index, text)

        return index

    @typing.overload
    def insertTab(self, index: int, widget: QtWidgets.QWidget, arg__3: str) -> int: ...
    @typing.overload
    def insertTab(self, index: int, widget: QtWidgets.QWidget, icon: QtGui.QIcon, label: str) -> int: ...

    def insertTab(self, *args, **kwargs) -> int:
        index = super().insertTab(*args, **kwargs)
        text = super().tabText(index)
        super().setTabText(index, "")
        self._tabBar.setTabText(index, text)

        return index

    def setTabText(self, index: int, text: str):
        self._tabBar.setTabText(index, text)

    def tabText(self, index: int):
        return self._tabBar.tabText(index)