from PyQt4.Qt import QToolButton, QPushButton, QVBoxLayout
from PyQt4.QtCore import Qt, SIGNAL
from qgis.gui import QgsMapCanvas


class GAppLayerW(QgsMapCanvas):
    def __init__(self, layer, rawLayer, linkedCanvas, dock):

        # Canvas params
        QgsMapCanvas.__init__(self, dock)
        self.setCanvasColor(Qt.white)
        self.setWheelAction(QgsMapCanvas.WheelZoom, factor=0)
        self._dock = dock

        # Add buttons
        buttonWidth = self.width() / 2.5

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
        if not self._hidden:
            self._linkedCanvas.moveLayerUp(self._layer)
            self._dock.moveWidgetUp(self)

    def moveDown(self):
        if not self._hidden:
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
        elif keyEvent.key() == Qt.Key_H:
            self.toggleLayer()

    def keyPressed(self, keyEvent):
        pass

    def keyReleased(self, QKeyEvent):
        pass

    def keyReleaseEvent(self, QKeyEvent):
        pass

    def _getCanvas(self):
        return self._canvas

    canvas = property(_getCanvas)
