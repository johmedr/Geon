from qgis.core import QgsApplication

from GConst import *


def GInit():
    app = QgsApplication([], True)
    app.setPrefixPath(QGIS_PATH, True)
    app.initQgis()
    return app


def GPrint(msg, flag="Ok"):
    if VERBOSE:
        print "[" + flag + "] " + str(msg)
