from qgis.core import *
from geon.database import PostGISDatabase
from geon.utils import *
from PyQt4.QtCore import QFileInfo

app = QgsApplication([], True)
app.setPrefixPath("/home/yop/anaconda2/pkgs/qgis-2.18.2-py27_0", True)
app.initQgis()

class VectorLayer(QgsVectorLayer):
    def __init__(self, postGISDatabase=None, baseName="NewLayer", table=None, subset=None, schema = "public", \
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
            QgsVectorLayer.__init__(self, path=path, baseName=fileInfo.baseName(), providerLib=fileType, loadDefaultStyleFlag=loadDefaultStyleFlag)
            if self.isValid():
                printf(self._name + " successfully loaded.")
            else:
                printf(self._name + " failed to load.", "!!")



db = PostGISDatabase("NYC")
vlay = VectorLayer(db, table="nyc_streets")
vl = VectorLayer(path="/home/yop/Programmation/Python/SIG/workshop-data/nyc_subway_stations.shp")



