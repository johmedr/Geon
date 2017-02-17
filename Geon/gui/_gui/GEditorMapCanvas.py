from qgis.gui import QgsMapToolPan

from GMapCanvas import GMapCanvas


class GEditorMapCanvas(GMapCanvas):
    def __init__(self, parent=None, layerSet=None):
        GMapCanvas.__init__(self, parent, layerSet)
        self._toolPan = QgsMapToolPan(self)
        self.pan()

    def pan(self):
        self.setMapTool(self._toolPan)
