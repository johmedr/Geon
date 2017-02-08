from geon.database import *
from geon.layer import *
from geon.view import *

app = QgsApplication([], True)
app.setPrefixPath("/home/yop/anaconda2/pkgs/qgis-2.18.2-py27_0", True)
app.initQgis()

db = PostGISDatabase()
l1 = VectorLayer(db, baseName="vl0", table="nyc_streets")
layerset = LayerSet(l1)

mv = MainWindow(layerset, l1.extent())
mv.show()

app.exit(app.exec_())





