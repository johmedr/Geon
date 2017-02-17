from PyQt4.Qt import QListWidget


class GEditorLayerListW(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
