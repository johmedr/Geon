from qgis.core import QgsMapLayerRegistry
from qgis.gui import QgsMapCanvasLayer

from Geon.utils import GPrint


class GLayerSet(list):
    def __init__(self, *layers):
        list.__init__(self)
        self._rawLayers = []
        if layers:
            for l in list(layers):
                self.insert(0, QgsMapCanvasLayer(l))
                self._rawLayers.insert(0, l)
                QgsMapLayerRegistry.instance().addMapLayer(l)

    def layer(self, layerName):
        l = None
        for l in self._rawLayers:
            if l.name() == layerName:
                break
        if l.name() != layerName:
            GPrint("Layer " + layerName + " not in set.", "!!")
            return False
        else:
            return l

    def contains(self, item):
        isin = self.__contains__(item) or self._rawLayers.__contains__(item)
        if not isin:
            for l in self._rawLayers:
                if item.name() == l.name():
                    isin = True
                    break
        return isin

    def addLayers(self, *newLayers):
        for l in list(newLayers):
            self.insert(0, QgsMapCanvasLayer(l))
            self._rawLayers.insert(0, l)
            QgsMapLayerRegistry.instance().addMapLayer(l)

    def appendLayerSet(self, layerSet):
        self.__add__(layerSet)

    def addBasemap(self, basemap):
        self._rawLayers.append(basemap)
        self.append(QgsMapCanvasLayer(basemap))
        QgsMapLayerRegistry.instance().addMapLayer(basemap)

    def __str__(self):
        msg = ""
        for l in self:
            msg += str(l) + " "
        return msg

    def _getRawLayers(self):
        return self._rawLayers

    rawLayers = property(_getRawLayers)
