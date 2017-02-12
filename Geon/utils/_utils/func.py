from qgis.core import QgsApplication

from const import *


def initGeon():
    app = QgsApplication([], True)
    app.setPrefixPath(QGIS_PATH, True)
    app.initQgis()
    return app


def printf(msg, flag="Ok"):
    if VERBOSE:
        print "[" + flag + "] " + str(msg)
