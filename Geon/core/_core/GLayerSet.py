from qgis.core import QgsMapLayerRegistry
from qgis.gui import QgsMapCanvasLayer


class GLayerSet(list):
    def __init__(self, *layers):
        list.__init__(self)
        self._rawLayers = []

        if layers:
            for l in list(layers):
                self.insert(0, QgsMapCanvasLayer(l))
                self._rawLayers.insert(0, l)
                QgsMapLayerRegistry.instance().addMapLayer(l)

    def contains(self, item):
        return self.__contains__(item)

    def addLayers(self, *newLayers):
        for l in list(newLayers):
            self.insert(0, QgsMapCanvasLayer(l))
            self._rawLayers.insert(0, l)
            QgsMapLayerRegistry.instance().addMapLayer(l)

    def appendLayerSet(self, layerSet):
        self = self + layerSet

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
