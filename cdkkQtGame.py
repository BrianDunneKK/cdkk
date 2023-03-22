import typing
from PyQt6.QtCore import (Qt, QSize, QPoint, QRect, QTimer)
from PyQt6.QtGui import (QPainter, QPainter, QPen, QBrush, QPaintEvent, QMouseEvent, QResizeEvent, QPixmap, QFont)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QCheckBox, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView, QSplashScreen, QDialog)

from cdkkGame import Game

# ----------------------------------------

class cdkkQtGame(QApplication):
    def __init__(self, argv: typing.List[str]) -> None:
        super().__init__(argv)
        self.game = Game()

    def init(self, title : str = "") -> bool:
        self.window = QMainWindow()
        return True

# ----------------------------------------

class cdkkSplashScreen:
    filename : str
    splash : QSplashScreen
    win :QWidget

    @staticmethod
    def init(filename : str, win : QWidget, show : bool, close_timeout : int):
        cdkkSplashScreen.win = win
        pix = QPixmap(filename)
        cdkkSplashScreen.splash = QSplashScreen(pix)
        if show:
            cdkkSplashScreen.show()
        if close_timeout > 0:
            QTimer.singleShot(close_timeout, cdkkSplashScreen.close)

    @staticmethod
    def show():
        cdkkSplashScreen.splash.show()

    @staticmethod
    def close(filename : str = ""):
        cdkkSplashScreen.splash.finish(cdkkSplashScreen.win)

# ----------------------------------------
