from PyQt4.Qt import QColor, QFileInfo
from qgis.core import QgsVectorLayer

from Geon.utils import *


class GVectorLayer(QgsVectorLayer):
    def __init__(self, postGISDatabase=None, baseName=None, table=None, subset=None, schema="public",
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
