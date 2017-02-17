from PyQt4.Qt import QFileInfo
from qgis.core import QgsRasterLayer

from GLayer import GLayer
from Geon.utils import *


class GRasterLayer(GLayer, QgsRasterLayer):
    def __init__(self, path, *args):
        fileInfo = QFileInfo(path)
        QgsRasterLayer.__init__(self, path, *args)
        GLayer.__init__(self, baseName=fileInfo.baseName(), name="rLayer<" + fileInfo.baseName() + ">")
        if not self.isValid():
            GPrint(self._name + " failed to load.", "!!")
        else:
            GPrint(self._name + " successfully loaded.")
