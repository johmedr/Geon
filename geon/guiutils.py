from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import *
from qgis.gui import *
from geon.layer import *


# Parent class for dockers
class Docker(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)


# Class for layer storage
class LayerDocker(Docker):
    def __init__(self, parent=None, layerSet=None, linkedCanvas=None):
        Docker.__init__(self, parent)

        maxDockerElem = 4
        if len(layerSet) < maxDockerElem:
            maxDockerElem = len(layerSet)

        widgetsWidth = parent.width() / maxDockerElem

        # Set dock parameters
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.setMinimumWidth(widgetsWidth)

        # Set main container parameter
        self._container = QWidget(self)
        self._container.setMinimumWidth(widgetsWidth)
        self.setWidget(self._container)

        # Vertical layout for the container (vertical dock)
        self._layout = QVBoxLayout(self._container)

        # Store the canvas of layers
        self._layerPortfolio = []

        # Create up button
        # self._buttonU = QToolButton(self._container)
        # self._buttonU.setArrowType(Qt.UpArrow)
        # self._buttonU.setFixedWidth(self._container.width())
        # self._layout.addWidget(self._buttonU)

        # For each layer in layer set :
        for i in range(0, len(layerSet)):

            # Create a new widget
            layerWidget = LayerWidget(layerSet[i], layerSet.rawLayers[i], linkedCanvas, self)

            # Set its properties
            layerWidget.setMinimumWidth(widgetsWidth)

            # Connect its with main canvas
            self.connect(linkedCanvas, SIGNAL("mapCanvasRefreshed()"), layerWidget.refreshExtent)

            # Add it to portfolio and display it
            self._layerPortfolio.append(layerWidget)
            self._layout.addWidget(layerWidget)

        # Create down button
        # self._buttonD = QToolButton(self._container)
        # self._buttonD.setArrowType(Qt.DownArrow)
        # self._buttonD.setFixedWidth(self._container.width())
        # self._layout.addWidget(self._buttonD)

    def moveWidgetUp(self, widget):
        newIndex = self._layout.indexOf(widget) - 1
        if newIndex >= 0:
            self._layout.removeWidget(widget)
            self._layout.insertWidget(newIndex, widget)

    def moveWidgetDown(self, widget):
        newIndex = self._layout.indexOf(widget) + 1
        if newIndex < len(self._layout):
            self._layout.removeWidget(widget)
            self._layout.insertWidget(newIndex, widget)


    def _getLayout(self):
        return self._layout

    layout = property(_getLayout)


class LayerWidget(QgsMapCanvas):
    def __init__(self, layer, rawLayer, linkedCanvas, dock):

        # Canvas params
        QgsMapCanvas.__init__(self, dock)
        self.setCanvasColor(Qt.white)
        self.setWheelAction(QgsMapCanvas.WheelZoom, factor=0)
        self._dock = dock

        # Add buttons
        buttonWidth = self.width()/2.5

        self._buttonUp = QToolButton(self)
        self._buttonUp.setArrowType(Qt.UpArrow)
        self._buttonUp.setMaximumWidth(buttonWidth)
        self._buttonUp.setVisible(False)
        self._buttonUp.connect(self._buttonUp, SIGNAL("clicked()"), self.moveUp)

        self._buttonHide = QPushButton("Hide")
        self._buttonHide.setMaximumWidth(buttonWidth)
        self._buttonHide.setVisible(False)
        self._buttonHide.setFocusPolicy(Qt.NoFocus)
        self._buttonHide.connect(self._buttonHide, SIGNAL("clicked()"), self.toggleLayer)

        self._buttonDown = QToolButton(self)
        self._buttonDown.setArrowType(Qt.DownArrow)
        self._buttonDown.setMaximumWidth(buttonWidth)
        self._buttonDown.setVisible(False)
        self._buttonDown.connect(self._buttonDown, SIGNAL("clicked()"), self.moveDown)

        self._layout = QVBoxLayout(self)
        self._layout.setMargin(1)
        self._layout.addWidget(self._buttonUp)
        self._layout.addWidget(self._buttonHide)
        self._layout.addWidget(self._buttonDown)

        self._rawLayer = rawLayer

        self._layer = layer
        self.setLayerSet([layer])

        self._linkedCanvas = linkedCanvas
        self._extent = self._linkedCanvas.extent()

        self.setExtent(self._extent)

        self.setFocusPolicy(Qt.StrongFocus)
        self._hidden = False

    def toggleLayer(self):
        if not self._hidden:
            self._linkedCanvas.hideLayer(self._layer)
            self._buttonHide.setText("Show")
            self._hidden = True
        else:
            self._linkedCanvas.showLayer(self._layer)
            self._buttonHide.setText("Hide")
            self._hidden = False

    def moveUp(self):
        self._linkedCanvas.moveLayerUp(self._layer)
        self._dock.moveWidgetUp(self)

    def moveDown(self):
        self._linkedCanvas.moveLayerDown(self._layer)
        self._dock.moveWidgetDown(self)

    def refreshExtent(self):
        self._extent = self._linkedCanvas.extent()
        self.zoomToFeatureExtent(self._extent)

    def isCurrentLayer(self):
        return self._linkedCanvas.currentLayer == self._rawLayer

    def setAsCurrentLayer(self):
        self._linkedCanvas.setCurrentLayer(self._rawLayer)

    def focusInEvent(self, focusEvent):
        self._buttonUp.setVisible(True)
        self._buttonHide.setVisible(True)
        self._buttonDown.setVisible(True)

        # if not self.isCurrentLayer():
        #     self.setAsCurrentLayer()

        QgsMapCanvas.focusInEvent(self, focusEvent)

    def focusOutEvent(self, focusEvent):
        if not self._buttonHide.hasFocus():
            self._buttonUp.setVisible(False)
            self._buttonHide.setVisible(False)
            self._buttonDown.setVisible(False)
        QgsMapCanvas.focusOutEvent(self, focusEvent)

    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key_Down:
            self.moveDown()
        elif keyEvent.key() == Qt.Key_Up:
            self.moveUp()

    def keyPressed(self, keyEvent):
        pass

    def keyReleased(self, QKeyEvent):
        pass

    def keyReleaseEvent(self, QKeyEvent):
        pass

    def _getCanvas(self):
        return self._canvas

    canvas = property(_getCanvas)


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
