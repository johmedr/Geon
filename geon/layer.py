from qgis.core import *
from geon.database import PostGISDatabase
from geon.utils import *
from PyQt4.QtCore import QFileInfo


class VectorLayer(QgsVectorLayer):
    def __init__(self, postGISDatabase=None, baseName="NewLayer", table=None, subset=None, schema = "public", \
                  geoColumn="geom", path=None, fileType=None, loadDefaultStyleFlag=True):

        if postGISDatabase:
            self._name = "vLayer<" + baseName + ">"
            dburi = postGISDatabase.getUri
            dburi.setDataSource(schema, table, geoColumn, subset)
            print dburi.connectionInfo()
            QgsVectorLayer.__init__(self, dburi.uri(), self._name)
            if self.isValid():
                printf(self._name + " successfully loaded.")
            else:
                printf(self._name + " failed to load.", "!!")
        else:
            fileInfo = QFileInfo(path)
            self._name = "vLayer<" + fileInfo.baseName() + ">"
            QgsVectorLayer.__init__(self, path=path, baseName=self._name, providerLib=fileType)
            if self.isValid():
                printf(self._name + " successfully loaded.")
            else:
                printf(self._name + " failed to load.", "!!")


db = PostGISDatabase("NYC")
vl = VectorLayer(path="/home/yop/Programmation/Python/SIG/workshop-data/nyc_subway_stations.shp")


