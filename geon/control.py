from geon.database import *
from geon.layer import *
from geon.view import *

def initGeon():
    app = QgsApplication([], True)
    app.setPrefixPath(qgisPath, True)
    app.initQgis()
    return app

app = initGeon()

layerset = LayerSet()

db = PostGISDatabase()
db.loadShapefile("/home/yop/Programmation/Python/SIG/workshop-data/nyc_homicides.shp")

basemap = RasterLayer("/home/yop/Programmation/Python/SIG/workshop-data/nyc_geo.tif")

streets = VectorLayer(db, table="nyc_streets")
subways = VectorLayer(db, table="nyc_subway_stations")
homicides = VectorLayer(db, table="nyc_homicides")



layerset.addLayers(streets, subways, homicides)
layerset.addBasemap(basemap)

mv = MainWindow(layerset)
mv.show()
app.exit(app.exec_())










