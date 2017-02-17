from PyQt4.Qt import QStatusBar


class GEditorStatusBar(QStatusBar):
    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)

        self.showMessage("Not connected to a database")
