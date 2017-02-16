from PyQt4.Qt import QMainWindow

from GEditorMenuBar import GEditorMenuBar


class GEditorMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.showMaximized()

        self.setMenuBar(GEditorMenuBar())
