from PyQt4.Qt import QTabWidget

from GEditorCentralLayerW import GEditorCentralLayerW
from GEditorCentralModelW import GEditorCentralModelW


class GEditorCentralTabW(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.addTab(GEditorCentralLayerW(), "Layer")
        self.addTab(GEditorCentralModelW(), "Model")
