from PyQt4.Qt import QColor, QObject
from PyQt4.QtCore import pyqtSlot

from Geon.core import GPostGISDatabase, GLayerSet, GVectorLayer, GRasterLayer


# TODO Split this class in many controllers
class GEditorController(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._database = None
        self._layerSet = None
        self._currentLayer = None
        self._currentLayerColor = None
        self._mapCanvas = None

    # Add something to check if db is already connected
    def connectDatabase(self, host, port, database, user, password):
        # TODO Create a multi-database management functionality ?
        pgdb = GPostGISDatabase(host=host, port=port, database=database, user=user, passwd=password)
        if pgdb.isConnected():
            error = False
            self._database = pgdb
        else:
            error = pgdb.getError()
        return error

    def databaseConnected(self):
        ret = False
        if self._database:
            ret = self._database.isConnected()
        return ret

    def databaseTables(self):
        if self._database:
            return self._database.tables()
        else:
            return False

    def databaseName(self):
        return self._database.getName()

    def createLayerFromTable(self, tableName, subset):
        # FIXME error if database not connected
        if not self._layerSet:
            self._layerSet = GLayerSet()
        lay = GVectorLayer(postGISDatabase=self._database, table=tableName, baseName=tableName, subset=subset)
        self._layerSet.addLayers(lay)

    @pyqtSlot(str)
    def createVectorLayerFromFile(self, filePath):
        if not self._layerSet:
            self._layerSet = GLayerSet()
        lay = GVectorLayer(path=filePath)
        self._layerSet.addLayers(lay)

    @pyqtSlot(str)
    def createRasterLayerFromFile(self, filePath):
        if not self._layerSet:
            self._layerSet = GLayerSet()
        lay = GRasterLayer(path=filePath)
        self._layerSet.addBasemap(lay)

    def layerSet(self):
        return self._layerSet

    def getLayer(self, layerName):
        return self._layerSet.layer(layerName)

    def setCurrentLayer(self, layer):
        self._currentLayer = layer
        self._currentLayerColor = layer.color

    @pyqtSlot(QColor)
    def setCurrentLayerColor(self, color):
        self._currentLayer.color = color
        self._currentLayerColor = color
        self._mapCanvas.refresh()

    @pyqtSlot(QColor)
    def showNewCurrentLayerColor(self, color):
        self._currentLayer.color = color
        self._mapCanvas.refresh()

    def resetCurrentLayerColor(self):
        self._currentLayer.color = self._currentLayerColor
        self._mapCanvas.refresh()

    def setMapCanvas(self, mapCanvas):
        self._mapCanvas = mapCanvas
