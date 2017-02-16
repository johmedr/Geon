from PyQt4.Qt import QFileInfo
from qgis.core import QgsRasterLayer

from Geon.utils import *


class GRasterLayer(QgsRasterLayer):
    def __init__(self, path, *args):
        fileInfo = QFileInfo(path)
        self._name = "rLayer<" + fileInfo.baseName() + ">"
        QgsRasterLayer.__init__(self, path, *args)
        if not self.isValid():
            GPrint(self._name + " failed to load.", "!!")
        else:
            GPrint(self._name + " successfully loaded.")
