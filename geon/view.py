from geon.guiutils import *
from copy import *


class GlobalCanvas(QgsMapCanvas):
    def __init__(self):
        self._layerSet = None
        self._displayedSet = None
        QgsMapCanvas.__init__(self)

    def setLayerSet(self, layerSet):
        self._layerSet = layerSet
        self._displayedSet = copy(self._layerSet)
        QgsMapCanvas.setLayerSet(self, self._displayedSet)

    def hideLayer(self, layer):
        self._displayedSet.remove(layer)
        QgsMapCanvas.setLayerSet(self, self._displayedSet)
        self.refresh()

    def showLayer(self, layer):
        self._displayedSet.insert(self._layerSet.index(layer), layer)
        QgsMapCanvas.setLayerSet(self, self._displayedSet)
        self.refresh()

    def moveLayerUp(self, layer):
        newIndex = self._displayedSet.index(layer) - 1
        if newIndex >= 0:
            self._displayedSet.remove(layer)
            self._displayedSet.insert(newIndex, layer)
            QgsMapCanvas.setLayerSet(self, self._displayedSet)
            self.refresh()

    def moveLayerDown(self, layer):
        newIndex = self._displayedSet.index(layer) + 1
        if newIndex < len(self._displayedSet):
            self._displayedSet.remove(layer)
            self._displayedSet.insert(newIndex, layer)
            QgsMapCanvas.setLayerSet(self, self._displayedSet)
            self.refresh()

class MainWindow(QMainWindow):
    def __init__(self, layerSet):
        QMainWindow.__init__(self)
        self.showMaximized()
        self._canvas = GlobalCanvas()
        self._canvas.setCanvasColor(Qt.white)
        self.setCentralWidget(self._canvas)

        self._layerSet = layerSet
        self._canvas.setLayerSet(layerSet)

        self._extent = self._layerSet.rawLayers[len(self._layerSet.rawLayers) - 1].extent()
        self._canvas.setExtent(self._extent)

        actionZoomIn = QAction("Zoom in", self)
        actionZoomOut = QAction("Zoom out", self)
        actionPan = QAction("Pan", self)
        actionRectangle = QAction("Draw rectangle", self)

        actionZoomIn.setCheckable(True)
        actionZoomOut.setCheckable(True)
        actionPan.setCheckable(True)
        actionRectangle.setCheckable(True)

        self.connect(actionZoomIn, SIGNAL("triggered()"), self.zoomIn)
        self.connect(actionZoomOut, SIGNAL("triggered()"), self.zoomOut)
        self.connect(actionPan, SIGNAL("triggered()"), self.pan)
        self.connect(actionRectangle, SIGNAL("triggered()"), self.drawRectangle)

        self.toolbar = self.addToolBar("_canvas actions")
        self.toolbar.setMovable(False)
        self.toolbar.addAction(actionZoomIn)
        self.toolbar.addAction(actionZoomOut)
        self.toolbar.addAction(actionPan)
        self.toolbar.addSeparator()
        self.toolbar.addAction(actionRectangle)

        # create the map tools
        self.toolPan = QgsMapToolPan(self._canvas)
        self.toolPan.setAction(actionPan)
        self.toolZoomIn = QgsMapToolZoom(self._canvas, False)  # false = in
        self.toolZoomIn.setAction(actionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self._canvas, True)  # true = out
        self.toolZoomOut.setAction(actionZoomOut)
        self.toolRectangle = RectangleMapTool(self._canvas)
        self.toolRectangle.setAction(actionRectangle)

        self.pan()

        self.dock = LayerDocker(self.centralWidget(), layerSet, self._canvas)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

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

    def zoomIn(self):
        self._canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self._canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self._canvas.setMapTool(self.toolPan)

    def drawRectangle(self):
        self._canvas.setMapTool(self.toolRectangle)

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

