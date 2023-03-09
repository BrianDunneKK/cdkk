import typing
from PyQt6.QtCore import (Qt, QSize, QPoint, QRect)
from PyQt6.QtGui import (QPainter, QPainter, QPen, QBrush, QPaintEvent, QMouseEvent, QResizeEvent)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView)

# ----------------------------------------

class cdkkQtGame(QApplication):
    def __init__(self, argv: typing.List[str]) -> None:
        super().__init__(argv)
        self.game = Game()

    def init(self, title : str = "") -> bool:
        self.window = GameWindow(title)
        self.window.init()
        return True

# ----------------------------------------

