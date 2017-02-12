from copy import copy

from qgis.gui import QgsMapCanvas


class GMainCanvas(QgsMapCanvas):
    def __init__(self):
        self._layerSet = None
        self._displayedSet = None
        QgsMapCanvas.__init__(self)

    def setLayerSet(self, layerSet):
        self._layerSet = layerSet
        self._displayedSet = copy(self._layerSet)
        QgsMapCanvas.setLayerSet(self, self._displayedSet)

    def hideLayer(self, layer):
        self._displayedSet.remove(layer)
        QgsMapCanvas.setLayerSet(self, self._displayedSet)
        self.refresh()

    def showLayer(self, layer):
        self._displayedSet.insert(self._layerSet.index(layer), layer)
        QgsMapCanvas.setLayerSet(self, self._displayedSet)
        self.refresh()

    # a revoir
    def moveLayerUp(self, layer):
        newIndex = self._layerSet.index(layer) - 1
        if newIndex >= 0:
            self._layerSet.remove(layer)
            self._layerSet.insert(newIndex, layer)
            dispIndex = self._displayedSet.index(layer)
            if self._layerSet.index(self._displayedSet[dispIndex + 1]) <= newIndex:
                self._displayedSet.remove(layer)
                self._displayedSet.insert(dispIndex + 1, layer)
                QgsMapCanvas.setLayerSet(self, self._displayedSet)
                self.refresh()

    def moveLayerDown(self, layer):
        newIndex = self._displayedSet.index(layer) + 1
        if newIndex < len(self._displayedSet):
            self._displayedSet.remove(layer)
            self._displayedSet.insert(newIndex, layer)
            QgsMapCanvas.setLayerSet(self, self._displayedSet)
            self.refresh()
