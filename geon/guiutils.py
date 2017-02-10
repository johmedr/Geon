from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import *
from qgis.gui import *

from geon.layer import *

class Docker(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)

class LayerDocker(Docker):
    def __init__(self, parent=None, layerSet=None, linkedCanvas=None):
        Docker.__init__(self, parent)

        widgetsWidth = parent.width() / len(layerSet)

        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.setMinimumWidth(widgetsWidth)
        self._container = QWidget(self)
        self._container.setMinimumWidth(widgetsWidth)
        self.setWidget(self._container)
        self._layout = QVBoxLayout(self._container)
        self._parent = parent
        self._layerSet = layerSet
        self._layerPortfolio = []


        for l in layerSet:
            layerWidget = LayerWidget([l], linkedCanvas, self)
            layerWidget.setMinimumWidth(widgetsWidth)
            self._layerPortfolio.append(layerWidget)
            self._layout.addWidget(layerWidget)

class DockWidget(QWidget):
    def __init__(self, parentDocker=None):
        QWidget.__init__(self, parentDocker)

class LayerWidget(QgsMapCanvas):
    def __init__(self, layer=None, linkedCanvas=None, dock=None):
        QgsMapCanvas.__init__(self, dock)

        self.setCanvasColor(Qt.white)

        self._layer = layer
        self.setLayerSet(layer)
        self._linkedCanvas = linkedCanvas
        self._extent = self._linkedCanvas.extent()
        self.connect(self._linkedCanvas, SIGNAL("mapCanvasRefreshed()"), self.refreshExtent)
        self.setExtent(self._extent)


    def refreshExtent(self):
        self._extent = self._linkedCanvas.extent()
        self.zoomToFeatureExtent(self._extent)

class ToolWidget(DockWidget):
    def __init__(self, parent=None, flags=0):
        DockWidget.__init__(self, parent, flags)


class RectangleMapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.reset()

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Polygon)

    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showRect(self.startPoint, self.endPoint)

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        r = self.rectangle()
        if r is not None:
            print "Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum()

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return

        self.endPoint = self.toMapCoordinates(e.pos())
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset(QGis.Polygon)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return

        point1 = QgsPoint(startPoint.x(), startPoint.y())
        point2 = QgsPoint(startPoint.x(), endPoint.y())
        point3 = QgsPoint(endPoint.x(), endPoint.y())
        point4 = QgsPoint(endPoint.x(), startPoint.y())

        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)  # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None

        return QgsRectangle(self.startPoint, self.endPoint)

    def deactivate(self):
        super(RectangleMapTool, self).deactivate()
        self.emit(SIGNAL("deactivated()"))
