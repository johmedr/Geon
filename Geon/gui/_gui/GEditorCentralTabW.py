from PyQt4.Qt import QTabWidget

from GEditorLayerTab import GEditorLayerTab
from GEditorModelTab import GEditorModelTab


class GEditorCentralTabW(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self._layerTab = GEditorLayerTab(self)

        self._modelTab = GEditorModelTab(self)

        self.addTab(self._layerTab, "Layer")
        self.addTab(self._modelTab, "Model")

    def layerTab(self):
        return self._layerTab

    def modelTab(self):
        return self._modelTab
