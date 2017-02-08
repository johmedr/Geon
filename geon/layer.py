from PyQt4.QtCore import QFileInfo
from qgis.core import *
from geon.utils import *
from qgis.gui import QgsMapCanvasLayer


class VectorLayer(QgsVectorLayer):
    def __init__(self, postGISDatabase=None, baseName="NewLayer", table=None, subset=None, schema="public", \
                 geoColumn="geom", path=None, fileType="ogr", loadDefaultStyleFlag=True):

        if postGISDatabase:
            self._name = "vLayer<" + baseName + ">"
            postGISDatabase.uri.setDataSource(schema, table, geoColumn, subset)
            QgsVectorLayer.__init__(self, postGISDatabase.uri.uri(), self._name, postGISDatabase.user)
            if self.isValid():
                printf(self._name + " successfully loaded.")
            else:
                printf(self._name + " failed to load.", "!!")
        else:
            fileInfo = QFileInfo(path)
            self._name = "vLayer<" + fileInfo.baseName() + ">"
            QgsVectorLayer.__init__(self, path=path, baseName=fileInfo.baseName(), providerLib=fileType,
                                    loadDefaultStyleFlag=loadDefaultStyleFlag)
            if self.isValid():
                printf(self._name + " successfully loaded.")
            else:
                printf(self._name + " failed to load.", "!!")

    def __str__(self):
        return self._name


class RasterLayer(QgsRasterLayer):
    def __init__(self, path, *args):
        fileInfo = QFileInfo(path)
        self._name = "rLayer<" + fileInfo.baseName() + ">"
        QgsRasterLayer.__init__(self, path, args)

    def __str__(self):
        return self._name

class LayerSet(list):
    def __init__(self, layer=None, name=""):
        list.__init__(self)
        self._name = name
        if layer:
            self.insert(0, QgsMapCanvasLayer(layer))
            QgsMapLayerRegistry.instance().addMapLayer(layer)


    def addLayer(self, newLayer):
        self.insert(0, QgsMapCanvasLayer(newLayer))
        QgsMapLayerRegistry.instance().addMapLayer(newLayer)

    def __str__(self):
        msg = ""
        for l in self:
            msg += str(l) + " "
        return msg

