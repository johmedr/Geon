from PyQt4.Qt import QWidget


class GEditorModelTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # TODO Add layer visualisation (correlated with the layer list current selection)
