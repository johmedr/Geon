import sip

for api in ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]:
    sip.setapi(api, 2)

from Geon.app import GApplicationWindow
from Geon.core import *
from Geon.utils import *
from PyQt4.Qt import SIGNAL

app = GInit()

layerset = GLayerSet()

db = GPostGISDatabase()

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
