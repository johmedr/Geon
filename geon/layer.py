from PyQt4.Qt import QColor
from PyQt4.QtCore import QFileInfo
from qgis.core import *
from qgis.gui import QgsMapCanvasLayer
from geon.utils import *


class VectorLayer(QgsVectorLayer):
    def __init__(self, postGISDatabase=None,  baseName=None, table=None, subset=None, schema="public", \
                 geoColumn="geom", path=None, fileType="ogr", loadDefaultStyleFlag=True):

        # Parameters
        self._name = ""
        self._symbols = None
        self._color = QColor()

        # Query data from PostGIS database
        if postGISDatabase:
            if baseName:
                self._name = "vLayer<" + baseName + ">"
            else:
                self._name = "vLayer<" + table + ">"

            postGISDatabase.uri.setDataSource(schema, table, geoColumn, subset)
            QgsVectorLayer.__init__(self, postGISDatabase.uri.uri(), self._name, postGISDatabase.user)

        # Query data from file
        else:
            fileInfo = QFileInfo(path)
            self._name = "vLayer<" + fileInfo.baseName() + ">"
            QgsVectorLayer.__init__(self, path=path, baseName=fileInfo.baseName(), providerLib=fileType,
                                    loadDefaultStyleFlag=loadDefaultStyleFlag)

        if not self.isValid():
            printf(self._name + " failed to load.", "!!")
        else:
            printf(self._name + " successfully loaded.")

            # Deal with color param
            self._symbols = self.rendererV2().symbols()
            self._color = self._symbols[0].color()



    def _getColor(self):
        return self._color

    def _setColor(self, newColor):
        self._color = newColor
        if self.isValid():
            self._symbols[0].setColor(newColor)

    color = property(_getColor, _setColor)



class RasterLayer(QgsRasterLayer):
    def __init__(self, path,*args):
        fileInfo = QFileInfo(path)
        self._name = "rLayer<" + fileInfo.baseName() + ">"
        QgsRasterLayer.__init__(self, path, *args)
        if not self.isValid():
            printf(self._name + " failed to load.", "!!")
        else:
            printf(self._name + " successfully loaded.")


class LayerSet(list):
    def __init__(self, *layers):
        list.__init__(self)
        self._rawLayers = []
        if layers:
            for l in list(layers):
                self.insert(0, QgsMapCanvasLayer(l))
                self._rawLayers.insert(0, l)
                QgsMapLayerRegistry.instance().addMapLayer(l)


    def addLayers(self, *newLayers):
        for l in list(newLayers):
            self.insert(0, QgsMapCanvasLayer(l))
            self._rawLayers.insert(0, l)
            QgsMapLayerRegistry.instance().addMapLayer(l)

    def appendLayerSet(self, layerSet):
        self = self + layerSet

    def addBasemap(self, basemap):
        self._rawLayers.append(basemap)
        self.append(QgsMapCanvasLayer(basemap))
        QgsMapLayerRegistry.instance().addMapLayer(basemap)

    def __str__(self):
        msg = ""
        for l in self:
            msg += str(l) + " "
        return msg

    def __copy__(self):
        newLayerSet = self
        newLayerSet._name = self._name
        return newLayerSet

    def _getRawLayers(self):
        return self._rawLayers

    rawLayers = property(_getRawLayers)
