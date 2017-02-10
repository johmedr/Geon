from geon.database import *
from geon.view import *
from qgis.utils import iface

def initGeon():
    app = QgsApplication([], True)
    app.setPrefixPath(qgisPath, True)
    app.initQgis()
    return app

app = initGeon()

layerset = LayerSet()

db = PostGISDatabase()
db.loadShapefile("/home/yop/Programmation/Python/SIG/workshop-data/nyc_census_blocks.shp")
db.loadShapefile("/home/yop/Programmation/Python/SIG/workshop-data/nyc_neighborhoods.shp")

basemap = RasterLayer("/home/yop/Programmation/Python/SIG/workshop-data/nyc_geo.tif")

streets = VectorLayer(db, table="nyc_streets")
subways = VectorLayer(db, table="nyc_subway_stations")
homicides = VectorLayer(db, table="nyc_homicides")
census = VectorLayer(db, table="nyc_census_blocks")
neighborhoods = VectorLayer(db, table="nyc_neighborhoods")


layerset.addLayers(census, neighborhoods, subways, homicides, streets)
layerset.addBasemap(basemap)

mv = MainWindow(layerset)
mv.show()
mv.connect(mv, SIGNAL("destroyed()"), app.exit)
app.exit(app.exec_())










