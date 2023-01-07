import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.resize(600, 600)
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        self.child.resize(100, 100)
        self.anim = QPropertyAnimation(self.child, b"pos")
        self.anim.setEndValue(QPoint(400, 400))
        self.anim.setDuration(1500)
        self.anim.start()


def main():
	app = QApplication(sys.argv)
	# eFilter=customEventFilter()
	# app.installEventFilter(eFilter)
	w = Window(app)
	w.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	# sys.excepthook = handle_exception
	main()