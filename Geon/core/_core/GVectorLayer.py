from PyQt4.Qt import QColor, QFileInfo
from qgis.core import QgsVectorLayer

from GLayer import GLayer
from Geon.utils import *


class GVectorLayer(QgsVectorLayer, GLayer):
    def __init__(self, postGISDatabase=None, baseName=None, table=None, subset=None, schema="public",
                 geoColumn="geom", path=None, fileType="ogr", loadDefaultStyleFlag=True):

        # Parameters
        self._name = ""
        self._baseName = ""
        self._symbols = None
        self._color = QColor()

        # Query data from PostGIS database
        if postGISDatabase:
            if baseName:
                name = "vLayer<" + baseName + ">"
            else:
                baseName = table
                name = "vLayer<" + table + ">"

            GLayer.__init__(self, name=name, baseName=baseName)
            postGISDatabase.uri.setDataSource(schema, table, geoColumn, subset)
            QgsVectorLayer.__init__(self, postGISDatabase.uri.uri(), self._name, postGISDatabase.user)

        # Query data from file
        else:
            fileInfo = QFileInfo(path)
            name = "vLayer<" + fileInfo.baseName() + ">"
            baseName = fileInfo.baseName()

            GLayer.__init__(self, name=name, baseName=baseName)
            QgsVectorLayer.__init__(self, path=path, baseName=fileInfo.baseName(), providerLib=fileType,
                                    loadDefaultStyleFlag=loadDefaultStyleFlag)

        if not self.isValid():
            GPrint(self._name + " failed to load.", "!!")
        else:
            GPrint(self._name + " successfully loaded.")

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
