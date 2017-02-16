from PyQt4.Qt import QMainWindow, Qt
from qgis.gui import QgsMapToolPan

from Geon.gui import GMainCanvas, GLayerDocker


class GApplicationWindow(QMainWindow):
    def __init__(self, layerSet):
        QMainWindow.__init__(self)
        self.showFullScreen()
        self._canvas = GMainCanvas()
        self._canvas.setCanvasColor(Qt.white)
        self.setCentralWidget(self._canvas)

        self._layerSet = layerSet
        self._canvas.setLayerSet(layerSet)

        self._extent = self._layerSet.rawLayers[len(self._layerSet.rawLayers) - 1].extent()
        self._canvas.setExtent(self._extent)

        self._toolPan = QgsMapToolPan(self._canvas)
        self.pan()

        self._layerDock = GLayerDocker(self.centralWidget(), layerSet, self._canvas)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._layerDock)

    def setLayerSet(self, layerSet, extent=None):
        self._layerSet = layerSet
        self._canvas.setLayerSet(layerSet)

        if extent:
            self._extent = extent
        else:
            self._extent = self._layerSet.rawLayers[len(self._layerSet.rawLayers) - 1].extent()

        self._canvas.setExtent(self._extent)

    def addLayerSet(self, layerSet):
        self._layerSet.appendLayerSet(layerSet)

    def pan(self):
        self._canvas.setMapTool(self._toolPan)

    def _getCanvas(self):
        return self._canvas

    def _getLayerSet(self):
        return self._layerSet

    def _setLayerSet(self, newLayerSet):
        self._layerSet = newLayerSet
        self._canvas.setLayerSet(self._layerSet)

    def _getExtent(self):
        return self._extent

    def _setExtent(self, newExtent):
        self._extent = newExtent

    canvas = property(_getCanvas)
    extent = property(_getExtent, _setExtent)
    layerSet = property(_getLayerSet, _setLayerSet)
