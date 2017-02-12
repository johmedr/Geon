from PyQt4.Qt import SIGNAL

from Geon.app import GApplicationWindow
from Geon.core import *
from Geon.utils import *

app = initGeon()

layerset = GLayerSet()

db = GPostGISDatabase()
db.loadShapefile("/home/yop/Programmation/Python/SIG/workshop-data/nyc_census_blocks.shp")
db.loadShapefile("/home/yop/Programmation/Python/SIG/workshop-data/nyc_neighborhoods.shp")

basemap = GRasterLayer("/home/yop/Programmation/Python/SIG/workshop-data/nyc_geo.tif")

streets = GVectorLayer(db, table="nyc_streets")
subways = GVectorLayer(db, table="nyc_subway_stations")
homicides = GVectorLayer(db, table="nyc_homicides")
census = GVectorLayer(db, table="nyc_census_blocks")
neighborhoods = GVectorLayer(db, table="nyc_neighborhoods")

layerset.addLayers(census, neighborhoods, subways, homicides, streets)
layerset.addBasemap(basemap)

mv = GApplicationWindow(layerset)
mv.show()
mv.connect(mv, SIGNAL("destroyed()"), app.exit)
app.exit(app.exec_())
