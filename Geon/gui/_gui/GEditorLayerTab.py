from PyQt4.Qt import QWidget, QVBoxLayout

from GEditorMapCanvas import GEditorMapCanvas
from Geon.core import GLayerSet


class GEditorLayerTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._canvas = GEditorMapCanvas(self)
        self._canvas.setMinimumHeight(self.height())

        layout = QVBoxLayout()
        layout.addWidget(self._canvas)
        self.setLayout(layout)
        self.show()

    def viewLayer(self, layer):
        layerSet = GLayerSet(layer)
        self._canvas.setLayerSet(layerSet)

    def mapCanvas(self):
        return self._canvas
